import torch
from torch.utils.data import Dataset, DataLoader
import torchaudio
import pandas as pd
import os
import soundfile as sf

"""
Class to convert the audio data into images for local data
"""
class DolphinWhistleDataset(Dataset):
    
    get_index = {
        'bottlenose_dolphin': 0,
        'common_dolphin': 1,
        'killer_whale': 2,
        'long-finned_pilot_whale': 3,
        'rissos_dolphin': 4,
        'white-beaked_dolphin': 5,
    }

    # Constructor
    # annotations_file - FILE containing all annotations for the audio files
    # audio_dir - DIRECTORY containing all the audio files 
    def __init__(self, annotations_file, audio_dir,transformation,target_sample_rate,
                 num_samples,
                 device):
        self.annotations = pd.read_csv(annotations_file)
        self.audio_dir = audio_dir
        self.device = device
        self.transformation = transformation.to(self.device)
        self.target_sample_rate = target_sample_rate
        self.num_samples = num_samples
        # no duplicates of audio files 
        name_set=set()
        for root, dirs, files in os.walk(audio_dir):
            for file in files:
                if file.endswith('wav'):
                    name_set.add(file)
        name_set=list(name_set)
        self.datalist=name_set

    # Method to define how to use length syntax 
    # len(dolphin dataset) = ?
    # number of sample?
    def __len__(self):
        return len(self.datalist)

    # a_list[1] -> a_list.__getitem__(1) 
    # how to get items from dataset
    def __getitem__(self, index):
        index = index - 1
        # return path to audio file from database
        audio_sample_path = self._get_audio_sample_path(index)
        # label associate with this sample path
        label = self._get_audio_sample_label(index)
        label_indexed = self.get_index[label]

        signal, sr = torchaudio.load(audio_sample_path, format='wav')

        # MORE STUFF 
        signal = signal.to(self.device)
        signal = self._resample_if_necessary(signal, sr)
        signal = self._mix_down_if_necessary(signal)
        signal = self._cut_if_necessary(signal)
        signal = self._right_pad_if_necessary(signal)
        signal = self.transformation(signal)
        return signal, torch.tensor(label_indexed)


    # TODO implement this based off database structure we use
    def _get_audio_sample_path(self, index):
        index = index - 1
        fold = f"{self.annotations.iloc[index, 1]}"
        path = os.path.join(self.audio_dir, fold, self.annotations.iloc[
            index, 0])
        return path
    
    def _cut_if_necessary(self, signal):
        if signal.shape[1] > self.num_samples:
            signal = signal[:, :self.num_samples]
        return signal
    
    def _right_pad_if_necessary(self, signal):
        length_signal = signal.shape[1]
        if length_signal < self.num_samples:
            num_missing_samples = self.num_samples - length_signal
            last_dim_padding = (0, num_missing_samples)
            signal = torch.nn.functional.pad(signal, last_dim_padding)
        return signal
    
    def _resample_if_necessary(self, signal, sr):
        if sr != self.target_sample_rate:
            resampler = torchaudio.transforms.Resample(sr, self.target_sample_rate)
            signal = resampler(signal)
        return signal

    def _mix_down_if_necessary(self, signal):
        if signal.shape[0] > 1:
            signal = torch.mean(signal, dim=0, keepdim=True)
        return signal

    
    # TODO implement this based off database structure we use
    def _get_audio_sample_label(self, index):
        index = index - 1
        return self.annotations.iloc[index, 1]
    
