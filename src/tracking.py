import cv2
from cv2 import selectROIs
import numpy as np
from tkinter.filedialog import askopenfilename


def selectSingleBoundingBox(capture):
    """
    Allows user to select a rectangle bounding an object
    @param capture : cv2.VideoCapture - input video capture

    Returns:
        Tuple conatining bounding box data (x,y,width,height) 
    """
    ret, frame = capture.read()
    if not ret:
        print('Cannot read video file')
        exit(0)
    bbox = cv2.selectROI(frame, False)
    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    cv2.destroyAllWindows()
    return bbox


def track(capture, bbox, mode, display=False):
    """
    Tracks object inside selected bounding box and returns object BBox positions in each frame
    @param capture : cv2.VideoCapture - input video capture
    @param bbox : tuple<int>[4] - location and size of the bounding box (x,y,width,height)
    @param mode: str - Tracker mode, influences tracking speed and precision
    @param display: bool - Enable/disable displaying tracking image

    Returns:
        array conatining tracker location of bounding boxes for each frame
    """

    # input check
    assert len(bbox) == 4 and bbox[0] >= 0 and bbox[1] >= 0 and bbox[2] != 0 and bbox[3] != 0
    modes = ['KCF', 'CSRT', 'MOSSE']
    if mode not in modes:
        print("Specified tracking mode not found. Using KCF instead.")
        mode = 'KCF'
    if mode == 'MOSSE':
        tracker = cv2.TrackerMOSSE_create()
    elif mode == 'CSRT':
        tracker = cv2.TrackerCSRT_create()
    else:
        tracker = cv2.TrackerKCF_create()

    # tracker initialization
    ret, frame = capture.read()
    if not ret:
        print('Cannot read video file')
        return -1
    tr = tracker.init(frame, bbox)

    trackingData = []
    while ret:
        # print(bbox)
        # append bbox data to return array and read the next frame
        trackingData.append(bbox)
        ret, frame = capture.read()
        if not ret:
            break
            # update tracker
        tr, bbox = tracker.update(frame)

        # Display tracking image
        if tr and display:
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(frame, p1, p2, (255, 0, 0), 2, 1)

        # tracked object lost
        else:
            # print("Tracker failure in frame: ",int(capture.get(cv2.CAP_PROP_POS_FRAMES)))
            if display:
                cv2.putText(frame, "Tracking failure", (0, 60), cv2.FONT_HERSHEY_PLAIN, 0.75, (0, 0, 255), 2)

        if display:
            cv2.putText(frame, mode + " Tracker", (0, 20), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 2);
            cv2.imshow("Tracking", frame)

            # exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27: break
    cv2.destroyAllWindows()
    return trackingData


def selectMultipleBoundingBoxes(capture):
    """
    Allows user to select rectangles bounding objects on captured frame
    @param capture : cv2.VideoCapture - input video capture

    Returns:
        Array of tuples conatining bounding box data (x,y,width,height) 
    """
    ret, frame = capture.read()
    if not ret:
        print('Cannot read video file')
        exit(0)
    bboxes = selectROIs("Object selection", frame, False)
    capture.set(cv2.CAP_PROP_POS_FRAMES, 0)
    cv2.destroyAllWindows()
    return bboxes


def trackMultiple(capture, bboxes, mode, display=False):
    """
    Tracks objects inside selected bounding boxes and returns objects BBox positions in each frame
    @param capture : cv2.VideoCapture - input video capture
    @param bboxes : array of tuples<int>[4] - locations and sizes of the bounding boxes (x,y,width,height)
    @param mode: str - Tracker mode, influences tracking speed and precision
    @param display: bool - Enable/disable displaying tracking image

    Returns:
        array of arrays conatining tracker location of bounding boxes for each frame
    """

    modes = ['KCF', 'CSRT', 'MOSSE']
    if mode not in modes:
        print("Specified tracking mode not found. Using KCF instead.")
        mode = 'KCF'

    # tracker initialization
    ret, frame = capture.read()
    if not ret:
        print('Cannot read video file')
        return -1
    multiTracker = cv2.legacy.MultiTracker_create()
    if mode == 'MOSSE':
        for bbox in bboxes:
            multiTracker.add(cv2.legacy.TrackerMOSSE_create(), frame, bbox)
    elif mode == 'CSRT':
        for bbox in bboxes:
            multiTracker.add(cv2.legacy.TrackerCSRT_create(), frame, bbox)
    else:
        for bbox in bboxes:
            multiTracker.add(cv2.legacy.TrackerKCF_create(), frame, bbox)
    trackingData = [[bbox] for bbox in bboxes]
    while ret:
        ret, frame = capture.read()

        if not ret:
            break
            # update tracker and display image
        success, boxes = multiTracker.update(frame)
        for i, newbox in enumerate(boxes):
            if success and display:
                p1 = (int(newbox[0]), int(newbox[1]))
                p2 = (int(newbox[0] + newbox[2]), int(newbox[1] + newbox[3]))
                cv2.rectangle(frame, p1, p2, (0, 255, 255), 2, 1)
            elif display:
                cv2.putText(frame, "Tracking failure", (0, 60), cv2.FONT_HERSHEY_PLAIN, 0.75, (0, 0, 255), 2)
            trackingData[i].append(newbox)

        if display:
            cv2.putText(frame, mode + " Tracker", (0, 20), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 2);
            cv2.imshow("Tracking", frame)

            # exit if ESC pressed
            k = cv2.waitKey(1) & 0xff
            if k == 27: break
    cv2.destroyAllWindows()
    return trackingData


inputFilePath = askopenfilename(title="Select file to convert")
capture = cv2.VideoCapture(inputFilePath)
# track(capture, selectSingleBoundingBox(capture), 'CSRT', True)
data = trackMultiple(capture, selectMultipleBoundingBoxes(capture), "CSRT", display=True)
