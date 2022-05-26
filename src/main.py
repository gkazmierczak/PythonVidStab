import converter
from tracker import Tracker
from stabilizer import Stabilizer

import cv2
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile

if __name__ == "__main__":
    # data = trackMultiple(capture, selectMultipleBoundingBoxes(capture), "CSRT", display=True)

    # print("????")
    # stabilizer = Stabilizer(data)

    Tk().withdraw()
    input_file_path = askopenfilename(title="Select file to convert")
    if input_file_path == "":
        messagebox.showerror("File error", "No file selected")
        exit(-1)

    output_file_path = asksaveasfile(title="Save file as")
    if output_file_path is None:
        messagebox.showerror("File error", "No path specified")
        exit(-1)

    capture = cv2.VideoCapture(input_file_path)
    framerate = capture.get(cv2.CAP_PROP_FPS)
    frames = converter.videoToFrameList(capture)

    print("LEN: ", len(frames))
    print(frames[0].shape)

    tracker = Tracker(frames)

    data = tracker.track('KCF', True)
    print("LEN: ", len(data))
    [print(x) for x in data]

    stabilizer = Stabilizer(frames, data)
    stabilizer.stabilize(generate_plots=True)
    print("FRAMES:")
    [print(x) for x in frames]

    # data = tracking.track(capture, tracking.selectSingleBoundingBox(capture), 'CSRT', True)
    converter.writeVideoToFile(output_file_path.name, frames, framerate, True)
