from DragonCenter.client import DragonCenterClient, UserScenario

client = DragonCenterClient()

print("System Info:")
print(client.update_all())

print("Switching to PERFORMANCE mode:")
client.set_status(UserScenario.SUPER_BATTERY)

print("New status:")
print(client.get_status())