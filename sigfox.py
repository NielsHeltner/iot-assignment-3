from network import WLAN
from network import Sigfox
import machine
import socket
import binascii
from ltr329als01 import LTR329ALS01


sigfox = Sigfox(mode=Sigfox.SIGFOX, rcz=Sigfox.RCZ1)
s = socket.socket(socket.AF_SIGFOX, socket.SOCK_RAW)

s.setblocking(True)

s.setsockopt(socket.SOL_SIGFOX, socket.SO_RX, False)
s.send("lol")