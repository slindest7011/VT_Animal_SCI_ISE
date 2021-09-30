import pyrealsense2 as rs

"""
This program takes a single depth picture of the area
Robert Kadlec 
9/23/2021
"""

pipeline = rs.pipeline()
config = rs.config()
config.enable_stream(rs.stream.depth, 1280, 720, rs.format.z16, 30)
pipeline.start()
frame = pipeline.wait_for_frames()
saver = rs.save_single_frameset("RoviSysTestPic")
saver.process(frame)