import torch
import torchaudio
from torch import nn, t
from Models import dolphinwhistledataset_localData
from Models import dolphinwhistledataset
from Models.CNNfromScratch_audio_network import Network
from torch import optim
from torch.utils.data import DataLoader
import json
import torch.nn.functional as Functional
import Models.metric_calculations as m
import matplotlib.pyplot as plt

# Get the parameters for the neural network from the parameters.json file

with open('parameters.json', 'r') as file:
    data = json.load(file)
    batch_size = data['ML_batch_size']
    epochs = data['ML_num_epochs']
    learning_rate = data['ML_learning_rate']
    batch_size = data['ML_batch_size']

    sample_rate = data['conversion_sample_rate']
    number_samples = data['conversion_num_samples']
    n_fft = data['conversion_n_fft']
    hop_length = data['conversion_hop_length']
    num_mels = data['conversion_num_mels']


# accomodating both OCEAN and local data
class_model_OCEAN = [
        '3ebfce8d-769b-11ef-9a56-0050568e393c/',
        '3ebfcfab-769b-11ef-9a56-0050568e393c/'
]

class_model_Local = [
        'bottlenose_dolphin',
        'common_dolphin',
        'killer_whale',
        'long-finned_pilot_whale',
        'rissos_dolphin',
        'white-beaked_dolphin',
]



def train_epoch(neural_network, data, loss_function, optimiser, device):
    # Train the model on the network on all data
        running_loss = 0

        for input, target in data:
            input = input.to(device)
            target = target.to(device)

            prediction = neural_network(input)
            loss = loss_function(prediction, target)
            running_loss += loss * input.size(0)
            optimiser.zero_grad()
            loss.backward()

            optimiser.step()
        return running_loss/len(data)


def train_model(neural_network, data, loss_function, optimiser, device, num_epochs):
    # Train the model on a number of epochs
    loss_array = []
    for i in range(num_epochs):
        loss = train_epoch(neural_network, data, loss_function, optimiser, device)
        loss_array.append(loss)
    print("finished")

    loss_array = torch.tensor(loss_array)
    plt.plot(loss_array.detach().cpu().numpy())
    plt.savefig('loss_graph.png')


def data_loader(training_data, batch_size):
    data_loader = DataLoader(dataset=training_data, batch_size = batch_size, shuffle=True,num_workers=2)

    return data_loader



def train(path):

    # getting training data, accomodating both OCEAN and local data
    if (path == "./split_ocean_downloads/"):
        ANNOTATIONS_FILE = "./split_ocean_downloads/training/labels_train.csv"
        AUDIO_DIR = "./split_ocean_downloads/training/"
    else:
        ANNOTATIONS_FILE = path + "/labels_train.csv"
        AUDIO_DIR = path + "/training"


    # Decide the device used
    if torch.cuda.is_available():
        device = "cuda"
    else:
        device = "cpu"
    print(f"Using {device}")

    spectrogram = torchaudio.transforms.Spectrogram(
             n_fft=n_fft,
             hop_length=hop_length,
             win_length=1000
    )

     # convert data, accomodating both OCEAN and local data
    if (path == "./split_ocean_downloads/"):
        data = dolphinwhistledataset.DolphinWhistleDataset(ANNOTATIONS_FILE, AUDIO_DIR, spectrogram,sample_rate, number_samples, device)
    else:
        data = dolphinwhistledataset_localData.DolphinWhistleDataset(ANNOTATIONS_FILE, AUDIO_DIR, spectrogram,sample_rate, number_samples, device)
        print(data)
    # load the data
    load_data = data_loader(data, batch_size)
    # create the neural network
    neural_network = Network().to(device)

    # Initialise loss function
    loss_function = nn.CrossEntropyLoss()

    # Initialise optimiser 
    optimiser = torch.optim.Adam(neural_network.parameters(), lr = learning_rate)

    # Train the model
    train_model(neural_network, load_data, loss_function, optimiser, device, epochs)

    # Save it in a file, to allow future testing
    torch.save(neural_network.state_dict(), "neural_network.pth")



def predict(model, input, target, path):
    # Method to predict the species of dolphin based on a spectogram input

    model.eval()
    with torch.no_grad():
        predictions = model(input)

        probabilities = Functional.softmax(predictions, dim=1)
        predicted_index = torch.argmax(predictions).item()

        # Convert into numbers instead of names, accomodating both OCEAN and local data

        if (path == "./split_ocean_downloads/"):
            predicted = class_model_OCEAN[predicted_index]
            expected = class_model_OCEAN[target]
        else:
            predicted = class_model_Local[predicted_index]
            expected = class_model_Local[target]


    return predicted, expected, probabilities



def test(path):
    # Call neural network
    neural_network = Network()
    # Load the trained network
    state_dict = torch.load("neural_network.pth", weights_only=True)
    neural_network.load_state_dict(state_dict)

    # getting testing data, accomodating both OCEAN and local data
    if (path == "./split_ocean_downloads/"):
        ANNOTATIONS_FILE = "./split_ocean_downloads/testing/labels_test.csv"
        AUDIO_DIR = "./split_ocean_downloads/testing/"
    else:
        ANNOTATIONS_FILE = path + "/labels_test.csv"
        AUDIO_DIR = path + "/testing"

    

    # Load the spectogram
    spectrogram = torchaudio.transforms.Spectrogram(
             n_fft=n_fft,
             hop_length=hop_length,
             win_length=1000
    )


    # Transform audio into spectogram,accomodating both OCEAN and local data
    if (path == "./split_ocean_downloads/"):
        data = dolphinwhistledataset.DolphinWhistleDataset(ANNOTATIONS_FILE, AUDIO_DIR, spectrogram,sample_rate, number_samples, "cpu")
    else:
        data = dolphinwhistledataset_localData.DolphinWhistleDataset(ANNOTATIONS_FILE, AUDIO_DIR, spectrogram,sample_rate, number_samples, "cpu")

    correct = 0
    overall = 0

    predicted_list = []
    expected_list = []
    probabilities_list = []


    # Run through all the data
    for x, (input, target) in enumerate(data):

        input.unsqueeze_(0)
        # Predict the data and calculate accuracy
        predicted, expected, probabilities = predict(neural_network, input, target,path)
        print(f"Predicted: '{predicted}', expected: '{expected}'")

        predicted_list.append(predicted)
        expected_list.append(expected)
        probabilities_list.append(probabilities)

        if predicted == expected:
            correct += 1
        overall += 1



     # get the metrics, to accomodate both OCEAN and local data
    if (path == "./split_ocean_downloads/"):
        m.calculate_metrics(correct, overall, predicted_list, expected_list, class_model_OCEAN)
    else:
        m.calculate_metrics(correct, overall, predicted_list, expected_list, class_model_Local)


def run(path):

    train(path)
    test(path)

