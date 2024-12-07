from typing import NamedTuple


class ControllerConfig(NamedTuple):
    controller_id: str
    address: int
    i2c_port: int


state_controllers = [
    ControllerConfig(
        controller_id="state1",
        address=0x20,
        i2c_port=1,
    ),
    ControllerConfig(
        controller_id="state2",
        address=0x21,
        i2c_port=1,
    ),
]

actuator_controllers = [
    ControllerConfig(
        controller_id="act1",
        address=0x22,
        i2c_port=1,
    ),
    ControllerConfig(
        controller_id="act2",
        address=0x23,
        i2c_port=1,
    ),
]


class BayConfig(NamedTuple):
    id: str
    state_controller_id: str
    state_controller_address_controller_register: int
    state_controller_address_register_bit_mask: int
    actuator_controller_id: str
    actuator_controller_address_controller_register: int
    actuator_controller_address_register_bit_mask: int
    width: float


bays = [
    BayConfig("5A", "state1", 0x01, 0b00001000, "act1", 0x01, 0b00001000, 160),
    BayConfig("4A", "state1", 0x01, 0b00010000, "act1", 0x01, 0b00010000, 110),
    BayConfig("3A", "state1", 0x01, 0b00100000, "act1", 0x01, 0b00100000, 150),
    BayConfig("2A", "state1", 0x01, 0b01000000, "act1", 0x01, 0b01000000, 110),
    BayConfig("1A", "state1", 0x01, 0b10000000, "act1", 0x01, 0b10000000, 110),
    BayConfig("6B", "state1", 0x00, 0b00100000, "act1", 0x00, 0b00100000, 140),
    BayConfig("5B", "state1", 0x00, 0b01000000, "act1", 0x00, 0b01000000, 100),
    BayConfig("4B", "state1", 0x00, 0b10000000, "act1", 0x00, 0b10000000, 90),
    BayConfig("3B", "state1", 0x01, 0b00000001, "act1", 0x01, 0b00000001, 80),
    BayConfig("2B", "state1", 0x01, 0b00000010, "act1", 0x01, 0b00000010, 90),
    BayConfig("1B", "state1", 0x01, 0b00000100, "act1", 0x01, 0b00000100, 140),
    BayConfig("7C", "state2", 0x00, 0b00000001, "act2", 0x00, 0b00000001, 190),
    BayConfig("6C", "state1", 0x00, 0b00000001, "act1", 0x00, 0b00000001, 110),
    BayConfig("5C", "state1", 0x00, 0b00000010, "act1", 0x00, 0b00000010, 90),
    BayConfig("4C", "state1", 0x00, 0b00000100, "act1", 0x00, 0b00000100, 80),
    BayConfig("3C", "", 0x00, 0b00000000, "", 0x00, 0b00000000, 90),
    BayConfig("2C", "state1", 0x00, 0b00001000, "act1", 0x00, 0b00001000, 80),
    BayConfig("1C", "state1", 0x00, 0b00010000, "act1", 0x00, 0b00010000, 80),
    BayConfig("7D", "state2", 0x00, 0b10000000, "act2", 0x00, 0b10000000, 120),
    BayConfig("6D", "state2", 0x00, 0b01000000, "act2", 0x00, 0b01000000, 140),
    BayConfig("5D", "state2", 0x00, 0b00100000, "act2", 0x00, 0b00100000, 120),
    BayConfig("4D", "state2", 0x00, 0b00010000, "act2", 0x00, 0b00010000, 80),
    BayConfig("3D", "state2", 0x00, 0b00001000, "act2", 0x00, 0b00001000, 90),
    BayConfig("2D", "state2", 0x00, 0b00000100, "act2", 0x00, 0b00000100, 80),
    BayConfig("1D", "state2", 0x00, 0b00000010, "act2", 0x00, 0b00000010, 80),
]
