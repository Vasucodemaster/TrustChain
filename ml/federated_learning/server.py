import flwr as fl

from ml.federated_learning.model import create_model


def weighted_average(metrics):
    total_examples = sum(
        num_examples
        for num_examples, _ in metrics
    )

    weighted_loss = sum(
        num_examples * metric["loss"]
        for num_examples, metric in metrics
    )

    return {
        "loss": weighted_loss / total_examples
    }


def create_strategy():

    model = create_model()

    initial_parameters = fl.common.ndarrays_to_parameters(
        [
            parameter.detach().cpu().numpy()
            for parameter in model.parameters()
        ]
    )

    strategy = fl.server.strategy.FedAvg(
        fraction_fit=1.0,
        fraction_evaluate=1.0,
        min_fit_clients=2,
        min_evaluate_clients=2,
        min_available_clients=2,
        initial_parameters=initial_parameters,
        fit_metrics_aggregation_fn=weighted_average
    )

    return strategy


def start_server():

    strategy = create_strategy()

    fl.server.start_server(
        server_address="127.0.0.1:8080",
        config=fl.server.ServerConfig(
            num_rounds=3
        ),
        strategy=strategy
    )


if __name__ == "__main__":
    start_server()
