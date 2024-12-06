import statistics

import torch
import torch.nn as nn
import torch.nn.functional as F

from ccrf.utils import logmmexp

import automic

# close enough :P
inf = 1e4

class MultipleCRF(nn.Module):
    def __init__(self, n_labels, duplicity):
        super().__init__()

        self.n_labels = n_labels
        self.duplicity = duplicity

        self.transitions = nn.Parameter(0.1 * torch.randn(self.n_labels*self.duplicity, self.n_labels * self.duplicity))

    def _Q(self, x):
        # x: float[batch_size, sequence_length, self.n_labels, self.duplicity]
        batch_size = x.shape[0]
        sequence_length = x.shape[1]
        
        logits = x.new_zeros((batch_size, self.n_labels, self.duplicity))
        # logits: float32[batch_size, self.n_labels, self.duplicity]
        
        for i in range(sequence_length):
            xi = x[:,i,:]
            # xi: float[batch_size, self.n_labels, self.duplicity]
            if i > 0:
                logits = logmmexp(
                    logits.view(batch_size, self.n_labels*self.duplicity),
                    self.transitions
                ).view(batch_size, self.n_labels, self.duplicity)
                # logits: float32[batch_size, self.n_labels, self.duplicity]
            logits = logits + xi

        return torch.logsumexp(logits, dim=(1,2))
        
    def _score(self, x, y):
        # y: long[batch_size, sequence_length]
        # x: float[batch_size, sequence_length, self.n_labels, self.duplicity]

        batch_size, sequence_length = y.shape
        
        mask = x.new_full((batch_size, sequence_length, self.n_labels), -inf)
        # mask: float[batch_size, sequence_length, self.n_labels]
        
        mask.scatter_(2, y.view(batch_size, sequence_length, 1), 0)

        return self._Q(x + mask.view(batch_size, sequence_length, self.n_labels, 1))

            
    def forward(self, x, k=200):
        # sample a bunch of sequences, and pick the mode
        # x : float[batch_size, sequence_length, self.n_labels, self.duplicity]
        samples = self.sample(x, k)
        # samples: int64[batch_size, k, sequence_length]
        # we want the mode sequence, not the position-wide mode
        modes = torch.tensor(
            [statistics.mode([tuple(row.tolist()) for row in instance]) for instance in samples],
            device=x.device
        )
        # modes: int64[batch_size, sequence_length

        return modes

    def loss(self, x, y):
        nll = self._Q(x) - self._score(x, y)
        return torch.mean(nll)

    def sample(self, x, k):
        """Samples ys from the distribution P(y|x)
            Args:
                x: input potentials; float32[batch, sequence_length, n_labels, duplicity]
                k: number of samples per input x (independent and with replacement)
            Returns:
                output tags; int64[batch, k, sequence_length]
        """
        # x : float[batch_size, sequence_length, self.n_labels, self.duplicity]
        batch_size, sequence_length, _, _ = x.shape

        logits = x.clone()
        # logits: float[batch_size, sequence_length, self.n_labels, self.duplicity]
        
        for i in range(1, sequence_length):
            logits[:,i] += logmmexp(
                logits[:,i-1].view(batch_size, self.n_labels*self.duplicity),
                self.transitions
            ).view(batch_size, self.n_labels, self.duplicity)
            
        sample_sequence = x.new_full((batch_size, k, sequence_length), 0, dtype=torch.int64)
        # sample_sequence: int64[batch, k, sequence_length]
        
        sample_logits = logits[:,-1].view(batch_size, self.n_labels*self.duplicity)
        # sample_logits: float32[batch_size, self.n_labels*self.duplcitiy]

        
        sample_p = F.softmax(sample_logits, dim=-1)
        # sample_p: float32[batch, self.n_labels*self.duplicity]
        
        sample_sequence[:,:,-1] = torch.multinomial(sample_p, k, replacement=True)
        
        for i in reversed(range(sequence_length-1)):
            sample_logits = logits[:,i].view(batch_size, 1, self.n_labels*self.duplicity)
            # sample_logits: float32[batch_size, 1, self.n_labels*self.duplicity]
            forward_transitions = (self.transitions.T)[sample_sequence[:,:,i+1],:]
            # forward_transitions: float32[batch_size, k, self.n_labels*self.duplicity]
            sample_logits = sample_logits + forward_transitions
            # sample_logits: float32[batch_size, k, self.n_labels*self.duplicity]
            sample_p = F.softmax(sample_logits, dim=-1)
            # sample_p: float32[batch_size, k, self.n_labels*self.duplicity]
            sample_p = sample_p.view(batch_size*k, -1)
            samples = torch.multinomial(sample_p, 1)
            sample_sequence[:,:,i] = samples.view(batch_size, k)
        # Each element of sample_sequence corresponds to a label*duplicity pair -- marginalize over duplicities
        return sample_sequence // self.duplicity
