from typing import Dict

from devctl.bay.controller import StateController, ActuatorController, Address
from devctl import config


class Bay:
    bay_id: str
    state_controller: StateController
    state_controller_address: Address
    actuator_controller: ActuatorController
    actuator_controller_address: Address

    def __init__(
        self,
        bay_id: str,
        state_controller: StateController,
        state_controller_address: Address,
        actuator_controller: ActuatorController,
        actuator_controller_address: Address,
    ):
        self.bay_id = bay_id
        self.state_controller = state_controller
        self.state_controller_address = state_controller_address
        self.actuator_controller = actuator_controller
        self.actuator_controller_address = actuator_controller_address


class Station:
    """Station which contains all bays, controller and card readers."""

    def __init__(self):
        """Initialize station from station config."""

        assert len({c.controller_id for c in config.state_controllers}) == len(
            config.state_controllers
        ), "Duplicate state controller ids in config"
        assert len({c.controller_id for c in config.actuator_controllers}) == len(
            config.actuator_controllers
        ), "Duplicate actuator controller ids in config"
        assert len({c.id for c in config.bays}) == len(
            config.bays
        ), "Duplicate bay ids in config"

        self.state_controllers: Dict[str, StateController] = {
            state_controller_config.controller_id: StateController(
                state_controller_config
            )
            for state_controller_config in config.state_controllers
        }
        self.actuator_controllers: Dict[str, ActuatorController] = {
            actuator_controller_config.controller_id: ActuatorController(
                actuator_controller_config
            )
            for actuator_controller_config in config.actuator_controllers
        }
        self.bays: Dict[str, Bay] = {
            bay_config.id: Bay(
                bay_id=bay_config.id,
                state_controller=self.state_controllers[bay_config.state_controller_id],
                state_controller_address=Address(
                    controller_register=bay_config.state_controller_address_controller_register,
                    register_bit_mask=bay_config.state_controller_address_register_bit_mask,
                ),
                actuator_controller=self.actuator_controllers[
                    bay_config.actuator_controller_id
                ],
                actuator_controller_address=Address(
                    controller_register=bay_config.actuator_controller_address_controller_register,
                    register_bit_mask=bay_config.actuator_controller_address_register_bit_mask,
                ),
            )
            for bay_config in config.bays
            if bay_config.state_controller_id != ""
        }
        self.configure()

    def configure(self):
        """Initialize all the ports."""

        for state_controller in self.state_controllers.values():
            state_controller.configure()
        for actuator_controller in self.actuator_controllers.values():
            actuator_controller.configure()

    def open_bay(self, bay_id: str) -> None:
        """Open the bay with the given id."""

        bay = self.bays[bay_id]
        bay.actuator_controller.open_bay(bay.actuator_controller_address)

    def open_all_bays(self) -> None:
        """Open all bays."""

        for bay in self.bays.values():
            bay.actuator_controller.open_bay(bay.actuator_controller_address)

    def get_states(self) -> Dict[str, bool]:
        """Gets the state of all bays."""

        return {
            bay.bay_id: bay.state_controller.is_open(bay.state_controller_address)
            for bay in self.bays.values()
        }

    def get_state(self, bay_id: str) -> bool:
        """Get the state of the bay with the given id."""

        bay = self.bays[bay_id]
        return bay.state_controller.is_open(bay.state_controller_address)


station = Station()
