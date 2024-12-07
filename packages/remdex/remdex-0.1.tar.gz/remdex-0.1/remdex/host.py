from remdex.connect import ReceiverSide, SenderSide, Message, SentMessage
import socket
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import cloudpickle

class Socket:
    def __init__(self, address:str, port:int) -> None:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.bind((address, port))
        sock.listen(0)
        self.sock = sock
    def get_incoming(self):
        conn, _ = self.sock.accept()
        return conn

def connect_to(address:str, port:int):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((address, port))
    return sock 

class ConnServer:

    def __setup_add__(self):
        self._processors = dict()
        self._pool = ThreadPoolExecutor()

    def _process_single(self, message:Message):
        (fn_id, args, kwargs) = cloudpickle.loads(message.data)
        try:
            message.reply(
                data=cloudpickle.dumps(self._processors[fn_id](*args, **kwargs))
            )
        except Exception as e:
            print(fn_id)
            print(e)
        
    def _processing(self):
        while True:
            self._pool.submit(self._process_single, self._receiver.recv())
            
    def __init__(self, sock:socket.socket) -> None:
        self.__setup_add__()
        self._receiver = ReceiverSide(sock=sock)
        Thread(target=self._processing, daemon=True).start()

    def add(self, name:str):
        def __wrapper__(fn):
            self._processors[name] = fn
        return __wrapper__


class ClientResult:

    def __init__(self, sent_message:SentMessage) -> None:
        self._sent_message = sent_message

    def get(self):
        return cloudpickle.loads(self._sent_message.get())


class ClientFn:

    def __init__(self, name:str, sender:SenderSide) -> None:
        self.name = name
        self._sender = sender

    def run(self, *args, **kwargs):
        return ClientResult(
            sent_message=self._sender.send(
                cloudpickle.dumps((self.name, args, kwargs))
            )
        )

class ConnClient: 
    def __init__(self, sock:socket.socket, index=0) -> None:
        self._sender = SenderSide(sock=sock, index=index)
    def call(self, name:str):
        return ClientFn(name=name, sender=self._sender)
