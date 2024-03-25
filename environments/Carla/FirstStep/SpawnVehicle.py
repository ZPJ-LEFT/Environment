import carla
import random

# 加载客户端
client = carla.Client('localhost', 2000)
world = client.get_world()


# 生成载具
vehicle_blueprints = world.get_blueprint_library().filter('*vehicle*')

# 获取地图的出生点
spawn_points = world.get_map().get_spawn_points()

# Spawn 50 vehicles randomly distributed throughout the map 
# for each spawn point, we choose a random vehicle from the blueprint library
for i in range(0,50):
    world.try_spawn_actor(random.choice(vehicle_blueprints), random.choice(spawn_points))
