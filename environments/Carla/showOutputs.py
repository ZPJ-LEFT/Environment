import cv2
import os
import numpy as np

path = 'C:\\codes\\Carla\\out'

for name in os.listdir(path):
    image = cv2.imread(os.path.join(path,name))

    array = np.frombuffer(image.raw_data, dtype=np.dtype("uint8"))
    array = np.reshape(array, (image.height, image.width, 4))

    print(image.shape)
    cv2.imshow('RGB',cv2.cvtColor(image,cv2.COLOR_BGRA2RGB))
    cv2.waitKey(0)
