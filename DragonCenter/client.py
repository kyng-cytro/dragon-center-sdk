import socket
import json
from enum import IntEnum
from typing import Union


class UserScenario(IntEnum):
    EXTREME_PERFORMANCE = 1
    BALANCED = 2
    SLIENT = 3
    SUPER_BATTERY = 4


class DragonCenterClient:
    def __init__(self, host: str = '127.0.0.1', port: int = 32682, timeout: float = 1.5):
        self.host = host
        self.port = port
        self.timeout = timeout

    def _send_and_receive(self, payload: bytes) -> Union[dict, str]:
        with socket.create_connection((self.host, self.port), timeout=self.timeout) as s:
            s.sendall(payload)
            response = s.recv(4096)
        try:
            return json.loads(response.decode('utf-8'))
        except (UnicodeDecodeError, json.JSONDecodeError):
            return repr(response)

    def get_status(self) -> Union[dict, str]:
        return self._send_and_receive(bytes.fromhex("e90300000005"))

    def update_all(self) -> Union[dict, str]:
        return self._send_and_receive(bytes.fromhex("ea030000557064617465416c6c"))

    def set_status(self, mode: Union[int, UserScenario]) -> Union[dict, str]:
        index = int(mode)
        if not (1 <= index <= 4):
            raise ValueError("Mode index must be between 1 and 4 (inclusive).")
        payload = self._build_set_status_packet(index)
        return self._send_and_receive(payload)

    def _build_set_status_packet(self, index: int) -> bytes:
        header = bytes.fromhex('e90300000012')
        data = {
            "Fan": 0,
            "Index": index,
            "IsLoad": False,
            "KB": -1,
            "PB": -1,
            "Performance": 2
        }
        json_bytes = json.dumps(data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        return header + json_bytes