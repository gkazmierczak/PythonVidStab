import converter
import xd2
import cv2
from tkinter import Tk, messagebox
from tkinter.filedialog import askopenfilename, asksaveasfile

if __name__ == "__main__":
    Tk().withdraw()
    inputFilePath = askopenfilename(title="Select file to convert")
    if inputFilePath == "":
        messagebox.showerror("File error", "No file selected")
        exit(-1)
    outputFilePath = asksaveasfile(title="Save file as")
    if outputFilePath == None:
        messagebox.showerror("File error", "No path specified")
        exit(-1)
    # greyscale.convertToGreyscale(inputFilePath,outputFilePath.name,compress=True)
    videoCapture = cv2.VideoCapture(inputFilePath)
    inputFramerate = videoCapture.get(cv2.CAP_PROP_FPS)
    frames = converter.videoToFrameList(videoCapture)
    # for i in range(len(frames)):
    #     frames[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
    stabilized_fames = xd2.stabilize(frames)
    converter.writeVideoToFile(outputFilePath.name, stabilized_fames, 30, True)