import depthai as dai
import numpy as np
import cv2
import time
from pathlib import Path
from multiprocessing.connection import Listener

class Camera:

    def __init__(self):
       
        self.encoded_authkey = self.createEncondedAuthkey()
        self.port = 6000
        self.conn = None

        self.nnPathDefault = self.getNeuralNetworkPath()
        self.fullFrameTracking = False

        self.pipeline = None
        self.camRgb = None
        self.spatialDetectionNetwork = None
        self.monoLeft = None
        self.monoRight = None
        self.stereo = None
        self.objectTracker = None
        self.xoutRgb = None
        self.trackerOut = None

        self.configCamera()

        # self.initServer()

    def createEncondedAuthkey(self):
        authkey = "secret"
        return authkey.encode('UTF-8')

    def getNeuralNetworkPath(self):
        return str((Path(__file__).parent / Path('models/mobilenet-ssd_openvino_2021.2_6shave.blob')).resolve().absolute())
            
    def createPipeline(self):
        self.pipeline = dai.Pipeline()
        self.pipeline.setOpenVINOVersion(dai.OpenVINO.Version.VERSION_2021_2)

    def createCamRgb(self):
        self.camRgb = self.pipeline.createColorCamera()

    def createSpatialDetectionNetwork(self):
        self.spatialDetectionNetwork = self.pipeline.createMobileNetSpatialDetectionNetwork()

    def createMonoLeft(self):
        self.monoLeft = self.pipeline.createMonoCamera()

    def createMonoRight(self):
        self.monoRight = self.pipeline.createMonoCamera()

    def createStereo(self):
        self.stereo = self.pipeline.createStereoDepth()

    def createObjectTracker(self):
        self.objectTracker = self.pipeline.createObjectTracker()

    def createXoutRgb(self):
        self.xoutRgb = self.pipeline.createXLinkOut()

    def creatTrackerOut(self):
        self.trackerOut = self.pipeline.createXLinkOut()

    def setStreamsName(self):
        self.xoutRgb.setStreamName("preview")
        self.trackerOut.setStreamName("tracklets")

    def setCamRgbPropierties(self):
        self.camRgb.setPreviewSize(300, 300)
        self.camRgb.setResolution(dai.ColorCameraProperties.SensorResolution.THE_1080_P)
        self.camRgb.setInterleaved(False)
        self.camRgb.setColorOrder(dai.ColorCameraProperties.ColorOrder.BGR)

    def setMonoLeftPropierties(self):
        self.monoLeft.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.monoLeft.setBoardSocket(dai.CameraBoardSocket.LEFT)

    def setMonoRightPropierties(self):
        self.monoRight.setResolution(dai.MonoCameraProperties.SensorResolution.THE_400_P)
        self.monoRight.setBoardSocket(dai.CameraBoardSocket.RIGHT)

    def setStereoPropierties(self):
        self.stereo.setConfidenceThreshold(255)

    def setSpatialDetectionNetworkProperties(self):
        self.spatialDetectionNetwork.setBlobPath(self.nnPathDefault)
        self.spatialDetectionNetwork.setConfidenceThreshold(0.5)
        self.spatialDetectionNetwork.input.setBlocking(False)
        self.spatialDetectionNetwork.setBoundingBoxScaleFactor(0.5)
        self.spatialDetectionNetwork.setDepthLowerThreshold(100)
        self.spatialDetectionNetwork.setDepthUpperThreshold(15000)

    def setObjectTrackerPropierties(self):
        self.objectTracker.setDetectionLabelsToTrack([15])  # track only person
        # possible tracking types: ZERO_TERM_COLOR_HISTOGRAM, ZERO_TERM_IMAGELESS
        self.objectTracker.setTrackerType(dai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
        # take the smallest ID when new object is tracked, possible options: SMALLEST_ID, UNIQUE_ID
        self.objectTracker.setTrackerIdAssigmentPolicy(dai.TrackerIdAssigmentPolicy.UNIQUE_ID)

    def linkDevices(self):

        self.monoLeft.out.link(self.stereo.left)
        self.monoRight.out.link(self.stereo.right)

        self.camRgb.preview.link(self.spatialDetectionNetwork.input)
        self.objectTracker.passthroughTrackerFrame.link(self.xoutRgb.input)
        self.objectTracker.out.link(self.trackerOut.input)

        if self.fullFrameTracking:
            self.camRgb.setPreviewKeepAspectRatio(False)
            self.camRgb.video.link(self.objectTracker.inputTrackerFrame)
            self.objectTracker.inputTrackerFrame.setBlocking(False)
            # do not block the pipeline if it's too slow on full frame
            self.objectTracker.inputTrackerFrame.setQueueSize(2)
        else:
            self.spatialDetectionNetwork.passthrough.link(self.objectTracker.inputTrackerFrame)

        self.spatialDetectionNetwork.passthrough.link(self.objectTracker.inputDetectionFrame)
        self.spatialDetectionNetwork.out.link(self.objectTracker.inputDetections)
        self.stereo.depth.link(self.spatialDetectionNetwork.inputDepth)

    def createSourcesAndOutputs(self):
        self.createPipeline()
        self.createCamRgb()
        self.createSpatialDetectionNetwork()
        self.createMonoLeft()
        self.createMonoRight()
        self.createStereo()
        self.createObjectTracker()
        self.createXoutRgb()
        self.creatTrackerOut()

    def setPropierties(self):
        self.setCamRgbPropierties()
        self.setMonoLeftPropierties()
        self.setMonoRightPropierties()
        self.setStereoPropierties()
        self.setSpatialDetectionNetworkProperties()
        self.setObjectTrackerPropierties()

    def configCamera(self):    
        self.createSourcesAndOutputs()
        self.setStreamsName()
        self.setPropierties()
        self.linkDevices()


    def initServer(self):
        address = ('localhost', self.port)     # family is deduced to be 'AF_INET'

        listener = Listener(address, authkey= self.encoded_authkey)
        print(f"Server started at port: {self.port}")
        print("Waiting for client...")

        self.conn = listener.accept()
        print('connection accepted from', listener.last_accepted)

    def getTrackedOutputs(self,device):
        device.getOutputQueue("preview", 4, False)
        return device.getOutputQueue("tracklets", 4, False)

    def addDetectedPerson(self,detectedPerson, detections):
        xr = int(detectedPerson.spatialCoordinates.x)
        yr = int(detectedPerson.spatialCoordinates.y)
        zr = int(detectedPerson.spatialCoordinates.z)
        detections.append([xr, yr, zr, detectedPerson.id])
        
    def sendDetectedCoordinates(self, detections):
        self.conn.send(detections)   
    
    def isPersonTracked(self, detectedPerson):
        return detectedPerson.status == dai.Tracklet.TrackingStatus.TRACKED

    def oneSecondPassed(self, startTime, currentTime):
        return (currentTime - startTime) > 0.05

    

    def detect(self):
        # Pipeline defined, now the device is connected to
        with dai.Device(self.pipeline) as device:

            preview = device.getOutputQueue("preview", 4, False)
            tracklets = device.getOutputQueue("tracklets", 4, False)

            startTime = time.monotonic()
            counter = 0
            fps = 0
            color = (255, 255, 255)

            while(True):
                imgFrame = preview.get()
                track = tracklets.get()

                counter+=1
                current_time = time.monotonic()
                if (current_time - startTime) > 1 :
                    fps = counter / (current_time - startTime)
                    counter = 0
                    startTime = current_time

                frame = imgFrame.getCvFrame()
                trackletsData = track.tracklets
                
                for t in trackletsData:
                    roi = t.roi.denormalize(frame.shape[1], frame.shape[0])
                    x1 = int(roi.topLeft().x)
                    y1 = int(roi.topLeft().y)
                    x2 = int(roi.bottomRight().x)
                    y2 = int(roi.bottomRight().y)

                    try:
                        label = labelMap[t.label]
                    except:
                        label = t.label

                    cv2.putText(frame, str(label), (x1 + 10, y1 + 20), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.putText(frame, f"ID: {[t.id]}", (x1 + 10, y1 + 35), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.putText(frame, t.status.name, (x1 + 10, y1 + 50), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.rectangle(frame, (x1, y1), (x2, y2), color, cv2.FONT_HERSHEY_SIMPLEX)

                    cv2.putText(frame, f"X: {int(t.spatialCoordinates.x)} mm", (x1 + 10, y1 + 65), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.putText(frame, f"Y: {int(t.spatialCoordinates.y)} mm", (x1 + 10, y1 + 80), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)
                    cv2.putText(frame, f"Z: {int(t.spatialCoordinates.z)} mm", (x1 + 10, y1 + 95), cv2.FONT_HERSHEY_TRIPLEX, 0.5, 255)

                cv2.putText(frame, "NN fps: {:.2f}".format(fps), (2, frame.shape[0] - 4), cv2.FONT_HERSHEY_TRIPLEX, 0.4, color)

                cv2.imshow("tracker", frame)

                if cv2.waitKey(1) == ord('q'):
                    break

               
