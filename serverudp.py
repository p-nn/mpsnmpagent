import socket
import _thread
from time import sleep


class ServerUdp(object):
    ip: str = ''
    port: int = 161
    socket = None
    running = False
    bufferSize = 1024

    def __init__(self, local_ip="", local_port=161):
        self.ip = local_ip
        self.port = local_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.settimeout(0)
        self.socket.bind((local_ip, local_port))

    def start(self):
        if not self.running:
            _thread.start_new_thread(self.myThread, ())
            self.running = True

    def stop(self):
        if self.running:
            self.running = False

    def handle_udp(self, bytes):
        sleep(1)
        return None

    def myThread(self):
        print("start thread")
        while self.running:
            try:
                self.handle_udp(self.socket.recvfrom(self.bufferSize))
            except:
                pass
        print("stop thread")