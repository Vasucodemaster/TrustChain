import torch
import torch.nn as nn
import flwr as fl

from opacus import PrivacyEngine

from ml.federated_learning.model import create_model
from ml.federated_learning.data import create_institution_data


class ReputationClient(fl.client.NumPyClient):

    def __init__(self, institution_id):
        self.institution_id = institution_id

        self.model = create_model()

        self.x_train, self.y_train = create_institution_data(
            institution_id
        )

        # Normalize local features and targets for stable DP training.
        self.x_train = self.x_train / 100.0
        self.y_train = self.y_train / 100.0
    def get_parameters(self, config):
        return [
            parameter.detach().cpu().numpy()
            for parameter in self.model.parameters()
        ]

    def set_parameters(self, parameters):

        state_dict = self.model.state_dict()

        new_state_dict = {}

        for (key, old_parameter), new_parameter in zip(
            state_dict.items(),
            parameters
        ):
            new_state_dict[key] = torch.tensor(
                new_parameter,
                dtype=old_parameter.dtype
            )

        self.model.load_state_dict(
            new_state_dict,
            strict=True
        )

    def fit(self, parameters, config):

        # Create a fresh model for every federated round.
        # This prevents Opacus from attaching hooks twice.
        model = create_model()

        state_dict = model.state_dict()

        new_state_dict = {}

        for (key, old_parameter), new_parameter in zip(
            state_dict.items(),
            parameters
        ):
            new_state_dict[key] = torch.tensor(
                new_parameter,
                dtype=old_parameter.dtype
            )

        model.load_state_dict(
            new_state_dict,
            strict=True
        )

        model.train()

        dataset = torch.utils.data.TensorDataset(
            self.x_train,
            self.y_train
        )

        loader = torch.utils.data.DataLoader(
            dataset,
            batch_size=2,
            shuffle=True
        )

        optimizer = torch.optim.Adam(
            model.parameters(),
            lr=0.0005
        )

        loss_function = nn.MSELoss()

        privacy_engine = PrivacyEngine()

        private_model, private_optimizer, private_loader = (
            privacy_engine.make_private(
                module=model,
                optimizer=optimizer,
                data_loader=loader,
                noise_multiplier=1.0,
                max_grad_norm=1.0
            )
        )

        epochs = int(config.get("epochs", 5))

        for _ in range(epochs):

            for batch_x, batch_y in private_loader:

                private_optimizer.zero_grad()

                prediction = private_model(batch_x)

                loss = loss_function(
                    prediction,
                    batch_y
                )

                loss.backward()

                private_optimizer.step()

        epsilon = privacy_engine.get_epsilon(
            delta=1e-5
        )

        # Store the clean underlying model for Flower.
        self.model = private_model._module

        return (
            self.get_parameters(config),
            len(self.x_train),
            {
                "institution": self.institution_id,
                "loss": float(loss.item()),
                "epsilon": float(epsilon)
            }
        )

    def evaluate(self, parameters, config):

        self.set_parameters(parameters)

        self.model.eval()

        with torch.no_grad():

            prediction = self.model(self.x_train)

            loss = nn.MSELoss()(
                prediction,
                self.y_train
            )

        return (
            float(loss.item()),
            len(self.x_train),
            {
                "institution": self.institution_id
            }
        )


def start_client(institution_id):

    client = ReputationClient(institution_id)

    fl.client.start_client(
        server_address="127.0.0.1:8080",
        client=client.to_client(),
        insecure=True
    )


if __name__ == "__main__":

    institution_id = 1

    start_client(institution_id)
