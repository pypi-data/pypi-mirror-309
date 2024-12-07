from typing import List, Tuple
import remdex.framework as framework

class Metric(framework.Metric):
    def __init__(self, name: str, value, weight: float = 1) -> None:
        super().__init__(name, value, weight)

class Params(framework.Params):
    def __init__(self, params, weight: float = 1) -> None:
        super().__init__(params, weight)

class Gradients(framework.Gradients):
    def __init__(self, gradients, weight: float = 1) -> None:
        super().__init__(gradients, weight)

class FedAvgClient(framework.FedAvgClient):
    def __init__(self):
        super().__init__()
    def train(self):
        return super().train()
    def batch_generator(self):
        return super().batch_generator()
    def batch_train(self, batch):
        return super().batch_train(batch)
    def evaluate(self) -> List[framework.Metric]:
        return super().evaluate()
    def get_params(self) -> List[framework.Params]:
        return super().get_params()
    def update_params(self, parameters: List[List]):
        return super().update_params(parameters)
    def save(self):
        return super().save()
    def start(self, server_address: str):
        return super().start(server_address)


class FedSgdClient(framework.FedSgdClient):
    def __init__(self):
        super().__init__()
    def train(self) -> List[framework.Gradients]:
        return super().train()
    def optimize(self, gradients: List[List]):
        return super().optimize(gradients)
    def batch_generator(self):
        return super().batch_generator()
    def batch_train(self, batch) -> List[framework.Gradients]:
        return super().batch_train(batch)
    def evaluate(self) -> List[framework.Metric]:
        return super().evaluate()
    def save(self):
        return super().save()
    
class FedAvgServer(framework.FedAvgServer):
    def __init__(self, address: str, epochs: int, num_clients: int, batched=False, init_params: List[List] = None) -> None:
        super().__init__(address, epochs, num_clients, batched, init_params)
    def start(self):
        return super().start()
    
class FedSgdServer(framework.FedSgdServer):
    def __init__(self, address: str, epochs: int, num_clients: int, batched=False, init_params: List[List] = None) -> None:
        super().__init__(address, epochs, num_clients, batched, init_params)
    def start(self):
        return super().start()

