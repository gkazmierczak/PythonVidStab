import cv2
import numpy as np
import ffmpeg
from typing import List
from cv2 import VideoCapture
import tempfile
import shutil
import converter

SMOOTHING_RADIUS = 60


def movingAverage(curve, radius):
    window_size = 2 * radius + 1
    f = np.ones(window_size)/window_size
    curve_pad = np.lib.pad(curve, (radius, radius), 'edge')
    curve_smoothed = np.convolve(curve_pad, f, mode='same')
    curve_smoothed = curve_smoothed[radius:-radius]
    return curve_smoothed


def smooth(trajectory):
    smoothed_trajectory = np.copy(trajectory)
    # Filter the x, y and angle curves
    for i in range(3):
        smoothed_trajectory[:, i] = movingAverage(
            trajectory[:, i], radius=SMOOTHING_RADIUS)

    return smoothed_trajectory


def fixBorder(frame, borderMode):

    s = frame.shape
    # Scale the image without moving the center
    T = cv2.getRotationMatrix2D((s[1]/2, s[0]/2), 0, 1.05)
    frame = cv2.warpAffine(
        frame, T, (s[1], s[0]), borderMode=borderMode)
    return frame


def stabilize(frames: List, borderMode=cv2.BORDER_REPLICATE):
    colorFrames = frames
    frames = []
    for frame in colorFrames:
        frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY))
    frameCount = len(frames)
    transformsArr = np.zeros((frameCount-1, 3), np.float32)
    for i in range(frameCount-2):
        prevPoints = cv2.goodFeaturesToTrack(
            frames[i], maxCorners=200, qualityLevel=0.1, minDistance=10, blockSize=1)
        currPoints, status, err = cv2.calcOpticalFlowPyrLK(
            frames[i], frames[i+1], prevPoints, None)
        assert prevPoints.shape == currPoints.shape

        idx = np.where(status == 1)[0]
        prevPoints = prevPoints[idx]
        currPoints = currPoints[idx]
        m = cv2.estimateAffinePartial2D(prevPoints, currPoints)
        dx = m[0][0][2]
        dy = m[0][1][2]
        # Extract rotation angle
        da = np.arctan2(m[0][1][0], m[0][0][0])
        transformsArr[i] = [dx, dy, da]
    trajectory = np.cumsum(transformsArr, axis=0)
    print(trajectory)
    smoothed_trajectory = smooth(trajectory)
    difference = smoothed_trajectory - trajectory
    transforms_smooth = transformsArr + difference
    frameSize = (len(frames[0][0]), len(frames[0]))
    stabilized_frames = []
    for i in range(frameCount-2):
        # Read next frame

        # Extract transformations from the new transformation array
        dx = transforms_smooth[i, 0]
        dy = transforms_smooth[i, 1]
        da = transforms_smooth[i, 2]

        # Reconstruct transformation matrix accordingly to new values
        m = np.zeros((2, 3), np.float32)
        m[0, 0] = np.cos(da)
        m[0, 1] = -np.sin(da)
        m[1, 0] = np.sin(da)
        m[1, 1] = np.cos(da)
        m[0, 2] = dx
        m[1, 2] = dy

        # Apply affine wrapping to the given frame
        frame_stabilized = cv2.warpAffine(
            colorFrames[i], m, frameSize, borderMode=borderMode)
        stabilized_frames.append(frame_stabilized)
        # Fix border artifacts
        # frame_stabilized = fixBorder(frame_stabilized, borderMode)

    return stabilized_frames