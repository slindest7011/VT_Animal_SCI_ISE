import pyrealsense2 as rs
import time
from datetime import datetime

"""
This program takes depth pictures when an object of a large enough size enters an area
Robert Kadlec 
9/23/2021
"""

#distance to ground / object that is constant
#x  and y cords for point of intrest
dist_to_ground = 1.6
xCord = int(335)
yCord = int(350)
#how many pictures of each cow are to be taken
numOfPics = 30
#time between the pictures of the cow
sec_between_pics = .01

pipeline = rs.pipeline()
#sets the configuration resolution and fps 
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 10)
pipeline_record_profile = pipeline.start()

#records the depth picture of a cow at the scale
#@param frame first frame to be captured 
def record(frame):
    #set cow to false to allow a while loop
    cow = False
    i = 0
    while not cow:  
        print("Cow Detected")
        #waits for frames
        while (i < numOfPics):
            saver = rs.save_single_frameset(datetime.now().strftime("%m_%d_%Y___%H_%M_%S") + "__pic" + str(i))
            saver.process(frame)
            time.sleep(sec_between_pics)
            frame = pipeline.wait_for_frames()
            i=i + 1

        frames = pipeline.wait_for_frames()
        #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
        depth = frames.get_depth_frame()
        
        #checks the distance to xChord pixel and ychord pixel
        dist_to_center = float(depth.get_distance(xCord, yCord))
        
        print(str(dist_to_center))
        #checks if cow left
        if(dist_to_center != 0 and dist_to_ground - dist_to_center < .5):
            cow = True

        time.sleep(0.25)
    
    loopUntilCow()
    
def loopUntilCow():
    cow = False
    
    while not cow: #while no cow is detected
        #gets the distance to center pixel
        frames = pipeline.wait_for_frames()
        #Retrieve the first depth frame, if no frame is found, return an empty frame instance.
        depth = frames.get_depth_frame()
        #checks the distance to xChord pixel and ychord pixel
        dist_to_center = float(depth.get_distance(xCord, yCord))

        # if first loop dist_to_center_previous set to dist_to_center
        # checks for distance change
        if(dist_to_center != 0 and dist_to_ground - dist_to_center > .25):
            cow = True
        
        #prints distance information
        print("The camera is facing an object " +
              str(dist_to_center) + "meters away ")
        #wait 1/2 sec
        time.sleep(.5)

    record(frames)

def main():
    loopUntilCow()

if __name__ == "__main__":
    main()
