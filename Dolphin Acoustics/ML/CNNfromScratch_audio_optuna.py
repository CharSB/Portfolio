import torch
import torchaudio
from torch import nn, t
from Models.CNNfromScratch_audio_optuna_network import Network
from torch import optim
from Models import dolphinwhistledataset_localData
from Models import dolphinwhistledataset
from torch.utils.data import DataLoader
import os
from plotly.io import show
import optuna
from optuna.trial import TrialState
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import torch.utils.data
from optuna.visualization import plot_intermediate_values
from optuna.visualization import plot_optimization_history
from optuna.visualization import plot_parallel_coordinate
import matplotlib.pyplot as plt
import kaleido

batch_size = 32
epochs = 1
sample_rate = 22050
number_samples = 22050
device = torch.device("cpu")
path = ""

def get_data(path):
    """Get the training and testing data, and convert to spectograms"""
    
    mel_spectrogram = torchaudio.transforms.MelSpectrogram(
            sample_rate=sample_rate,
            n_fft=1024,
            hop_length=512,
            n_mels=64
    )

    # load the training data, accomodating both OCEAN and local data
    
    if (path == "./split_ocean_downloads/"):
        ANNOTATIONS_FILE = "./split_ocean_downloads/training/labels_train.csv"
        AUDIO_DIR = "./split_ocean_downloads/training/"
        training_data = dolphinwhistledataset.DolphinWhistleDataset(ANNOTATIONS_FILE, AUDIO_DIR, mel_spectrogram,sample_rate, number_samples, device)
    
    else:
        ANNOTATIONS_FILE = path + "/labels_train.csv"
        AUDIO_DIR = path + "/training"
        training_data = dolphinwhistledataset_localData.DolphinWhistleDataset(ANNOTATIONS_FILE, AUDIO_DIR, mel_spectrogram,sample_rate, number_samples, device)
    train_data = DataLoader(dataset=training_data, batch_size = batch_size, shuffle=True,num_workers=2)
    
    # load the testing data, accomodating both OCEAN and local data
    if (path == "./split_ocean_downloads/"):
        ANNOTATIONS_FILE = "./split_ocean_downloads/testing/labels_test.csv"
        AUDIO_DIR = "./split_ocean_downloads/testing/"
        testing_data = dolphinwhistledataset.DolphinWhistleDataset(ANNOTATIONS_FILE, AUDIO_DIR, mel_spectrogram,sample_rate, number_samples, device)

    else:
        ANNOTATIONS_FILE = path + "/labels_test.csv"
        AUDIO_DIR = path + "/testing"
        testing_data = dolphinwhistledataset_localData.DolphinWhistleDataset(ANNOTATIONS_FILE, AUDIO_DIR, mel_spectrogram,sample_rate, number_samples, device)
    test_data = DataLoader(dataset=testing_data, batch_size = batch_size, shuffle=True,num_workers=2)

    return train_data, test_data

def objective_path(path):
    def objective(trial):
        # Generate the model.
        model = Network(trial).to(device)

        # Generate the optimizer.
        optimizer_name = trial.suggest_categorical("optimizer", ["Adam", "RMSprop", "SGD"])
        learning_rate = trial.suggest_float("lr", 1e-5, 1e-1, log=True)
        optimizer = getattr(optim, "Adam")(model.parameters(), lr=learning_rate)
        #batch_size = trial.suggest_categorical('batch_size', [16, 32, 64, 128, 256])
        num_trained = batch_size * 30
        num_valid = batch_size * 10

        # Get the data
        train_loader, valid_loader = get_data(path)


        for epoch in range(epochs):
            # Train the model
            model.train()
            for batch_idx, (data, target) in enumerate(train_loader):
                if batch_idx * batch_size >= num_trained:
                    break

                data, target = data.view(data.size(0), 1,128,22).to(device), target.to(device)
                
                optimizer.zero_grad()
                output = model(data)
                loss = F.nll_loss(output, target)
                loss.backward()
                optimizer.step()

            # Evaluate the model and predict
            
            model.eval()
            correct = 0
            with torch.no_grad():
                for batch_idx, (data, target) in enumerate(valid_loader):
                    # Limit the test data.
                    if batch_idx * batch_size >= num_valid:
                        break
                    data, target = data.view(data.size(0), 1,128,22).to(device), target.to(device)
                    output = model(data)

                    pred = output.argmax(dim=1, keepdim=True)
                    correct += pred.eq(target.view_as(pred)).sum().item()

            # Calculate accuracy
            accuracy = (correct / min(len(valid_loader.dataset), num_valid)) * 100

            trial.report(accuracy, epoch)

            # Handle pruning based on the intermediate value.
            if trial.should_prune():
                raise optuna.exceptions.TrialPruned()

        return accuracy
    return objective


def run(path_input):
    # Create an Optuna study
    study = optuna.create_study(direction="maximize")
    # Run a number of trials

    study.optimize(objective_path(path_input), n_trials=2, timeout=20000)
    
    # Calculate complete and pruned files
    pruned_trials = study.get_trials(deepcopy=False, states=[TrialState.PRUNED])
    complete_trials = study.get_trials(deepcopy=False, states=[TrialState.COMPLETE])

    print("Study statistics: ")
    print("  Number of finished trials: ", len(study.trials))
    print("  Number of pruned trials: ", len(pruned_trials))
    print("  Number of complete trials: ", len(complete_trials))

    print("Best trial:")
    trial = study.best_trial

    print("Value:", trial.value)

    print("Params:")
    for key, value in trial.params.items():
        print("    {}: {}".format(key, value))
    
    # Plot the optimization history across trials
    fig = plot_optimization_history(study)
    fig.write_image(f"optimisationhistory_best{trial.value}.png")

    # Plot the learning rate of each trial
    fig = plot_intermediate_values(study)
    fig.write_image(f"intermediatevalues_best{trial.value}.png")

    # Plot the hyperparameter values tested
    fig = plot_parallel_coordinate(study)
    fig.write_image(f"parallel_best{trial.value}.png")