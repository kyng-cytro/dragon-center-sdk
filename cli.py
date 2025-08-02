import argparse
from DragonCenter.client import DragonCenterClient, FanMode, UserScenario, PerformanceLevel


def main():
    parser = argparse.ArgumentParser(description="Switch MSI Dragon Center performance mode")
    parser.add_argument(
        "mode",
        type=str,
        choices=[m.name.lower() for m in UserScenario],
        help="Performance mode: silent, balanced, performance, user_defined"
    )
    parser.add_argument(
        "--user-perf",
        type=str,
        choices=[lvl.name.lower() for lvl in PerformanceLevel],
        help="User-defined performance level: turbo, high, medium, low (only for user_defined)"
    )
    parser.add_argument(
        "--fan",
        type=str,
        choices=[f.name.lower() for f in FanMode],
        help="Fan mode: auto, advanced, cooler_boost (only for user_defined)"
    )
    parser.add_argument(
        "--host", type=str, default="127.0.0.1", help="Dragon Center host (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=32682, help="Dragon Center port (default: 32682)"
    )

    args = parser.parse_args()
    client = DragonCenterClient(host=args.host, port=args.port)

    mode_enum = UserScenario[args.mode.upper()]

    if mode_enum == UserScenario.USER_DEFINED:
        if args.user_perf is None:
            parser.error("user_defined mode requires --user-perf")
        user_perf = PerformanceLevel[args.user_perf.upper()]
        fan_mode = FanMode[args.fan.upper()] if args.fan else None
        result = client.set_status(mode_enum, user_perf=user_perf, fan_mode=fan_mode)
    else:
        result = client.set_status(mode_enum)

    print("Response:")
    print(result)


if __name__ == "__main__":
    main()