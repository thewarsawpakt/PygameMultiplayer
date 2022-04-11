from dataclasses import dataclass


@dataclass
class PacketType:
    DISCONNECT = -1
    IDLE = 0
    MOVING = 1


@dataclass
class PacketPriority:
    DROPPABLE = 0
    PRIORITY = 1


@dataclass
class Packet:
    priority: PacketPriority
    type_: PacketType
    data: bytes

