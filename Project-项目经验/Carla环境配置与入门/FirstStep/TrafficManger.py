import carla
import random

# 加载客户端
client = carla.Client('localhost', 2000)
world = client.get_world()


for vehicle in world.get_actors().filter('*vehicle*'):
    vehicle.set_autopilot(True)
