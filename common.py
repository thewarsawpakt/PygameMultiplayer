from dataclasses import dataclass
from enum import Enum


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
    data: bytes

