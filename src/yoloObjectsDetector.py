import numpy as np
import time
import cv2


class YoloObjectsDetector:
    def __init__(self, image, yolo_path="../yolo", confidence=0.5, threshold=0.3):
        self.image = image
        self.height = self.image.shape[0]
        self.width = self.image.shape[1]

        # load the COCO class labels our YOLO model was trained on
        # derive the paths to the YOLO weights and model configuration
        self.labels = open(yolo_path + "/coco.names").read().strip().split("\n")
        self.weights_path = yolo_path + "/yolov3.weights"
        self.config_path = yolo_path + "/yolov3.cfg"

        # load confidence and threshold level
        self.confidence = confidence
        self.threshold = threshold

        # initialize a list of colors to represent each possible class label
        self.colors = np.random.randint(0, 255, size=(len(self.labels), 3), dtype="uint8")

    def get_selected_object_bounding_box(self):
        outputs = self.load_run_model()
        boxes, confidences, classIDs = self.generate_bounding_boxes(outputs)
        bbox = self.get_bbox_from_image(boxes, confidences, classIDs)
        return bbox

    def load_run_model(self):
        # load our YOLO object detector trained on COCO dataset (80 classes)
        print("[INFO] loading YOLO from disk...")
        net = cv2.dnn.readNetFromDarknet(self.config_path, self.weights_path)

        # determine only the *output* layer names that we need from YOLO
        ln = net.getLayerNames()
        ln = [ln[i - 1] for i in net.getUnconnectedOutLayers()]

        # construct a blob from the input image and then perform a forward
        # pass of the YOLO object detector, giving us our bounding boxes and
        # associated probabilities
        blob = cv2.dnn.blobFromImage(self.image, 1 / 255.0, (416, 416), swapRB=True, crop=False)
        net.setInput(blob)
        start = time.time()
        outputs = net.forward(ln)
        end = time.time()

        # show timing information on YOLO
        print("[INFO] YOLO took {:.6f} seconds".format(end - start))

        return outputs

    def generate_bounding_boxes(self, layerOutputs):
        # initialize our lists of detected bounding boxes, confidences, and
        # class IDs, respectively
        boxes = []
        confidences = []
        classIDs = []

        # loop over each of the layer outputs
        for output in layerOutputs:
            # loop over each of the detections
            for detection in output:
                # extract the class ID and confidence (i.e., probability) of
                # the current object detection
                scores = detection[5:]
                classID = np.argmax(scores)
                confidence = scores[classID]

                # filter out weak predictions by ensuring the detected
                # probability is greater than the minimum probability
                if confidence > self.confidence:
                    # scale the bounding box coordinates back relative to the
                    # size of the image, keeping in mind that YOLO actually
                    # returns the center (x, y)-coordinates of the bounding
                    # box followed by the boxes' width and height
                    box = detection[0:4] * np.array([self.width, self.height, self.width, self.height])
                    (centerX, centerY, width, height) = box.astype("int")

                    # use the center (x, y)-coordinates to derive the top and
                    # and left corner of the bounding box
                    x = int(centerX - (width / 2))
                    y = int(centerY - (height / 2))

                    # update our list of bounding box coordinates, confidences,
                    # and class IDs
                    boxes.append([x, y, int(width), int(height)])
                    confidences.append(float(confidence))
                    classIDs.append(classID)

        return boxes, confidences, classIDs

    def paint_box_on_object(self, box, color, label, confidence):
        # unpack the coordinates of the box
        x, y, w, h = box[0], box[1], box[2], box[3]

        # draw a bounding box rectangle and label on the image
        cv2.rectangle(self.image, (x, y), (x + w, y + h), color, 2)
        text = "{}: {:.4f}".format(label, confidence)
        cv2.putText(self.image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    def get_bbox_from_image(self, boxes, confidences, classIDs):
        # apply non-maxima suppression to suppress weak, overlapping bounding boxes
        indexes = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold)
        n = len(indexes)

        boxes = [boxes[i] for i in indexes]
        confidences = [confidences[i] for i in indexes]
        classIDs = [classIDs[i] for i in indexes]
        centers = np.array([[int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)] for bbox in boxes])

        if len(boxes) == 0:
            return None
        if len(boxes) == 1:
            return boxes[0]

        selected = []

        for i in range(n):
            color = [int(c) for c in self.colors[classIDs[i]]]
            label = self.labels[classIDs[i]]
            confidence = confidences[i]
            self.paint_box_on_object(boxes[i], color, label, confidence)

        def onMouse(event, x, y, flags, param):
            nonlocal selected

            if event == cv2.EVENT_LBUTTONDOWN:
                print('x = %d, y = %d' % (x, y))
                selected_index = np.argmin(np.linalg.norm(centers - np.array([x, y]), axis=1))
                selected = boxes[selected_index]

        # show image to select bbox
        cv2.imshow("Image", self.image)
        cv2.setMouseCallback('Image', onMouse)

        while len(selected) == 0:
            cv2.waitKey(10)

        return selected
