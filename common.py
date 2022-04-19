from dataclasses import dataclass
from enum import Enum
import typing

WINDOW_SIZE = (500, 500)
FPS = float("inf")
SERVER_ADDRESS = ("127.0.0.1", 20000)  # Address of the server we will be connecting to
PACKET_SIZE = 512


class PacketType(Enum):
    DISCONNECT = -1
    IDLE = 0
    MOVING = 1


class PacketPriority(Enum):
    DROPPABLE = 0
    PRIORITY = 1


@dataclass
class Packet:
    priority: PacketPriority
    type: PacketType
    data: typing.Any
