import torch
import torch.nn as nn
from torchvision.models import resnet50
from torchvision.models import ResNet50_Weights
import torch.optim as optim
from sklearn.metrics import f1_score

from dataloader import init_loader

NUM_CLASSES = 6
EPOCHS = 2
BATCH_SIZE = 32
IMG_SIZE = 232


def init_model():
    model = resnet50(weights=ResNet50_Weights.DEFAULT)
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, NUM_CLASSES)
    return model


if __name__ == "__main__":
    device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
    print(f"Device: {device}")
    train_data, train_loader = init_loader('train', BATCH_SIZE, IMG_SIZE)
    print("Train samples:", len(train_data))
    val_data, val_loader = init_loader('val', BATCH_SIZE, IMG_SIZE)
    print("Validation samples:", len(val_data))

    model = init_model().to(device)

    criterion = nn.CrossEntropyLoss()
    optimizer = optim.SGD(model.parameters(), lr=0.001, momentum=0.9)

    best_f1 = 0
    for epoch in range(EPOCHS):
        model.train()
        train_loss = 0
        for inputs, labels in train_loader:
            inputs, labels = inputs.to(device), labels.to(device)
            optimizer.zero_grad()
            outputs = model(inputs)
            loss = criterion(outputs, labels)
            loss.backward()
            optimizer.step()
            train_loss += loss.item() * inputs.size(0)

        model.eval()

        val_loss = 0
        full_preds = []
        full_labels = []
        with torch.no_grad():
            for inputs, labels in val_loader:
                inputs, labels = inputs.to(device), labels.to(device)
                outputs = model(inputs)
                loss = criterion(outputs, labels)
                val_loss += loss.item() * inputs.size(0)
                _, preds = torch.max(outputs, 1)
                full_preds.extend(preds.tolist())
                full_labels.extend(labels.tolist())

        train_loss /= len(train_data)
        val_loss /= len(val_data)
        val_f1 = f1_score(full_labels, full_preds, average='weighted')
        print(f"Epoch [{epoch + 1}/{EPOCHS}] Train Loss: {train_loss:.4f}",
              f"Val Loss: {val_loss:.4f} Val F1: {val_f1:.4f}")

        # Save the model
        if val_f1 > best_f1:
            best_f1 = val_f1
            torch.save(model, '../models/model.pt', )
