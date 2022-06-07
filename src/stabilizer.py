import numpy as np
import matplotlib.pyplot as plt


class Stabilizer:
    def __init__(self, frames, data):
        self.data = data
        self.frames = frames

        if len(self.frames) != len(self.data):
            raise Exception("Length of tracker data should be equal number of frames")
        self.n = len(self.frames)

    def stabilize(self, smoothing_radius=10, generate_plots=False):
        """
        Stabilizes video (self.frames) based on tracker data saved in self.data.

        @param smoothing_radius: int - Number of frames from which average will be taken to smoothen video
        @param generate_plots: bool - Enable/disable smoothing plots generation
        """

        width = self.frames[0].shape[1]
        height = self.frames[0].shape[0]

        trajectory = np.array([[int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)] for bbox in self.data])

        non_zero = trajectory[0]
        for i in range(1, len(trajectory)):
            if trajectory[i][0] == 0 and trajectory[i][1] == 0:
                trajectory[i] = non_zero
            else:
                non_zero = trajectory[i]

        if generate_plots:
            plt.subplot(2, 1, 1)
            plt.plot([x[0] for x in trajectory], [x[1] for x in trajectory], marker='.', color='r')

        self.trajectory_smooth(trajectory, smoothing_radius)

        if generate_plots:
            plt.subplot(2, 1, 2)
            plt.plot([x[0] for x in trajectory], [x[1] for x in trajectory], marker='.', color='g')
            plt.savefig("../plots/trajectory_smooth.png")

        margin_x = min(np.min(trajectory[:, 0]), np.min(width - trajectory[:, 0])) - 1
        margin_y = min(np.min(trajectory[:, 1]), np.min(height - trajectory[:, 1])) - 1

        for i, frame in enumerate(self.frames):
            x, y = trajectory[i]
            self.frames[i] = frame[y - margin_y:y + margin_y, x - margin_x:x + margin_x]

    @staticmethod
    def trajectory_smooth(trajectory, n):
        """
        Creates smoothen trajectory by taking an average of n frames.

        @param trajectory: list - Trajectory to be smoothened
        @param n: int - Number of frames from which average will be taken to smoothen trajectory
        """
        curr_sum_x = np.sum(trajectory[:n, 0])
        curr_sum_y = np.sum(trajectory[:n, 1])
        x = []
        y = []

        for i in range(n, len(trajectory)):
            curr_sum_x -= trajectory[i - n, 0]
            curr_sum_x += trajectory[i, 0]
            curr_sum_y -= trajectory[i - n, 1]
            curr_sum_y += trajectory[i, 1]

            x.append(curr_sum_x // n)
            y.append(curr_sum_y // n)

        first = n // 2
        trajectory[first:first + len(x), 0] = x
        trajectory[first:first + len(y), 1] = y
