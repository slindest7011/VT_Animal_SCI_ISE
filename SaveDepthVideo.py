import pyrealsense2 as rs
import time
from datetime import datetime
import keyboard
from SendDepthPicturesToS3 import to_aws

"""
This program records video when an object of a large enough size enters an area
Robert Kadlec 
9/23/2021
"""

#distance to floor 
#x, y pixel to monitor depth
dist_to_floor = 5.5#3
xCord = 460*2#int(165*2)
yCord = 350*2#int(185*2)

def main():
    count =0
    while count<=3:

        #start the pipeline (camera)
        pipeline = rs.pipeline()
       
        #sets up the camera settings and reccording file
        config = rs.config()
        config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
        config.enable_record_to_file("RoviSysTest" + datetime.now().strftime("%m_%d_%H_%M_%S") + ".bag")
        #config.enable_record_to_file(datetime.now().strftime("%m_%d_%H_%M_%S") + ".bag")
        pipeline_record_profile = pipeline.start(config)
        device_record = pipeline_record_profile.get_device()
        device_recorder = device_record.as_recorder()
        
        #pause the recording until a cow is detected
        rs.recorder.pause(device_recorder)

        #start checking for cow
        while True: #while no cow is detectede

            #press e to end the program
            #this is important because it creates a trashed .bag file 
            #without this the last file would be unviewable
            if keyboard.is_pressed('e'):
                pipeline.stop()
                pipeline = None
                config = None
                exit()

            # Waits for frames from camera
            frames = pipeline.wait_for_frames()
            #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
            depth = frames.get_depth_frame()
   
            #checks the distance to xChord pixel and ychord pixel
            dist_to_center = float(depth.get_distance(xCord, yCord) )#int(width / 2), int(height / 2)

            print("The camera is facing an object " +
                  str(dist_to_center) + "meters away ")
            
            # checks if object is on point of intrest
            if(dist_to_center != 0 and dist_to_floor - dist_to_center > .5):
                break
            #to avoid using too much memory wait 1/4 sec before looping again
            time.sleep(.25)
                    
        #cow is detected so recording is resumed
        rs.recorder.resume(device_recorder)
        pipeline.wait_for_frames().keep()
        
        #timeout prevents recording from going past 5 seconds
        timeout = time.time() + 5
        
        
        while True:  
            print("Recording")
            #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
            frames = pipeline.wait_for_frames()
            depth = frames.get_depth_frame()
            
            #checks the distance to xChord pixel and ychord pixel
            dist_to_cow = float(depth.get_distance(xCord, yCord))
            #if time is longer than 5 seconds
            if(time.time() > timeout):
                break
            #if cow has left
            if(dist_to_cow != 0 and dist_to_floor - dist_to_cow < 0.5):
                break
            break
            time.sleep(.25)
            
        #unassigns all variables
        pipeline.stop()
        pipeline = None
        config = None
        print("Recording Stopped Reseting")
    count+=1

if __name__ == "__main__":
    main()
    to_aws()