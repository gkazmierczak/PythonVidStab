import cv2
import ffmpeg
import os
from typing import List
from cv2 import VideoCapture


def convertToGreyscale(inputVideoPath:str, outputVideoName:str) -> None:
    videoCapture = cv2.VideoCapture(inputVideoPath)
    inputFramerate = videoCapture.get(cv2.CAP_PROP_FPS)
    frames = videoToFrameList(videoCapture)
    for i in range(len(frames)):
        frames[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
    tempfileName="vid_tempfile.mp4"
    writeVideoToFile(tempfileName, frames, inputFramerate, iscolor=False)
    muxVideoAudio(tempfileName, inputVideoPath, outputVideoName)
    os.remove(tempfileName)


def videoToFrameList(videoCapture: VideoCapture) -> List:
    frames = []
    ret, frame = videoCapture.read()
    while ret:
        frames.append(frame)
        ret, frame = videoCapture.read()
    return frames


def writeVideoToFile(outputVideoName:str, frames:List, framerate:float, iscolor:bool=True) -> None:
    frameSize = (len(frames[0][0]), len(frames[0]))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output = cv2.VideoWriter(outputVideoName, fourcc,
                             framerate, frameSize, iscolor)
    for frame in frames:
        output.write(frame)
    output.release()


def muxVideoAudio(videofilePath:str, audiofilePath:str, outputVideoName:str) -> None:
    inputVideo = ffmpeg.input(videofilePath)
    inputAudio = ffmpeg.input(audiofilePath)
    ffmpeg.concat(inputVideo, inputAudio, v=1, a=1).output(outputVideoName,vcodec='libx264').overwrite_output().run()
