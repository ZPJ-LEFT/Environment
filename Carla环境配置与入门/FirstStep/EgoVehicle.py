import carla
import random

# 加载客户端
client = carla.Client('localhost', 2000)
world = client.get_world()

# Create ego_vehicle
ego_bp = world.get_blueprint_library().find('vehicle.lincoln.mkz_2020')
ego_bp.set_attribute('role_name', 'hero')
ego_vehicle = world.spawn_actor(ego_bp, random.choice(spawn_points))
