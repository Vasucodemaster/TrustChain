import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from opacus import PrivacyEngine

from ml.federated_learning.model import create_model


def train_private_model(x, y, epochs=5):
    model = create_model()

    dataset = TensorDataset(x, y)
    loader = DataLoader(
        dataset,
        batch_size=2,
        shuffle=True
    )

    optimizer = torch.optim.Adam(
        model.parameters(),
        lr=0.001
    )

    loss_function = nn.MSELoss()

    privacy_engine = PrivacyEngine()

    model, optimizer, loader = privacy_engine.make_private(
        module=model,
        optimizer=optimizer,
        data_loader=loader,
        noise_multiplier=1.0,
        max_grad_norm=1.0
    )

    model.train()

    for epoch in range(epochs):
        total_loss = 0.0

        for batch_x, batch_y in loader:
            optimizer.zero_grad()

            prediction = model(batch_x)
            loss = loss_function(prediction, batch_y)

            loss.backward()
            optimizer.step()

            total_loss += loss.item()

    epsilon = privacy_engine.get_epsilon(delta=1e-5)

    return model, epsilon, total_loss
