import cv2
import ffmpeg
from typing import List
from cv2 import VideoCapture
import tempfile
import shutil


def convertToGreyscale(inputVideoPath: str, outputVideoName: str, compress: bool) -> None:
    videoCapture = cv2.VideoCapture(inputVideoPath)
    inputFramerate = videoCapture.get(cv2.CAP_PROP_FPS)
    frames = videoToFrameList(videoCapture)
    for i in range(len(frames)):
        frames[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)
    if ffmpeg.probe(inputVideoPath, select_streams='a')['streams']:
        tempdirPath = tempfile.mkdtemp()
        tempfileName = tempdirPath + "\\tempfile.mp4"
        writeVideoToFile(tempfileName, frames, inputFramerate, iscolor=False)
        muxVideoAudio(tempfileName, inputVideoPath, outputVideoName)
        shutil.rmtree(tempdirPath)
    else:
        writeVideoToFile(outputVideoName, frames, inputFramerate, iscolor=False)
        if compress:
            repackVideo(outputVideoName)


def convertFramesToGreyscale(frames: List) -> None:
    for i in range(len(frames)):
        frames[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)


def createVideoCapture(inputVideoPath: str) -> cv2.VideoCapture:
    return cv2.VideoCapture(inputVideoPath)


def videoToFrameList(videoCapture: VideoCapture) -> List:
    frames = []
    ret, frame = videoCapture.read()
    while ret:
        frames.append(frame)
        ret, frame = videoCapture.read()
    return frames


def writeVideoToFile(outputVideoName: str, frames: List, framerate: float, iscolor: bool = True) -> None:
    frameSize = (len(frames[0][0]), len(frames[0]))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output = cv2.VideoWriter(outputVideoName, fourcc,
                             framerate, frameSize, iscolor)
    for frame in frames:
        output.write(frame)
    output.release()


def muxVideoAudio(videofilePath: str, audiofilePath: str, outputVideoName: str) -> None:
    inputVideo = ffmpeg.input(videofilePath)
    inputAudio = ffmpeg.input(audiofilePath)
    ffmpeg.concat(inputVideo, inputAudio, v=1, a=1).output(
        outputVideoName, vcodec="libx264").overwrite_output().run()


def repackVideo(videoPath: str) -> None:
    tempdirPath = tempfile.mkdtemp()
    tempfileName = tempdirPath + "\\tempfile.mp4"
    ffmpeg.input(videoPath).output(tempfileName, vcodec="libx264").run()
    shutil.move(tempfileName, videoPath)
    shutil.rmtree(tempdirPath)
