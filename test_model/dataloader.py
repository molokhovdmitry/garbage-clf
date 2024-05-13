import os
import torch
from torchvision import datasets, transforms


def init_loader(split, batch_size, img_size):
    data_transform = transforms.Compose([
        transforms.Resize((img_size, img_size)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])
    data_path = "../data/processed/kaggle"
    dataset = datasets.ImageFolder(
        root=os.path.join(data_path, split),
        transform=data_transform
    )

    data_loader = torch.utils.data.DataLoader(
        dataset,
        batch_size=batch_size
    )

    return dataset, data_loader
