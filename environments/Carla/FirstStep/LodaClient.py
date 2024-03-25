import carla
import random

# 加载客户端
client = carla.Client('localhost', 2000)
world = client.get_world()
