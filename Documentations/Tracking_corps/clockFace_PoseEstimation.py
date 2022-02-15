# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 16:14:46 2020

@author: Nicole
"""
import pyrealsense2 as rs
# Import Numpy for easy array manipulation
import numpy as np
# Import OpenCV for easy image rendering
import cv2 as cv
import os

from cubemos.skeletontracking.native_wrapper import CM_TargetComputeDevice, CM_Image
from cubemos.skeletontracking.core_wrapper import initialise_logging, CM_LogLevel
from cubemos.skeletontracking.native_wrapper import Api, SkeletonKeypoints


class PoseEstimation:
    def __init__(self):
        print("Constructeur de la classe")
        
        #Realsense
        self.pipeline = rs.pipeline()
        self.pipeline_profile = rs.pipeline_profile()
        self.frameset = rs.frame().as_frameset()
        
        #Color
        self.color_frame = rs.frame()
        self.color_width = 1280
        self.color_height = 720
        self.color_fps = 30
        
        #Depth
        self.depth_frame = rs.frame()
        self.intrinsics = rs.intrinsics()
        self.depth_width = 1280
        self.depth_height = 720
        self.depth_fps = 30
        
        #Cubemos
        self.multiple = 16
        self.confidence_threshold = 0.5
        #a faire plus tard
        
        #visualize
        self.skeleton_color = (189, 114, 0)
        self.radius = 5
        self.keypoint_ids = [(1, 2),(1, 5),(2, 3),(3, 4),(5, 6),(6, 7),(1, 8),(8, 9),(9, 10),(1, 11),(11, 12),(12, 13),(1, 0),(0, 14),(14, 16),(0, 15),(15, 17)]
        self.numberKeyPoints = 18
        self.keyPoints = [0,1,2,3,4,5,6,7,8,11,14,15,16,17]
        
        #saveData
        self.coordXYZ_camera = np.zeros((1,3))
        self.coordxy_image = np.zeros((1,2))
        self.lastName = input("Please give me your last name \n")
        self.passageNumber = input("Please enter the passage number \n")
        self.fileName = "Data/"+str(self.lastName)+"_Passage"+str(self.passageNumber)+"_3Dcoordinates.txt"
        self.out = cv.VideoWriter("Data/"+str(self.lastName)+"_Passage"+str(self.passageNumber)+"_film.avi",cv.VideoWriter_fourcc('M','J','P','G'), 25, (self.color_width,self.color_height))
        self.out_RGB = cv.VideoWriter("Data/"+str(self.lastName)+"_Passage"+str(self.passageNumber)+"_film_RGB.avi",cv.VideoWriter_fourcc('M','J','P','G'), 25, (self.color_width,self.color_height))
        self.out_Depth = cv.VideoWriter("Data/"+str(self.lastName)+"_Passage"+str(self.passageNumber)+"_film_Depth.avi",cv.VideoWriter_fourcc('M','J','P','G'), 25, (self.color_width,self.color_height))

 
        
        #Initialize
        self.initialize()
        #self.enable_device_from_file = self.enable_device_from_file('1.mp4')
        
        
    def run(self):
        try:
            while True:
                
                #Update Data
                self.update()
                
                #Draw Data
                self.draw()
                
                #Show Data
                self.show()
                
                #Compute 3D coordinates
                self.compute3DCoordinates()
                
                key = cv.waitKey(1)
                # Press esc or 'q' to close the image window
                if key & 0xFF == ord('q') or key == 27:
                    break
        finally:
            self.finalize()
    
    
    def initialize(self):
        cv.setUseOptimized(True)
        
        #initialize Sensor
        self.initialize_sensor()
        
        #initialize Skeleton
        self.initialize_skeleton()
        
        self.initialize_dataFile()
        
        print("Initialisation ok")
        
        
    def initialize_sensor(self):
        
        #Set Device Config
        self.config = rs.config()

        ##Je lui indique qu'il doit chercher le flux dans le rosbag 5.bag
        rs.config.enable_device_from_file(self.config,"5.bag",repeat_playback=False)
        ### Valeur de la résolution pas bonne il me semble
        self.config.enable_stream(rs.stream.color,self.color_width,self.color_height,rs.format.bgr8,self.color_fps)
        self.config.enable_stream(rs.stream.depth,self.depth_width,self.depth_height,rs.format.z16,self.depth_fps)

        #self.config.enable_device_from_file("Test.mp4")
        
        #Start Pipeline
        self.pipeline_profile = self.pipeline.start(self.config)
        
        #Get Intrinsics
        self.intrinsics = self.pipeline_profile.get_stream(rs.stream.depth).as_video_stream_profile().get_intrinsics()

        
    def initialize_skeleton(self):  
        #create handle
        self.license_directory = os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "license")
        self.api = Api(self.license_directory)
        
        #load model
        self.model_directory = os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "models")
        self.model = os.path.join(self.model_directory, "fp32", "skeleton-tracking.cubemos")
        self.api.load_model(CM_TargetComputeDevice.CM_CPU,self.model)
        
        self.log_directory = os.path.join(os.environ["LOCALAPPDATA"], "Cubemos", "SkeletonTracking", "logs")
        
        
    def initialize_dataFile(self):
        self.fileData = open(self.fileName,"w") 
        self.fileData.write("Time in ms"+"\t"+
                            "Point1-X"+"\t"+"Point1-Y"+"\t"+"Point1-Z"+"\t"+
                            "Point2-X"+"\t"+"Point2-Y"+"\t"+"Point2-Z"+"\t"+
                            "Point3-X"+"\t"+"Point3-Y"+"\t"+"Point3-Z"+"\t"+
                            "Point4-X"+"\t"+"Point4-Y"+"\t"+"Point4-Z"+"\t"+
                            "Point5-X"+"\t"+"Point5-Y"+"\t"+"Point5-Z"+"\t"+
                            "Point6-X"+"\t"+"Point6-Y"+"\t"+"Point6-Z"+"\t"+
                            "Point7-X"+"\t"+"Point7-Y"+"\t"+"Point7-Z"+"\t"+
                            "Point8-X"+"\t"+"Point8-Y"+"\t"+"Point8-Z"+"\t"+
                            "Point9-X"+"\t"+"Point9-Y"+"\t"+"Point9-Z"+"\t"+
                            "Point12-X"+"\t"+"Point12-Y"+"\t"+"Point12-Z"+"\t"+
                            "Point15-X"+"\t"+"Point15-Y"+"\t"+"Point15-Z"+"\t"+
                            "Point16-X"+"\t"+"Point16-Y"+"\t"+"Point16-Z"+"\t"+
                            "Point17-X"+"\t"+"Point17-Y"+"\t"+"Point17-Z"+"\t"+
                            "Point18-X"+"\t"+"Point18-Y"+"\t"+"Point18-Z"+"\n")

            
    def finalize(self):
        
        #Stop Pipeline
        self.pipeline.stop()
        
        #Close Windows
        self.out.release()
        self.out_RGB.release()
        self.out_Depth.release()
        cv.destroyAllWindows()
        
        #Close data file
        self.fileData.close()
        
        print("Finalisation ok")
        
    def update(self):
        #Update Frame
        self.update_frame()
        
        #Update Color
        self.update_color()
        
        #Update Depth
        self.update_depth()
        
        #Update Skeleton
        self.update_skeleton()
        
        
    
    def update_frame(self):
        #Update Frame
        self.frameset = self.pipeline.wait_for_frames()
        self.time = self.frameset.get_timestamp()
        
    def update_color(self):
        #retrieve color frame
        self.color_frame = self.frameset.get_color_frame()
        
        #retrieve frame size
        self.color_width = self.color_frame.as_video_frame().get_width()
        self.color_height = self.color_frame.as_video_frame().get_height()
        self.color_stride = self.color_frame.as_video_frame().get_stride_in_bytes()
        
    def update_depth(self):
        #retrieve depth frame
        self.depth_frame = self.frameset.get_depth_frame()
        
        #retrieve frame size
        self.depth_width = self.depth_frame.as_video_frame().get_width()
        self.depth_height = self.depth_frame.as_video_frame().get_height()
        
        
    def update_skeleton(self):
        image = np.asanyarray(self.color_frame.get_data())
        
        self.size = 12*self.multiple
        self.skeletons = self.api.estimate_keypoints(image,self.size)
        self.new_skeletons = self.api.estimate_keypoints(image, self.size)
        self.new_skeletons = self.api.update_tracking_id(self.skeletons, self.new_skeletons)
        

        

    def draw(self):
        #draw color
        self.draw_color()
        
        #draw skeleton
        self.draw_skeleton()
       
        
    def draw_color(self):
        self.color = np.asanyarray(self.color_frame.get_data())
        self.depth = np.asanyarray(self.depth_frame.get_data())
        
    
    def draw_skeleton(self):
        
        self.out_RGB.write(self.color)
        self.depth = cv.applyColorMap(cv.convertScaleAbs(self.depth, alpha=0.03), cv.COLORMAP_JET) 
        self.out_Depth.write(self.depth)
        self.render_result(self.skeletons, self.color, self.confidence_threshold)
        self.out.write(self.color)
        
        
    def compute3DCoordinates(self):
        for i in range(len(self.skeletons)):
            skeleton = self.skeletons[i]

            self.fileData.write(str(self.time)+'\t')
#            for j in range(self.numberKeyPoints):
            for j in range(len(self.keyPoints)):
                if (skeleton.confidences[self.keyPoints[j]]< self.confidence_threshold):
                    self.fileData.write("NaN"+"\t")
                    self.fileData.write("NaN"+"\t")
                    self.fileData.write("NaN"+"\t")
                    continue
                #get coordinates in the image system
                joint = skeleton.joints[self.keyPoints[j]]
                self.coordxy_image[0,0] = int(joint[0])
                self.coordxy_image[0,1] = int(joint[1])
                
                depth = self.depth_frame.get_distance(int(self.coordxy_image[0,0]),int(self.coordxy_image[0,1]))
                
                x = (self.coordxy_image[0,0]-self.intrinsics.ppx)/(self.intrinsics.fx)
                y = (self.coordxy_image[0,1]-self.intrinsics.ppy)/(self.intrinsics.fy)
                
                #correction distorsion
                r2  = x*x + y*y
                f = 1 + self.intrinsics.coeffs[0]*r2 + self.intrinsics.coeffs[1]*r2*r2 + self.intrinsics.coeffs[4]*r2*r2*r2
                ux = x*f + 2*self.intrinsics.coeffs[2]*x*y + self.intrinsics.coeffs[3]*(r2 + 2*x*x)
                uy = y*f + 2*self.intrinsics.coeffs[3]*x*y + self.intrinsics.coeffs[2]*(r2 + 2*y*y)
                self.coordXYZ_camera[0,0] = ux*depth
                self.coordXYZ_camera[0,1] = uy*depth
                self.coordXYZ_camera[0,2] = depth
                
                self.fileData.write(str(self.coordXYZ_camera[0,0])+"\t")
                self.fileData.write(str(self.coordXYZ_camera[0,1])+"\t")
                self.fileData.write(str(self.coordXYZ_camera[0,2])+"\t")
            self.fileData.write("\n")
            

                
                
    def render_result(self,skeletons, img, confidenceThreshold):
        global limbs
        for index, skeleton in enumerate(skeletons):
            limbs = self.get_valid_limbs(self.keypoint_ids, skeleton, confidenceThreshold)
            for limb in limbs:
                self.color = cv.line(self.color, limb[0], limb[1], self.skeleton_color, thickness=2, lineType=cv.LINE_AA)
        
        
        
    def get_valid_limbs(self,keypointIds, skeleton, confidence_threshold):
        limbs = [
            (tuple(map(int, skeleton.joints[i])), tuple(map(int, skeleton.joints[v])))
            for (i, v) in keypointIds
            if skeleton.confidences[i] >= confidence_threshold
            and skeleton.confidences[v] >= confidence_threshold
        ]
        valid_limbs = [
            limb
            for limb in limbs
            if limb[0][0] >= 0 and limb[0][1] >= 0 and limb[1][0] >= 0 and limb[1][1] >= 0
        ]
        return valid_limbs

    def show(self):
        cv.imshow("GEPROVAS - Squelette", self.color)
        
x = PoseEstimation()
x.run()
