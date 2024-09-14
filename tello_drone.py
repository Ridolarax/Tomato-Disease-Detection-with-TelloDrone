import cv2
import numpy as np
from djitellopy import Tello
from time import sleep
import keyboard
import random, string 
import threading, random


class Drone:
    def __init__(self) -> None:
        pass
        self.drone = Tello()
        self.frame = None
        self.frame_available = threading.Event()

        self.DroneConnect()
        # self.start_streaming()

    def DroneConnect(self):
        self.drone.connect()

    def getBattery(self):
        if self.drone.get_battery() is not None:
            self.battery_level = self.drone.get_battery()
            print(self.battery_level)
            return self.battery_level
        else:
            print("Failed to retrieve battery level. Please ensure the drone is connected.")

    
    def DroneTakeOff(self):
        if self.getBattery() > 15:
            self.drone.takeoff()
            self.control_drone()
        else:
            print("Drone Battery too low")
        

    def DroneLand(self):
        self.drone.land()
    
    def control_drone(self):
        print("Control the drone using the following keys: ")
        print("'w': Move forward")
        print("'s': Move backward")
        print("'a': Move left")
        print("'d': Move right")
        print("'Up-Arrow': Move Up")
        print("'Down-Arrow': Move Down")
        print("'Left-Arrow': Rotate left")
        print("'Right-Arrow': Rotate Right")
        print("'q': Quit and Land the Drone")

        while True:
            if keyboard.is_pressed("w"):
                self.drone.move_forward(30)
            elif keyboard.is_pressed("s"):
                self.drone.move_back(30)
            elif keyboard.is_pressed("a"):
                self.drone.move_left(30)
            elif keyboard.is_pressed("d"):
                self.drone.move_right(30)
            elif keyboard.is_pressed("up"):
                self.drone.move_up(30)
            elif keyboard.is_pressed("down"):
                self.drone.move_down(30)
            elif keyboard.is_pressed("left"):
                self.drone.rotate_counter_clockwise(30)
            elif keyboard.is_pressed("right"):
                self.drone.rotate_clockwise(30)
            elif keyboard.is_pressed("q"):
                print("Drone Landing...")
                self.DroneLand()
                break

            sleep(0.1)

    def start_streaming(self):
        self.drone.streamon()
        try:
            while True:
                self.frame_read = self.drone.get_frame_read()
                self.frame = self.frame_read.frame

                if self.frame is not None:
                    ret, buffer = cv2.imencode('.jpg', self.frame)
                    frame_image = buffer.tobytes()
                    yield frame_image
                else:
                    yield None
        finally:
            self.drone.streamoff()
            cv2.destroyAllWindows()


    def takeShot(self):
        # self.frame_available.wait(timeout= 10)

        if self.frame is not None:
            img_address = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".png"
            success = cv2.imwrite(img_address, self.frame)
            
            if success:
                print(f"Frame captured for prediction and saved as {img_address}")
                return img_address
            else:
                print("Failed to saved the captured frame")
        else:
            print("No frame available to capture")
            return None
        



    #  if self.frame is not None:
    #         img_address = ''.join(random.choices(string.ascii_letters + string.digits, k=10)) + ".png"
    #         # img_address = "dum.png"
    #         success = cv2.imwrite(img_address, self.frame)

    #         if success:
    #             print(f"Frame Captured for prediction and Saved as {img_address}")
    #             return img_address
    #         else:
    #             print("Failed to capture frame")
    #             return None
            
    #     else:
    #         print("No frame available to capture")
    #         return None


# drone1 = Drone()
# drone1.getBattery()
# # drone1.DroneTakeOff()

# stream_thread = threading.Thread(target=drone1.start_streaming)
# stream_thread.start()

# drone1.takeShot()
# stream_thread.join()