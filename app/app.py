import os
import time
import torch
import torch.nn as nn
import streamlit as st
from torchvision.models import resnet50
from torchvision import transforms
from PIL import Image

IMG_SIZE = 232
model_path = '/app/models/model.pt'

classes = {
    0: 'Cardboard',
    1: 'Glass',
    2: 'Metal',
    3: 'Paper',
    4: 'Plastic',
    5: 'Trash'
}


def init_model():
    model = resnet50()
    num_features = model.fc.in_features
    model.fc = nn.Linear(num_features, len(classes))

    # Wait for the model to train
    while not os.path.exists(model_path):
        time.sleep(2)
    time.sleep(2)

    # Load the model
    model.load_state_dict(torch.load(
        model_path,
        map_location=torch.device('cpu')))
    return model


def preprocess_image(image):
    data_transform = transforms.Compose([
        transforms.Resize((IMG_SIZE, IMG_SIZE)),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(
            mean=[0.485, 0.456, 0.406],
            std=[0.229, 0.224, 0.225]
        )
    ])

    return data_transform(image)


def predict(model, image):
    input = preprocess_image(Image.open(image))
    model.eval()
    output = model(torch.unsqueeze(input, dim=0))
    softmax = nn.Softmax(dim=1)
    probs = softmax(output)
    predictions = {}
    for index, name in classes.items():
        probability = probs[:, index].item()
        predictions[name] = probability
    return predictions


st.title("Garbage recognition")

file = st.file_uploader(
    "Choose an image...",
    type=['jpg', 'png']
)

if file:
    # Predict
    model = init_model()
    predictions = predict(model, file)
    st.write(predictions)
    st.image(file, use_column_width=True)
