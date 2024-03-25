import carla
import random

# 加载客户端
client = carla.Client('localhost', 2000)
world = client.get_world()


# 加载地图
client.load_world('Town05')
