import torch
import torchaudio
from sklearn.metrics import precision_score, recall_score, confusion_matrix


"""
Calculating and printing the Evaluation Metrics
"""


def accuracy(correct, overall):
    return 100 * correct // overall


def positives_precision(predicted, expected, pos_label):
    return precision_score(expected, predicted,pos_label=pos_label, average='macro')


def negatives_precision(predicted, expected, pos_label):
    return recall_score(expected, predicted,pos_label=pos_label, average='macro')

def matrix(predicted, expected):
    return confusion_matrix(expected, predicted)


def calculate_metrics(correct, overall, predicted, expected, values):

    print("Accuracy")
    print(accuracy(correct, overall))
    print()

    for value in values:
        print("Positives Precision: " + value)
        print(positives_precision(predicted, expected, value))
        print()

        print("Negatives Precision: " + value)
        print(negatives_precision(predicted, expected, value))
        print()

    print("Confusion Matrix")
    print(matrix(predicted, expected))
    print()
    