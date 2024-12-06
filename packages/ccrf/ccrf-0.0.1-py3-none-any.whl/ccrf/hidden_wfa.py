import torch
import torch.nn as nn
import torch.nn.functional as F

from ccrf.utils import logmmexp

import automic

# close enough :P
inf = 1e4

class HiddenWFACRF(nn.Module):
    def __init__(self, n_labels, n_states):
        super().__init__()

        self.n_labels = n_labels
        self.n_states = n_states

        self.transitions = nn.Parameter(0.01 * torch.randn(self.n_states, self.n_labels, self.n_states))

    def _Q(self, x_label, x_state=None):
        # x_label: float[batch_size, sequence_length, self.n_labels]
        batch_size = x_label.shape[0]
        sequence_length = x_label.shape[1]
        # x_state: float[batch_size, sequence_length, self.n_states]
        if x_state is None:
            x_state = x_label.new_zeros((batch_size, sequence_length, self.n_states))

        state_logits = x_label.new_zeros((batch_size, self.n_states))
        # state_logits: float32[batch_size, self.n_states]
        
        for i in range(sequence_length):
            xli = x_label[:,i,:]
            # xli: float[batch_size, self.n_labels]
            xsi = x_state[:,i,:]
            # xsi: float[batch_size, self.n_states]
            label_state_logits = logmmexp(state_logits, self.transitions.view(self.n_states, self.n_labels * self.n_states)).view(batch_size, self.n_labels, self.n_states)
            # label_state_logits: float32[batch_size, self.n_labels, self.n_states]
            label_state_logits = label_state_logits + xli.view(batch_size, self.n_labels, 1)
            label_state_logits = label_state_logits + xsi.view(batch_size, 1, self.n_states)
            state_logits = torch.logsumexp(label_state_logits, 1)

        return torch.logsumexp(state_logits, dim=1)
        
    def _score(self, y, x_label, x_state=None):
        # y: long[batch_size, sequence_length]
        # x_label: float[batch_size, sequence_length, self.n_labels]
        # x_label: float[batch_size, sequence_length, self.n_states]

        batch_size, sequence_length = y.shape
        
        mask = torch.full_like(x_label, -inf)
        # mask: float[batch_size, sequence_length, self.n_labels]
        mask.scatter_(2, y.view(batch_size, sequence_length, 1), 0)

        return self._Q(x_label + mask, x_state)

            
    def forward(self, x_label, x_state):
        # x_label : float[batch_size, sequence_length, self.n_labels]
        batch_size = x_label.shape[0]
        sequence_length = x_label.shape[1]
        # x_state: float[batch_size, sequence_length, self.n_states]
        if x_state is None:
            x_state = x_label.new_zeros((batch_size, sequence_length, self.n_states))



        label_state_logits = x_label.new_zeros((batch_size, sequence_length, self.n_labels, self.n_states))
        # label_state_logits: float32[1+batch_size, sequence_length, self.n_labels, self.n_states]

        label_state_logits += x_label.view(batch_size, sequence_length, self.n_labels, 1)
        label_state_logits += x_state.view(batch_size, sequence_length, 1, self.n_states)


        for i in range(sequence_length):
            if i > 0:
                transition_scores = logmmexp(last_state_logits, self.transitions.view(self.n_states, self.n_labels*self.n_states)).view(batch_size, self.n_labels, self.n_states)
                # transition_scores: float32[batch_size, self.n_labels, self.n_states]
                label_state_logits[:,i] += transition_scores
            last_state_logits = torch.logsumexp(label_state_logits[:,i], 1)
            # last_stae_logits: float32[batch_size, self.n_states]

        # BEGIN BACKWARDS PASS

        sample_sequence = x_label.new_full((batch_size, sequence_length), 0, dtype=torch.int64)
        # sample_sequence: int64[batch, sequence_length]

        transitionsT = self.transitions.permute(2, 1, 0)
        # transitionsT: float32[self.nl_labels, self.n_states, self.n_states]

        last_label_state_logits = None

        for i in reversed(range(sequence_length)):
            if last_label_state_logits is not None:
                forward_transitions = logmmexp(
                    last_label_state_logits.view(batch_size, self.n_labels*self.n_states),
                    transitionsT.reshape(self.n_labels*self.n_states, self.n_states)
                ).view(batch_size, self.n_states)
            else:
                forward_transitions = x_label.new_zeros((batch_size, self.n_states))
            # forward_transitions: float32[batch_size, self.n_states]
            
            sample_label_state_logits = label_state_logits[:,i,:]
            # sample_logits: float32[batch_size, self.n_labels, self.n_states]
            
            sample_label_state_logits = sample_label_state_logits + forward_transitions.view(batch_size, 1, self.n_states)

            # marginalize over states
            sample_label_logits = torch.logsumexp(sample_label_state_logits, 2)
            # sample_label_logits: float32[batch, self.n_labels]

            samples = torch.argmax(sample_label_logits, dim=1)
            # samples: int64[batch_size]
            
            sample_sequence[:,i] = samples

            indices = samples.view(batch_size, 1).repeat(1, self.n_states).view(batch_size, 1, self.n_states)

            mask = torch.full_like(sample_label_state_logits, -inf)

            mask.scatter_(1, indices, 0)


            last_label_state_logits = sample_label_state_logits + mask
            # last_state_logits: float32[batch, self.n_states]

        return sample_sequence

    def loss(self, y, x_label, x_state=None):
        nll = self._Q(x_label, x_state) - self._score(y, x_label, x_state)
        return torch.mean(nll)

    def sample(self, x, k, temp=1):
        raise NotImplementedError
        """
        sample from the distribution
        """
        # x : float[batch_size, sequence_length, n_labels]
        x = x[:,:,self.tag2label] / temp
        # x: float[batch_size, sequence_length, n_tags]
        batch_size, sequence_length, _ = x.shape

        transitions = self._transitions(temp)

        logits = x.new_full((batch_size, sequence_length, self.n_tags), -inf)
        # logits: float[batch_size, sequence_length, self.n_tags]
        for tag in self.start_tags:
            logits[:,0,tag] = x[:,0,tag]
        for i in range(1, sequence_length):
            xi = x[:,i,:]
            # xi: float[batch_size, self.n_tags]
            logits[:,i] = logmmexp(logits[:,i-1], transitions) + xi

        for tag in range(self.n_tags):
            if tag not in self.end_tags:
                logits[:,-1,tag] = -inf
            
        sample_sequence = x.new_full((batch_size, k, sequence_length), 0, dtype=torch.int64)
        # sample_sequence: int64[batch, k, sequence_length]
        
        sample_logits = logits[:,-1,:]
        
        sample_p = F.softmax(sample_logits, dim=-1)
        # sample_p: float32[batch, self.n_tags]

        sample_sequence[:,:,-1] = torch.multinomial(sample_p, k, replacement=True)
        for i in reversed(range(sequence_length-1)):
            sample_logits = logits[:,i,:].view(batch_size, 1, self.n_tags)
            # sample_logits: float32[batch_size, 1, self.n_tags]
            forward_transitions = (transitions.T)[sample_sequence[:,:,i+1],:]
            # forward_transitions: float32[batch_size, k, self.n_tags]
            sample_logits = sample_logits + forward_transitions
            # sample_logits: float32[batch_size, k, self.n_tags]
            sample_p = F.softmax(sample_logits + forward_transitions, dim=-1)
            # sample_p: float32[batch_size, k, self.n_tags]
            sample_p = sample_p.view(batch_size*k, -1)
            samples = torch.multinomial(sample_p, 1)
            sample_sequence[:,:,i] = samples.view(batch_size, k)
        return sample_sequence
