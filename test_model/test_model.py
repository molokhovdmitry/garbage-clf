import os
import torch
from sklearn.metrics import f1_score, classification_report

from dataloader import init_loader

BATCH_SIZE = os.getenv('BATCH_SIZE')
IMG_SIZE = os.getenv('IMG_SIZE')


def test_f1():

    device = torch.device('cpu')
    print(f"Device: {device}")

    # Load the test data
    _, test_loader = init_loader('test', BATCH_SIZE, IMG_SIZE)

    # Load the model
    model = torch.load('../models/model.pt', map_location=device)

    model.eval()

    # Get the predictions
    val_f1 = 0
    full_preds = []
    full_labels = []
    with torch.no_grad():
        for inputs, labels in test_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            outputs = model(inputs)
            _, preds = torch.max(outputs, 1)
            full_preds.extend(preds.tolist())
            full_labels.extend(labels.tolist())

    val_f1 = f1_score(
        full_labels,
        full_preds,
        average='weighted',
        zero_division=0,
    )
    print(full_labels, full_preds)
    print(f"Test F1: {val_f1:4f}")
    print(classification_report(full_labels, full_preds, zero_division=0))
    assert val_f1 > 0.01
