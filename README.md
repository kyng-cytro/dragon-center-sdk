# DragonCenter SDK (Unofficial)

Python SDK + CLI for interacting with MSI Dragon Center's local socket interface.

This tool allows you to get system info, query current performance status, and switch user scenarios, including custom performance and fan configurations—just like MSI Dragon Center does internally.

## Usage

Python SDK
```py
from DragonCenter.client import DragonCenterClient, UserScenario, PerformanceLevel, FanMode

client = DragonCenterClient()

# View current system state
print("System Info:")
print(client.update_all())

# Switch to SUPER BATTERY mode
client.set_status(UserScenario.SUPER_BATTERY)

# Switch to USER_DEFINED mode (Turbo + Cooler Boost)
client.set_status(
    UserScenario.USER_DEFINED,
    user_perf=PerformanceLevel.TURBO,
    fan_mode=FanMode.COOLER_BOOST
)

# Check current status
print("New Status:")
print(client.get_status())
```

CLI Tool
```bash
python cli.py [scenario] [--host <string>] [--port <number>] [--user-perf LEVEL] [--fan MODE]
```
Examples:
```bash
# Switch to Extreme Performance
python cli.py extreme_performance

# Set user-defined performance (Turbo mode + Cooler Boost)
python cli.py user_defined --user-perf turbo --fan cooler_boost

# View help
python cli.py --help
```

## User Scenarios

| Scenario              | Value |
|-------------------|-------|
| EXTREME_PERFORMANCE | 1     |
| BALANCED            | 2     |
| SLIENT              | 3     |
| SUPER_BATTERY       | 4     |
| USER_DEFINED        | 5     |

`Only USER_DEFINED requires user_perf and fan_mode.`

## Performance Levels

For `USER_DEFINED`:

| Name   | Value |
|--------|-------|
| TURBO  | 0     |
| HIGH   | 1     |
| MEDIUM | 2     |
| LOW    | 3     |

## Fan Modes

| Name          | Value |
|---------------|-------|
| AUTO          | 0     |
| ADVANCED      | 1     |
| COOLER_BOOST  | 2     |


## Advanced

The Dragon Center server defaults to 127.0.0.1:32682, but just in case you can override this in both the CLI and SDK.

```py
DragonCenterClient(host="127.0.0.1", port=32682)
```

## Disclaimer

This tool is not affiliated with or supported by MSI. Reverse-engineered for educational purposes and local use only. Use at your own risk.