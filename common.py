import enum


class PacketTypes(enum.Enum):
    DISCONNECT = -1
    IDLE = 0
    MOVING = 1
