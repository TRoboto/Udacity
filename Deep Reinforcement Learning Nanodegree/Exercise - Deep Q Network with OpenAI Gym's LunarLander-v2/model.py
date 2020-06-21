import torch
import torch.nn as nn
import torch.nn.functional as F

class QNetwork(nn.Module):
    """Actor (Policy) Model."""

    def __init__(self, state_size, action_size, seed):
        """Initialize parameters and build model.
        Params
        ======
            state_size (int): Dimension of each state
            action_size (int): Dimension of each action
            seed (int): Random seed
        """
        super(QNetwork, self).__init__()
        self.seed = torch.manual_seed(seed)
        
        self.fc1 = nn.Linear(state_size, state_size*2)
        self.fc2 = nn.Linear(state_size*2, state_size*8)
        self.fc3 = nn.Linear(state_size*8, state_size*16)
        self.fc4 = nn.Linear(state_size*16, action_size)

        self.dropout = nn.Dropout(0.25)
    def forward(self, state):
        """Build a network that maps state -> action values."""
        x = self.dropout(F.relu(self.fc1(state)))
        x = self.dropout(F.relu(self.fc2(x)))
        x = self.dropout(F.relu(self.fc3(x)))
        x = self.fc4(x)
        
        return x
