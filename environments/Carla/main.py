import carla
import random
import logging
import os
import time
from queue import Queue
from queue import Empty

from carla import ColorConverter as cc

# Sensor callback.
# This is where you receive the sensor data and
# process it as you liked and the important part is that,
# at the end, it should include an element into the sensor queue.
def sensor_callback(sensor_data, sensor_queue, sensor_name):
    # Do stuff with the sensor_data data like save it to disk
    # Then you just need to add to the queue
    save_path = os.path.join('C:\\codes\\Carla\\out' , sensor_name)
    if not os.path.exists(save_path):
        os.makedirs(save_path)

    if sensor_name == 'camera_rgb':
        sensor_queue.put((sensor_data.frame, sensor_name))
        sensor_data.save_to_disk(os.path.join(save_path, '%06d.png' % sensor_data.frame))
    else:
        sensor_queue.put((sensor_data.frame, sensor_name))
        sensor_data.get_color_coded_flow().save_to_disk(os.path.join(save_path, '%06d.png' % sensor_data.frame)) 

def get_actor_blueprints(world, filter, generation):
    bps = world.get_blueprint_library().filter(filter)

    if generation.lower() == "all":
        return bps

    # If the filter returns only one bp, we assume that this one needed
    # and therefore, we ignore the generation
    if len(bps) == 1:
        return bps

    try:
        int_generation = int(generation)
        # Check if generation is in available generations
        if int_generation in [1, 2]:
            bps = [x for x in bps if int(x.get_attribute('generation')) == int_generation]
            return bps
        else:
            print("   Warning! Actor Generation is not valid. No actor will be spawned.")
            return []
    except:
        print("   Warning! Actor Generation is not valid. No actor will be spawned.")
        return []
    

def main():
    try:
        logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

        seed = 0
        seed_walk = 0
        synchronous = True
        hero = True
        number_of_vehicles = 30
        number_of_walkers = 10
        car_lights_on = False
        width = 256
        height = 256

        random.seed(seed)

        vehicles_list = []
        walkers_list = []
        sensor_list = []
        all_id = []

        # Load Client
        client = carla.Client('localhost', 2000)
        client.set_timeout(10.0)

        # Load World
        world = client.get_world()
        settings = world.get_settings()
        spectator = world.get_spectator()

        # Load Traffic Manger
        traffic_manager = client.get_trafficmanager(8000)
        traffic_manager.set_global_distance_to_leading_vehicle(2.5)
        traffic_manager.set_random_device_seed(seed)

        # Synchronous or Asynchronous
        synchronous_master = synchronous
        if synchronous:
            traffic_manager.set_synchronous_mode(True)
            if not settings.synchronous_mode:
                synchronous_master = True
                settings.synchronous_mode = True
                settings.fixed_delta_seconds = 0.05
            else:
                synchronous_master = False
        world.apply_settings(settings)

        # Load Blueprints
        blueprintsVehicle = get_actor_blueprints(world, 'vehicle.*', 'All')
        blueprintsWalkers = get_actor_blueprints(world, 'walker.pedestrian.*', '2')
        blueprintsVehicle = sorted(blueprintsVehicle, key=lambda bp: bp.id)

        # Load Spawn Points
        spawn_points = world.get_map().get_spawn_points()
        number_of_spawn_points = len(spawn_points)
        if number_of_vehicles < number_of_spawn_points:
            random.shuffle(spawn_points)
        elif number_of_vehicles > number_of_spawn_points:
            msg = 'requested %d vehicles, but could only find %d spawn points'
            logging.warning(msg, number_of_vehicles, number_of_spawn_points)
            number_of_vehicles = number_of_spawn_points

        # @todo cannot import these directly.
        SpawnActor = carla.command.SpawnActor
        SetAutopilot = carla.command.SetAutopilot
        FutureActor = carla.command.FutureActor

        # --------------
        # Spawn vehicles
        # --------------
        batch = []
        for n, transform in enumerate(spawn_points):
            if n >= number_of_vehicles:
                break
            blueprint = random.choice(blueprintsVehicle)
            if blueprint.has_attribute('color'):
                color = random.choice(blueprint.get_attribute('color').recommended_values)
                blueprint.set_attribute('color', color)
            if blueprint.has_attribute('driver_id'):
                driver_id = random.choice(blueprint.get_attribute('driver_id').recommended_values)
                blueprint.set_attribute('driver_id', driver_id)
            if hero:
                blueprint.set_attribute('role_name', 'hero')
                hero = False
            else:
                blueprint.set_attribute('role_name', 'autopilot')

            # spawn the cars and set their autopilot and light state all together
            batch.append(SpawnActor(blueprint, transform)
                .then(SetAutopilot(FutureActor, True, traffic_manager.get_port())))

        for response in client.apply_batch_sync(batch, synchronous_master):
            if response.error:
                logging.error(response.error)
            else:
                vehicles_list.append(response.actor_id)
        
        # Set automatic vehicle lights update if specified
        if car_lights_on:
            all_vehicle_actors = world.get_actors(vehicles_list)
            for actor in all_vehicle_actors:
                traffic_manager.update_vehicle_lights(actor, True)
        
        # -------------
        # Spawn Walkers
        # -------------
        # some settings
        percentagePedestriansRunning = 0.0      # how many pedestrians will run
        percentagePedestriansCrossing = 0.0     # how many pedestrians will walk through the road
        if seed_walk:
            world.set_pedestrians_seed(seed_walk)
            random.seed(seed_walk)
        # 1. take all the random locations to spawn
        spawn_points = []
        for i in range(number_of_walkers):
            spawn_point = carla.Transform()
            loc = world.get_random_location_from_navigation()
            if (loc != None):
                spawn_point.location = loc
                spawn_points.append(spawn_point)
        # 2. we spawn the walker object
        batch = []
        walker_speed = []
        for spawn_point in spawn_points:
            walker_bp = random.choice(blueprintsWalkers)
            # set as not invincible
            if walker_bp.has_attribute('is_invincible'):
                walker_bp.set_attribute('is_invincible', 'false')
            # set the max speed
            if walker_bp.has_attribute('speed'):
                if (random.random() > percentagePedestriansRunning):
                    # walking
                    walker_speed.append(walker_bp.get_attribute('speed').recommended_values[1])
                else:
                    # running
                    walker_speed.append(walker_bp.get_attribute('speed').recommended_values[2])
            else:
                print("Walker has no speed")
                walker_speed.append(0.0)
            batch.append(SpawnActor(walker_bp, spawn_point))
        results = client.apply_batch_sync(batch, True)
        walker_speed2 = []
        for i in range(len(results)):
            if results[i].error:
                logging.error(results[i].error)
            else:
                walkers_list.append({"id": results[i].actor_id})
                walker_speed2.append(walker_speed[i])
        walker_speed = walker_speed2
        # 3. we spawn the walker controller
        batch = []
        walker_controller_bp = world.get_blueprint_library().find('controller.ai.walker')
        for i in range(len(walkers_list)):
            batch.append(SpawnActor(walker_controller_bp, carla.Transform(), walkers_list[i]["id"]))
        results = client.apply_batch_sync(batch, True)
        for i in range(len(results)):
            if results[i].error:
                logging.error(results[i].error)
            else:
                walkers_list[i]["con"] = results[i].actor_id
        # 4. we put together the walkers and controllers id to get the objects from their id
        for i in range(len(walkers_list)):
            all_id.append(walkers_list[i]["con"])
            all_id.append(walkers_list[i]["id"])
        all_actors = world.get_actors(all_id)

        # wait for a tick to ensure client receives the last transform of the walkers we have just created
        if not synchronous or not synchronous_master:
            world.wait_for_tick()
        else:
            world.tick()

        # 5. initialize each controller and set target to walk to (list is [controler, actor, controller, actor ...])
        # set how many pedestrians can cross the road
        world.set_pedestrians_cross_factor(percentagePedestriansCrossing)
        for i in range(0, len(all_id), 2):
            # start walker
            all_actors[i].start()
            # set walk to random point
            all_actors[i].go_to_location(world.get_random_location_from_navigation())
            # max speed
            all_actors[i].set_max_speed(float(walker_speed[int(i/2)]))

        print('spawned %d vehicles and %d walkers, press Ctrl+C to exit.' % (len(vehicles_list), len(walkers_list)))

        # Example of how to use Traffic Manager parameters
        traffic_manager.global_percentage_speed_difference(30.0)
        
        # -------------
        # Sensors
        # -------------
        # We create the sensor queue in which we keep track of the information
        # already received. This structure is thread safe and can be
        # accessed by all the sensors callback concurrently without problem.
        sensor_queue = Queue()
        main_vehicle = world.get_actor(random.choice(vehicles_list))
        camera_init_trans = carla.Transform(carla.Location(z=3))

        camera_rgb = world.get_blueprint_library().find('sensor.camera.rgb')
        camera_rgb.set_attribute('image_size_x', str(width))
        camera_rgb.set_attribute('image_size_y', str(height))
        sensor_rgb = world.spawn_actor(camera_rgb, camera_init_trans, main_vehicle)
        sensor_rgb.listen(lambda data: sensor_callback(data, sensor_queue, "camera_rgb"))
        sensor_list.append(sensor_rgb)

        camera_optical_flow = world.get_blueprint_library().find('sensor.camera.optical_flow')
        camera_optical_flow.set_attribute('image_size_x', str(width))
        camera_optical_flow.set_attribute('image_size_y', str(height))
        sensor_optical_flow = world.spawn_actor(camera_optical_flow, camera_init_trans, main_vehicle)
        sensor_optical_flow.listen(lambda data: sensor_callback(data, sensor_queue, "camera_optical_flow"))
        sensor_list.append(sensor_optical_flow)

        # camera_dvs = world.get_blueprint_library().find('sensor.camera.dvs')
        # sensor_dvs = world.spawn_actor(camera_dvs, camera_init_trans, main_vehicle)
        # sensor_dvs.listen(lambda image: image.save_to_disk('C:\\Carla\\out\\%06d.png' % image.frame))

        # -------------
        # Main Loop
        # -------------
        while True:
            if synchronous and synchronous_master:
                world.tick()
            else:
                world.wait_for_tick()

            w_frame = world.get_snapshot().frame
            print("\nWorld's frame: %d" % w_frame)

            # Now, we wait to the sensors data to be received.
            # As the queue is blocking, we will wait in the queue.get() methods
            # until all the information is processed and we continue with the next frame.
            # We include a timeout of 1.0 s (in the get method) and if some information is
            # not received in this time we continue.
            try:
                for i in range(len(sensor_list)):
                    spectator.set_transform(sensor_list[i].get_transform())

                    s_frame = sensor_queue.get(True, 1.0)
                    print("    Frame: %d   Sensor: %s" % (s_frame[0], s_frame[1]))
            except Empty:
                print("    Some of the sensor information is missed")
    
    finally:
        for sensor in sensor_list:
            sensor.destroy()

        if synchronous and synchronous_master:
            settings = world.get_settings()
            settings.synchronous_mode = False
            settings.no_rendering_mode = False
            settings.fixed_delta_seconds = None
            world.apply_settings(settings)

        print('\ndestroying %d vehicles' % len(vehicles_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in vehicles_list])

        # stop walker controllers (list is [controller, actor, controller, actor ...])
        for i in range(0, len(all_id), 2):
            all_actors[i].stop()

        print('\ndestroying %d walkers' % len(walkers_list))
        client.apply_batch([carla.command.DestroyActor(x) for x in all_id])

        time.sleep(0.5)
    

if __name__ == "__main__":
    main()
