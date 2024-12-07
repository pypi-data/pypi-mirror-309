from typing import List, Tuple
from remdex.host import ConnServer, ConnClient, Socket, connect_to, ClientResult
from threading import Event
from queue import Queue
from pprint import pprint
import sys
import os

globals()['dex_all_models'] = dict()

__dex_all_models__ = dict()

__auto_server_addr__:str = None

class DexError:
    BATCH_ENDED = 'BATCHENDEDBATCHENDED'


def add_gradient_weighted(grad1, grad2, w2):
    return [
        g1 + g2 * w2 for g1, g2 in zip(grad1, grad2)
    ]

def divide_gradients(gradients, divider):
    return [
        g / divider for g in gradients
    ]

def multiply_gradients(gradients, factor):
    return [
        g * factor for g in gradients
    ]


class Metric:
    def __init__(self, name:str, value, weight:float = 1.0) -> None:
        self.name = name
        self.value = value
        self.weight = weight

class Params:
    def __init__(self, params, weight: float = 1.0) -> None:
        self.params = params
        self.weight = weight

class Gradients:
    def __init__(self, gradients, weight: float = 1.0) -> None:
        self.gradients = gradients
        self.weight = weight

class Model:
    def __init__(self, model, name:str) -> None:
        self.model = model
        self.name = name

class FedAvgClient:

    def __setup_add__(self):
        self.__batched__ = False
        self.__server__: ConnServer
        self.__train_q__ = Queue()
        self.__batch_generator__ = None
        self.__batch_ended__ = True
        self.__batched__ = False
        self.__finish_event__ = Event()

    def __train__(self):
        self.train()
        self.__train_q__.put(0)

    def __get_params__(self): 
        self.__train_q__.get()
        if self.__batch_ended__ and self.__batched__:
            return DexError.BATCH_ENDED
        return self.get_params()
    
    def __batch_train__(self):
        try: 
            self.batch_train(next(self.__batch_generator__))
            self.__train_q__.put(0)
        except:
            self.__train_q__.put(0)
            self.__batch_ended__ = True

    def __batch_train_start__(self):
        self.__batched__ = True
        self.__batch_ended__ = False
        self.__batch_generator__ = self.batch_generator()

    def __finish__(self):
        self.__finish_event__.set()

    def __setup_user_methods__(self):
        self.__server__.add('train')(self.__train__) 
        self.__server__.add('get_params')(self.__get_params__)
        self.__server__.add('update_params')(self.update_params)
        self.__server__.add('batch_train')(self.__batch_train__)
        self.__server__.add('batch_train_start')(self.__batch_train_start__)
        self.__server__.add('evaluate')(self.evaluate)
        self.__server__.add('finish')(self.__finish__)
        self.__server__.add('return_models')(self.return_models)

    def __init__(self):
        pass

    def get_params(self,) -> List[Params]:
        pass

    def update_params(self, parameters: List[list]):
        pass

    def train(self, ):
        pass

    def batch_generator(self):
        pass

    def batch_train(self, batch):
        pass

    def save(self,):
        pass

    def evaluate(self,)->List[Metric]:
        pass

    def return_models(self, ) -> List[Model]:
        pass

    def start(self, server_address:str):

        assigned_address = server_address
        if server_address == 'auto':
            assigned_address = __auto_server_addr__

        self.__setup_add__()
        [address, port] = assigned_address.split(':') 
        port = int(port)
        # connect to server address 
        conn = connect_to(address=address, port=port)
        server = ConnServer(sock=conn)
        self.__server__ = server 
        self.__setup_user_methods__()
        self.__finish_event__.wait()


class FedSgdClient:

    def __setup_add__(self):
        self.__batched__ = False
        self.__server__: ConnServer
        self.__gradient_q__ = Queue()
        self.__all_gradients__ = [] 
        self.__batch_data_generator__ = None
        self.__finish_event__ = Event()

    def __get_latest_gradients__(self):
        self.__gradient_q__.get()
        return self.__all_gradients__.pop(0)
    
    def __train__(self):
        #print('trained') 
        self.__all_gradients__.append(self.train())
        self.__gradient_q__.put(0)
        

    def __batch_train_start__(self):
        self.__batch_data_generator__ = self.batch_generator()

    def __batch_train__(self):
        try:
            self.__all_gradients__.append(
                self.batch_train(
                    next(self.__batch_data_generator__)
                )
            )   
            self.__gradient_q__.put(0)
        except:
            self.__all_gradients__.append(DexError.BATCH_ENDED)
            self.__gradient_q__.put(0)

    def __finish__(self):
        self.__finish_event__.set()

    def __setup_user_methods__(self):
        self.__server__.add('train')(self.__train__)
        self.__server__.add('init_parameters')(self.init_parameters)
        self.__server__.add('optimize')(self.optimize)
        self.__server__.add('batch_train')(self.__batch_train__)
        self.__server__.add('get_gradients')(self.__get_latest_gradients__)
        self.__server__.add('batch_train_start')(self.__batch_train_start__)
        self.__server__.add('evaluate')(self.evaluate)
        self.__server__.add('finish')(self.__finish__)
        self.__server__.add('return_models')(self.return_models)

    def __init__(self):
        pass

    def train(self)->List[Gradients]:
        pass
    
    def init_parameters(self, parameters:List[list]):
        pass
    
    def optimize(self, gradients: List[list]):
        pass

    def batch_generator(self):
        pass

    def batch_train(self, batch)->List[Gradients]:
        pass

    def return_models(self, ) -> List[Model]:
        pass

    def evaluate(self,)->List[Metric]:
        pass

    def start(self, server_address:str):
        assigned_address = server_address
        if server_address=='auto':
            assigned_address = __auto_server_addr__
        self.__setup_add__()
        [address, port] = assigned_address.split(':') 
        port = int(port)
        # connect to server address 
        conn = connect_to(address=address, port=port)
        server = ConnServer(sock=conn)
        self.__server__ = server 
        self.__setup_user_methods__()
        self.__finish_event__.wait()

def init_parameters(
    client:ConnClient, 
    parameters: List[list]
):
    return client.call('init_parameters').run(
        parameters = parameters
    )

def save_model(model:Model):
    try:
        model.model.save(model.name)
    except:
        import torch
        torch.save(model.model.state_dict(), f'{model.name}.pth')

def return_models(clients:List[ConnClient], ):
    models: List[Model] = clients[0].call('return_models').run().get()
    if models is None: return
    # save the models
    for m in models:
        save_model(m)
        

def finish_clients(clients: List[ConnClient]):
    r = [c.call('finish').run() for c in clients]

def get_summed_gradients(clients: List[ConnClient]):
    # get latest gradients
    weights = []
    grads = None
    for c in clients:
        recv_grads: List[Gradients] = c.call('get_gradients').run().get()
        # skip if none
        if recv_grads == DexError.BATCH_ENDED:
            continue
        if grads == None:
            grads = []
            for idx, rg in enumerate(recv_grads, 0):
                weights.insert(idx, rg.weight)
                grads.insert(idx,multiply_gradients(rg.gradients, rg.weight))
            continue
        # normal situation
        for idx, rg in enumerate(recv_grads, 0):
            weights[idx] += rg.weight
            grads[idx] = add_gradient_weighted(grads[idx], rg.gradients, rg.weight)

    return weights, grads

def sgd_optimize(grads:List[list], clients: List[ConnClient]):
    for c in clients:
        c.call('optimize').run(grads).get()

def sgd_step_update(clients: List[ConnClient]):
    # get gradients
    weights, grads = get_summed_gradients(clients)
    # check if nothing is received
    if grads is None:
        return False
    # get average gradients
    avg_grads = []
    for w, g in zip(weights, grads):
        avg_grads.append(divide_gradients(g, w))
    # optimize
    sgd_optimize(avg_grads, clients)
    return True

def sgd_step(clients: List[ConnClient]):
    # train
    train_requests = [
        c.call('train').run() for c in clients
    ]
    sgd_step_update(clients=clients)

def batch_sgd_step(clients: List[ConnClient], epoch:int, epochs:int):
    # start training first 
    start_requests = [c.call('batch_train_start').run() for c in clients]
    [s.get() for s in start_requests]
    can_continue = True
    batch_position = 1
    # run steps 
    while can_continue:
        train_requests = [
            c.call('batch_train').run() for c in clients
        ]
        [t.get() for t in train_requests]
        can_continue = sgd_step_update(clients)
        # evaluate model
        if can_continue:
            evals = get_eval(clients)
            if evals is not None:
                print(f'Epoch {epoch}/{epochs} Batch:{batch_position}')
                pprint(evals)
                print()
        batch_position+=1


def retrieve_models(clients:List[ConnClient]):
    models_map = dict()
    for c in clients:
        models: List[Model] = c.call('return_models').run().get()
        for m in models:
            models_map[m.name] = m.model
    for name, model in models_map.items():
       __dex_all_models__[name] = model
    

    
def train_sgd(
    clients: List[ConnClient],
    epochs: int, 
    batched: bool = False,
    parameters: List[list] = None,
):
    # init parameters 
    if parameters is not None:
        init_requests: List[ClientResult] = [init_parameters(i, parameters) for i in clients]
        [i.get() for i in init_requests]
    # start training
    for i in range(1, epochs+1):
        if batched:
            #print('batched')
            batch_sgd_step(clients, i, epochs)
        else:
            #print('not batched')
            sgd_step(clients)
            evals = get_eval(clients)
            if evals is not None:
                print(f'Epoch {i}/{epochs}')
                pprint(evals)
                print()
    retrieve_models(clients=clients)
    finish_clients(clients=clients)


def get_summed_params(clients: List[ConnClient]):
    # get latest paramms
    weights = []
    params = None
    for c in clients:
        recv_params: List[Params] = c.call('get_params').run().get()
        # skip if none
        if recv_params == DexError.BATCH_ENDED:
            continue
        if params == None:
            params = []
            for idx, rg in enumerate(recv_params, 0):
                weights.insert(idx, rg.weight)
                params.insert(idx,multiply_gradients(rg.params, rg.weight))
            continue
        # normal situation
        for idx, rg in enumerate(recv_params, 0):
            weights[idx] += rg.weight
            params[idx] = add_gradient_weighted(params[idx], rg.params, rg.weight)

    return weights, params


def avg_update_params(params, clients: List[ConnClient]):
    for c in clients:
        c.call('update_params').run(params).get()

def avg_step_update(clients: List[ConnClient]):
    # get parameters
    weights, params = get_summed_params(clients)
    # check if nothing is received
    if params is None:
        return False
    # get average parameters
    avg_params = []
    for w, g in zip(weights, params):
        avg_params.append(divide_gradients(g, w))
    # optimize
    avg_update_params(avg_params, clients)
    return True

def avg_step(clients: List[ConnClient]):
    # train
    trains = [ c.call('train').run() for c in clients]
    [t.get() for t in trains]
    
    avg_step_update(clients)

def batch_avg_step(clients: List[ConnClient], epoch:int, epochs:int):
    starts = [c.call('batch_train_start').run() for c in clients]
    [s.get() for s in starts]
    can_continue = True
    batch_position = 1
    while can_continue:
        trains = [ c.call('batch_train').run() for c in clients]
        [t.get() for t in trains]
        can_continue = avg_step_update(clients=clients)
        # evaluate model
        if can_continue:
            evals = get_eval(clients)
            if evals is not None:
                print(f'Epoch {epoch}/{epochs} Batch:{batch_position}')
                pprint(evals)
                print()
        batch_position+=1


def compute_eval(evals:List[Metric]):
    values = dict()
    weights = dict()
    for i in evals:
        if i is None:continue
        for e in i:
            try:
                values[e.name] += e.value * e.weight
                weights[e.name] += e.weight
            except:
                values[e.name] = e.value * e.weight
                weights[e.name] = e.weight

    for k in values.keys():
        values[k] = values[k] / weights[k]

    if len([k for k in values.keys()]) == 0:
        return None
    
    return values
            

def get_eval(clients: List[ConnClient]):
    evals = [c.call('evaluate').run() for c in clients]
    evals = [ e.get() for e in evals ]
    evals:List[Metric] = evals
    computed_eval = compute_eval(evals=evals)
    if computed_eval is None:
        return 
    return computed_eval

    
def train_avg(
    clients: List[ConnClient],
    epochs: int, 
    batched: bool = False,
    parameters: List[list] = None,
):
    if parameters is not None:
        init_requests: List[ClientResult] = [init_parameters(i, parameters) for i in clients]
        [i.get() for i in init_requests]
    # start training
    for i in range(1,epochs+1):
        if batched:
            #print('batched')
            batch_avg_step(clients, epoch=i, epochs=epochs)
        else:
            #print('not batched')
            avg_step(clients)
            evals = get_eval(clients)
            if evals is not None:
                print(f'Epoch {i}/{epochs}')
                pprint(evals)
                print()
    retrieve_models(clients=clients)
    finish_clients(clients=clients)

class FedAvgServer:

    def __init__(
        self, address:str, epochs:int, 
        num_clients:int, batched=False, 
        init_params: List[list]=None
    ) -> None:
        
        assigned_address = address

        if address == 'auto':
            assigned_address = __auto_server_addr__

        self.address = assigned_address
        self.epochs = epochs
        self.batched = batched
        self.num_clients = num_clients
        [self.ip, port] = self.address.split(':')
        self.port = int(port)
        self.init_params = init_params

    def start(self, ):
        sock = Socket(address=self.ip, port=self.port)
        clients = [ConnClient(sock.get_incoming()) for i in range(self.num_clients)]
        train_avg(
            clients=clients,
            epochs=self.epochs, 
            batched=self.batched,
            parameters=self.init_params
        )


class FedSgdServer(FedAvgServer):
    def __init__(self, address: str, epochs: int, 
                 num_clients: int, batched=False, 
                 init_params: List[List] = None
        ) -> None:
        super().__init__(address, epochs, num_clients, batched, init_params)

    def start(self):
        sock = Socket(address=self.ip, port=self.port)
        clients = [ConnClient(sock.get_incoming()) for i in range(self.num_clients)]
        train_sgd(
            clients=clients,
            epochs=self.epochs, 
            batched=self.batched,
            parameters=self.init_params
        )


