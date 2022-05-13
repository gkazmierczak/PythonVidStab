import cv2
from cv2 import selectROIs


class Tracker:
    def __init__(self, frames):
        self.frames = frames
        self.bbox = self.select_single_bounding_box(0)

    def select_single_bounding_box(self, frame):
        """
        Allows user to select a rectangle bounding an object
        @param frame : input video frame number

        Returns:
            Tuple containing bounding box data (x, y, width, height)
        """

        if not frame < len(self.frames) or frame < 0:
            raise Exception("Wrong frame number")

        bbox = cv2.selectROI(self.frames[frame], False)
        cv2.destroyAllWindows()
        return bbox

    def track(self, mode, display=False):
        """
        Tracks object inside selected bounding box and returns object BBox positions in each frame
        @param mode: str - Tracker mode, influences tracking speed and precision
        @param display: bool - Enable/disable displaying tracking image

        Returns:
            array conatining tracker location of bounding boxes for each frame
        """

        bbox = self.bbox

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

        tracker.init(self.frames[0], bbox)

        tracking_data = [bbox]
        for i in range(1, len(self.frames)):
            frame = self.frames[i]

            # print(bbox)
            # append bbox data to return array and read the next frame
            tracking_data.append(bbox)
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
                cv2.putText(frame, mode + " Tracker", (0, 20), cv2.FONT_HERSHEY_PLAIN, 0.75, (255, 255, 255), 2)
                cv2.imshow("Tracking", frame)

                # exit if ESC pressed
                k = cv2.waitKey(1) & 0xff
                if k == 27:
                    break

        cv2.destroyAllWindows()
        return tracking_data