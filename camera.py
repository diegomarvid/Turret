import depthai as dai
import numpy as np
import time
from pathlib import Path
from multiprocessing.connection import Listener
from oneEuro import OneEuroFilter

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

        self.initServer()

        self.max_detected_players = 1


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
        self.spatialDetectionNetwork.setDepthUpperThreshold(10000)

    def setObjectTrackerPropierties(self):
        self.objectTracker.setDetectionLabelsToTrack([15])  # track only person
        # possible tracking types: ZERO_TERM_COLOR_HISTOGRAM, ZERO_TERM_IMAGELESS
        self.objectTracker.setTrackerType(dai.TrackerType.ZERO_TERM_COLOR_HISTOGRAM)
        # take the smallest ID when new object is tracked, possible options: SMALLEST_ID, UNIQUE_ID
        self.objectTracker.setTrackerIdAssigmentPolicy(dai.TrackerIdAssigmentPolicy.SMALLEST_ID)

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

            tracklets = self.getTrackedOutputs(device)

            startTime = time.monotonic()

            while(True):

                currentTime = time.monotonic()

                number_of_detected = 0

                if self.oneSecondPassed(startTime, currentTime):

                    startTime = currentTime
              
                    track = tracklets.get()
                    trackletsData = track.tracklets

                    detections = []

                    for detectedPerson in trackletsData:
                        if self.isPersonTracked(detectedPerson):
                            number_of_detected = number_of_detected + 1
                            if number_of_detected <= self.max_detected_players:
                                self.addDetectedPerson(detectedPerson, detections)

                    if number_of_detected > 0: 
                        self.sendDetectedCoordinates(detections)

    
