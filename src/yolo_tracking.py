import numpy as np
import time
import cv2
from tkinter.filedialog import askopenfilename


class YoloTracking:
    def __init__(self, image, yolo_path="./yolo", confidence=0.5, threshold=0.3):
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

    def detect_objects(self):
        outputs = self.load_run_model()
        boxes, confidences, classIDs = self.generate_bounding_boxes(outputs)
        self.show_output_image(boxes, confidences, classIDs)

        print(classIDs)

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

    def show_output_image(self, boxes, confidences, classIDs):
        # apply non-maxima suppression to suppress weak, overlapping bounding
        # boxes
        idxs = cv2.dnn.NMSBoxes(boxes, confidences, self.confidence, self.threshold)

        # ensure at least one detection exists
        if len(idxs) > 0:
            # loop over the indexes we are keeping
            for i in idxs.flatten():
                color = [int(c) for c in self.colors[classIDs[i]]]
                label = self.labels[classIDs[i]]
                confidence = confidences[i]

                # draw a bounding box rectangle and label on the image
                self.paint_box_on_object(boxes[i], color, label, confidence)

        # show the output image
        cv2.imshow("Image", self.image)
        cv2.waitKey(0)


if __name__ == "__main__":
    input_file_path = askopenfilename(title="Select file to convert")
    if input_file_path == "":
        raise Exception("No file selected")

    capture = cv2.VideoCapture(input_file_path)

    ret, frame = capture.read()
    if not ret:
        raise Exception("Cannot read video file")

    yolo = YoloTracking(frame)
    yolo.detect_objects()
