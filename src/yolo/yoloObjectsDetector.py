import numpy as np
import time
import cv2
import os


class YoloObjectsDetector:
    def __init__(self, image, yolo_path=None, min_confidence=0.5, threshold=0.3):
        self.image = image

        # get image height and width
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]

        # load yolo model labels and set paths to yolo weights and config
        if yolo_path is None:
           yolo_path = os.path.abspath(os.path.dirname(__file__))
        self.labels = open(yolo_path + "/coco.names").read().strip().split("\n")
        self.weights_path = yolo_path + "/yolov3.weights"
        self.config_path = yolo_path + "/yolov3.cfg"

        # set confidence and threshold level
        self.min_confidence = min_confidence
        self.threshold = threshold

        # initialize a list of colors to represent class labels
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")

    def get_selected_object_bounding_box(self):
        outputs = self.load_run_model()
        boxes, confidences, classIDs = self.generate_bounding_boxes(outputs)
        bbox = self.get_bbox_from_image(boxes, confidences, classIDs)
        return bbox

    def load_run_model(self):
        # load YOLO object detector trained on COCO dataset
        print("Loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)

        ln = net.getLayerNames()
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

        # construct a blob from the image and set as input
        blob = cv2.dnn.blobFromImage(self.image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)

        # perform a forward pass of the YOLO object detector, giving
        # bboxes of detected objects and associated probabilities
        start = time.time()
        outputs = net.forward(ln)
        end = time.time()

        print(f"YOLO objects detecting took {round(end - start, 4)} seconds")

        return outputs

    def generate_bounding_boxes(self, layerOutputs):
        # initialize lists of detected bboxes, confidences, and class IDs
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # get the class ID and confidence of the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter objects with confidence smaller than minimum given as class parameter
                if confidence > self.min_confidence:
                    # scale the bounding box coordinates back relative to the size of the image
                    box = detection[0:4] * np.array([self.width, self.height, self.width, self.height])
                    (centerX, centerY, width, height) = box.astype("int")

                    # get coordinates of top left corner of the bbox
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update list of bboxes, confidences, and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        return boxes, confidences, classIDs

    def paint_box_on_object(self, box, color, label, confidence):
        # unpack coordinates
        x, y, w, h = box[0], box[1], box[2], box[3]

        # draw a bounding box and label on the image
        cv2.rectangle(self.image, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(label, confidence)
        cv2.putText(self.image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def get_bbox_from_image(self, boxes, confidences, classIDs):
        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, self.min_confidence, self.threshold)
        n = len(indexes)

        # creat lists of filtered bboxes, confidences and classIDs
        boxes = [boxes[i] for i in indexes]
        confidences = [confidences[i] for i in indexes]
        classIDs = [classIDs[i] for i in indexes]

        # create list containing center of each bounding box
        centers = np.array([[int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)] for bbox in boxes])

        if len(boxes) == 0:
            return None
        if len(boxes) == 1:
            return boxes[0]

        # list of selected bboxes
        selected = []

        for i in range(n):
            color = [int(c) for c in self.colors[classIDs[i]]]
            label = self.labels[classIDs[i]]
            confidence = confidences[i]
            self.paint_box_on_object(boxes[i], color, label, confidence)

        # on mouse event function to select bbox
        def onMouse(event, x, y, flags, param):
            nonlocal selected

            if event == cv2.EVENT_LBUTTONDOWN:
                print('x = %d, y = %d' % (x, y))
                selected_index = np.argmin(np.linalg.norm(centers - np.array([x, y]), axis=1))
                selected = boxes[selected_index]

        # show image and set onMouse event to select bbox
        cv2.imshow("Image", self.image)
        cv2.setMouseCallback('Image', onMouse)

        while len(selected) == 0:
            cv2.waitKey(10)

        return selected
