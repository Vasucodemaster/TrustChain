import requests
import json

url = "http://127.0.0.1:8000/contributions/"

data = {
    "user_id": 1,
    "type": "code",

    "title": "Privacy-Preserving Federated Learning Framework",

    "description": (
        "Developed a federated learning framework that enables multiple "
        "clients to collaboratively train a machine learning model without "
        "sharing their raw data. The system uses FedAvg aggregation and "
        "differential privacy with gradient clipping and noise addition."
    ),

    "repository_url": "https://github.com/example/federated-learning",

    "source_url": "https://github.com/example/federated-learning",

    "code_text": """
import torch
from opacus import PrivacyEngine

def train_client(model, dataloader, optimizer, epochs=3):
    model.train()

    for epoch in range(epochs):
        for data, target in dataloader:
            optimizer.zero_grad()
            output = model(data)
            loss = torch.nn.functional.cross_entropy(output, target)
            loss.backward()
            optimizer.step()

    return model

def aggregate_models(client_models, weights):
    global_state = {}

    for key in client_models[0].state_dict():
        global_state[key] = sum(
            weights[i] * client_models[i].state_dict()[key]
            for i in range(len(client_models))
        )

    return global_state
""",

    "documentation_text": (
        "The framework consists of multiple clients and a central server. "
        "Each client trains locally and sends model updates instead of raw "
        "data. The server performs FedAvg aggregation. Differential privacy "
        "is applied using gradient clipping and calibrated noise. The system "
        "supports configurable training rounds, model evaluation, privacy "
        "parameters, and experiment logging."
    )
}

response = requests.post(url, json=data)

print("\n========== TRUSTCHAIN F4 TEST ==========")
print("HTTP Status:", response.status_code)

try:
    result = response.json()
    print(json.dumps(result, indent=2))

except Exception:
    print(response.text)
