import unittest

from ml.federated_learning.model import create_model
from ml.federated_learning.data import create_institution_data
from ml.federated_learning.server import create_strategy


class TestF1FederatedLearning(unittest.TestCase):

    def test_model_output_shape(self):
        import torch

        model = create_model()
        x, _ = create_institution_data(1)
        output = model(x)

        self.assertEqual(tuple(x.shape), (5, 6))
        self.assertEqual(tuple(output.shape), (5, 1))

    def test_data_for_multiple_institutions(self):
        import torch

        for institution_id in (1, 2, 3):
            x, y = create_institution_data(institution_id)
            self.assertEqual(tuple(x.shape), (5, 6))
            self.assertEqual(tuple(y.shape), (5, 1))
            self.assertTrue(torch.isfinite(x).all())
            self.assertTrue(torch.isfinite(y).all())

    def test_fedavg_strategy(self):
        strategy = create_strategy()

        self.assertEqual(type(strategy).__name__, "FedAvg")
        self.assertGreaterEqual(strategy.min_fit_clients, 2)
        self.assertGreaterEqual(strategy.min_evaluate_clients, 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)

    def test_weighted_average_loss(self):
        from ml.federated_learning.server import weighted_average

        result = weighted_average([
            (2, {"loss": 0.2}),
            (6, {"loss": 0.6}),
        ])

        expected = (2 * 0.2 + 6 * 0.6) / 8
        self.assertAlmostEqual(result["loss"], expected)

    def test_weighted_average_single_client(self):
        from ml.federated_learning.server import weighted_average

        result = weighted_average([(5, {"loss": 0.4})])
        self.assertAlmostEqual(result["loss"], 0.4)
