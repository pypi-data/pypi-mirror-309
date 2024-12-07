import socket
from threading import Event, Thread, Lock
import random
from typing import Dict, List


data_content_del = b'mitdatalier'
DATA_SIZE_LENGTH = 32
DATA_ID_LENGTH = 20

def random_id() -> bytes:
    gen = lambda : random.randint(1000,2000)
    return f'{gen()}-{gen()}-{gen()}'.encode().zfill(DATA_ID_LENGTH)

def recv_size(sock:socket.socket, size: int):
    data_sets = []
    cur_size = 0
    while cur_size<size:
        data_sets.append(sock.recv(size-cur_size))
        cur_size+= len(data_sets[-1])
    return b''.join(data_sets)
    
def recv_data_seg(sock:socket.socket):
    return recv_size(
        sock=sock, 
        size=int.from_bytes(sock.recv(DATA_SIZE_LENGTH), 'big')
    )

#def prep_before_send(data:bytes):
    

def breakdown_id(data:bytes):
    [data_id, content] = data.split(data_content_del)
    return data_id, content

    
class Message:
    def __init__(self, data:bytes, reply_fn:callable) -> None:
        self.id, self.data = breakdown_id(data)
        self.reply_fn = reply_fn # the ConnHandler._reply()
    def reply(self, data:bytes):
        self.reply_fn(self.id, data)

# create socket to process data requests and replies
class ReceiverSide:

    def __setup_add__(self):
        self.reply_event = Event()
        self.replied_data: List[bytes] = [] # contains fully prepared data
        self.recv_lock = Lock()

    def _replying(self, ):
        while True: 
            self.reply_event.wait()
            self.reply_event.clear()
            replied_len = len(self.replied_data)
            if replied_len==0:
                continue
            self.sock.sendall(b''.join(self.replied_data[:replied_len]))
            self.replied_data[:replied_len] = []

    def __init__(self, sock:socket.socket) -> None:
        self.sock = sock
        self.__setup_add__()
        Thread(target=self._replying, daemon=True).start()

    def _data_processing(self, data: bytes):
        return len(data).to_bytes(DATA_SIZE_LENGTH, 'big') + data
    
    def _reply(self, data_id:bytes, data:bytes):
        # all data processing comes here
        self.replied_data.append(
            self._data_processing(data_id+data_content_del+data)
        )
        self.reply_event.set()

    def recv(self):
        with self.recv_lock:
            return Message(
                data=recv_data_seg(sock=self.sock),
                reply_fn=self._reply
            )
    
# the sending end

class SentMessage: 
    def __init__(self, data_id:bytes, get_fn) -> None:
        self.id = data_id
        self.get_fn = get_fn
        self.data = None
    def get(self, )->bytes:
        if self.data is not None:
            return self.data
        return self.get_fn(self.id)

class SenderSide:

    def __setup_add__(self):
        self.send_event = Event()
        self.sent_data: List[bytes] = [] # contains fully prepared data
        self.result_store: Dict[bytes, bytes] = dict()
        self.recv_lock = Lock()
        self.read_lock = Lock()

    def _sending(self,):
        while True: 
            self.send_event.wait()
            self.send_event.clear()
            sent_len = len(self.sent_data)
            if sent_len==0:
                continue
            self.sock.sendall(b''.join(self.sent_data[:sent_len]))
            self.sent_data[:sent_len] = []
            #print(f"sent:{self.index}")

    def _recv_once(self,):
        with self.recv_lock:
            recv_data_id, recv_data = breakdown_id(
                    data=recv_data_seg(self.sock)
                )
            self.result_store[recv_data_id] = recv_data
                

    def _get_reply(self, data_id:bytes):
        while True:
            with self.read_lock:
                if data_id in self.result_store:
                    data = self.result_store[data_id]
                    del self.result_store[data_id]
                    return data
            self._recv_once()

    def __init__(self, sock:socket.socket, index=0) -> None:
        self.sock = sock
        self.index = index
        #print(f'index:{self.index}')
        self.__setup_add__()
        Thread(target=self._sending, daemon=True).start()
        

    def _data_processing(self, data:bytes):
        data_id = random_id()
        cur_data = data_id+data_content_del+data
        return data_id, len(cur_data).to_bytes(DATA_SIZE_LENGTH, 'big')+cur_data

    def send(self, data:bytes):
        data_id, cur_data = self._data_processing(data)
        self.sent_data.append(cur_data)
        self.send_event.set()
        return SentMessage(data_id=data_id,get_fn=self._get_reply)

    