# VT_Animal_SCI_ISE




This Weight Estimation System is made up of two major scripts, the cropByLineAngle.py and Dash.py. 

To Run this system follow the current guidelines: 


        1 Enter the following in your command line python -m pip install -r requirements.txt
        2 Enter in your database credientials within the slots on the Dash.py on line 21 and cropByLineAngle.py on line 360
        3 Store the Data Within the FarmVisit7 Directory with each cow being stored within their folder. 
        Example Directory Structure: 
        FarmVisit7 
              Cow1 
                  123.bag
                  123.png
                  123.txt
              Cow2
                  123.bag
                  123.png
                  123.txt
             
        4 Run the cropByAngle.py script. This will prompt a window to select either an angle picture or a horizontal picture. To select an angled image press 2 
          for the horizontal image press any other key. After this you can size the images length or width. This is down by using the arrow keys and the shift button.           to make a dimension smaller use the shift key and the corressponing arrows, to make them larger, do not use the shift key. Size the image to crop the head, 
          neck and tail from each image.
          
        5 After Finishing the running through the cropyByLineAngle.py script. Run the Dash.py script. After this script runs, go to your favorite web browser and                 search 127.0.0.1:8050. There you should see your dashboard with the data you just uploaded.
           
 
*** Due to a potiential bug in the pyrealsense2 module, the cropByLineAngle.py script is sometimes subject to crash. If that happens re run the script to restart the data gleaning process
