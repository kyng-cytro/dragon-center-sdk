import socket
import json
from enum import IntEnum
from typing import Optional, Union


class UserScenario(IntEnum):
    EXTREME_PERFORMANCE = 1
    BALANCED = 2
    SLIENT = 3
    SUPER_BATTERY = 4
    USER_DEFINED = 5


class PerformanceLevel(IntEnum):
    TURBO = 0
    HIGH = 1
    MEDIUM = 2
    LOW = 3


class FanMode(IntEnum):
    AUTO = 0
    ADVANCED = 1
    COOLER_BOOST = 2


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

    def set_status(
        self,
        scenario: Union[int, UserScenario],
        *,
        user_perf: Optional[Union[int, PerformanceLevel]] = None,
        fan_mode: Optional[Union[int, FanMode]] = None
    ) -> Union[dict, str]:
        index = int(scenario)
        if not (1 <= index <= 5):
            raise ValueError("Mode index must be between 1 and 5 (inclusive).")

        payload = self._build_set_status_packet(index, user_perf, fan_mode)
        return self._send_and_receive(payload)

    def _build_set_status_packet(
        self,
        index: int,
        user_perf: Optional[int] = None,
        fan_mode: Optional[int] = None
    ) -> bytes:
        header = bytes.fromhex('e90300000012')
        data = {"Index": index}

        if index == UserScenario.USER_DEFINED:
            if user_perf is None:
                raise ValueError("For USER_DEFINED (Index 5), user_perf must be provided")
            data["Performance"] = int(user_perf)
            if fan_mode is not None:
                data["Fan"] = int(fan_mode)

        json_bytes = json.dumps(data, separators=(',', ':'), ensure_ascii=False).encode('utf-8')
        return header + json_bytes