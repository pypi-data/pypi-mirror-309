# Copyright 2024 CrackNuts. All rights reserved.

import pathlib
import typing

from cracknuts_panel.acquisition_panel import AcquisitionPanelWidget
from cracknuts_panel.cracker_panel import CrackerPanelWidget
from cracknuts_panel.panel import MsgHandlerPanelWidget
from cracknuts_panel.trace_panel import TraceMonitorPanelWidget
import json
import os


class CracknutsPanelWidget(CrackerPanelWidget, AcquisitionPanelWidget, TraceMonitorPanelWidget, MsgHandlerPanelWidget):
    _esm = pathlib.Path(__file__).parent / "static" / "CrackNutsPanelWidget.js"
    _css = ""

    _CURRENT_CONFIG_NAME = ".cracknuts_config"

    def __init__(self, *args: typing.Any, **kwargs: typing.Any) -> None:
        if "acquisition" not in kwargs:
            raise ValueError("acquisition must be provided")
        kwargs["cracker"]: 'StatefulCracker' = kwargs["acquisition"].cracker
        super().__init__(*args, **kwargs)
        self._load_current_path_config()
        self.reg_msg_handler("dumpConfigButton", "onClick", self.dump_config_button_click)
        self.reg_msg_handler("loadConfigButton", "onClick", self.load_config_button_click)
        self.reg_msg_handler("saveConfigButton", "onClick", self.save_config_button_click)

    def sync_config(self) -> None:
        CrackerPanelWidget.sync_config(self)
        AcquisitionPanelWidget.sync_config(self)

    def bind(self) -> None:
        CrackerPanelWidget.bind(self)
        AcquisitionPanelWidget.bind(self)

    def dump_config_button_click(self, args: dict[str, typing.Any]):
        self.send(
            {
                "dumpConfigCompleted": self._dump_config()
            }
        )

    def load_config_button_click(self, args: dict[str, typing.Any]):
        connection_info = args.get("connection")
        config_info = args.get("config")
        acquisiton_info = args.get("acquisition")
        self.cracker.load_config_from_str(config_info)
        self.cracker.set_uri(connection_info)
        self.acquisition.load_config_from_str(acquisiton_info)
        self.sync_config()
        self.send({"loadConfigCompleted": True})

    def save_config_button_click(self, args: dict[str, typing.Any]):
        current_config_path = os.path.join(os.getcwd(), self._CURRENT_CONFIG_NAME)
        with open(current_config_path, "w") as f:
            f.write(self._dump_config())

    def _dump_config(self):
        return json.dumps(
            {
                "connection": self.cracker.get_uri(),
                "config": self.cracker.dump_config(),
                "acquisition": self.acquisition.dump_config()
            }
        )

    def _load_current_path_config(self):
        """
        Load the workspace configuration if it exists.
        """
        current_config_path = os.path.join(os.getcwd(), self._CURRENT_CONFIG_NAME)
        if os.path.exists(current_config_path):
            with open(current_config_path) as f:
                try:
                    config = json.load(f)
                except json.JSONDecodeError as e:
                    self._logger.error(f"Load workspace config file failed: {e.args}")
                    return
                connection_info = config.get("connection")
                config_info = config.get("config")
                acquisition_info = config.get("acquisition")
                self.cracker.load_config_from_str(config_info)
                self.cracker.set_uri(connection_info)
                self.acquisition.load_config_from_str(acquisition_info)