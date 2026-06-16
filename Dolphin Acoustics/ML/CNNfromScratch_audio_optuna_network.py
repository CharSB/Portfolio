from torch import nn
import optuna
from optuna.trial import TrialState
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data

class Network(nn.Module):
    """
    Neural network class for the training and validation with hyperparameter tuning
    """

    def __init__(self, trial):
        super().__init__()
        # Suggest the number the layers
        num_layers = trial.suggest_int("n_layers",1,5)
        layers = []
        in_channels = 1
        out_channels = 28

        # Form each of the layers, suggesting the number of filters and kernel size
        # Each layer is convolutional with an ReLu activation function 
        for x in range(num_layers):
            out_channels = trial.suggest_int(f"num_filters{x}",8,128)
            kernel_size = trial.suggest_int(f"kernel_size{x}",3,5)
            layers.append(nn.Conv2d(in_channels, out_channels, kernel_size=kernel_size,padding=2))
            layers.append(nn.ReLU())
            layers.append(nn.MaxPool2d(kernel_size=2))
            in_channels = out_channels

        self.layers = nn.Sequential(*layers)

        # Make sure the layers fit into the network format
        self.adapt = nn.AdaptiveAvgPool2d((5,4))

        # Flatten the layers
        self.flatten = nn.Flatten()
        
        # Linear transformation into a single layer
        self.linear = nn.Linear(in_channels * 5 * 4, 10)

    # One forward pass in then neural network
    def forward(self, input):
        input = self.layers(input)
        input = self.adapt(input)
        input = self.flatten(input)
        prediction = self.linear(input)
        return prediction