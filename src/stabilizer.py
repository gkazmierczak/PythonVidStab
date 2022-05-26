import numpy as np
import matplotlib.pyplot as plt


class Stabilizer:
    def __init__(self, frames, data):
        self.data = data
        self.frames = frames

        if len(self.frames) != len(self.data):
            raise Exception("Length of tracker data should be equal number of frames")
        self.n = len(self.frames)

    def stabilize(self,smoothingRadius=30,generatePlots=False):
        width = self.frames[0].shape[1]
        height = self.frames[0].shape[0]

        trajectory = np.array([[int(bbox[0] + bbox[2] / 2), int(bbox[1] + bbox[3] / 2)] for bbox in self.data])
        # print(trajectory)

        if generatePlots:
            plt.plot([x[0] for x in trajectory], [x[1] for x in trajectory], marker='.', color='r')

        self.trajectory_smooth(trajectory, smoothingRadius)

        if generatePlots:
            plt.plot([x[0] for x in trajectory], [x[1] for x in trajectory], marker='.', color='g')
            plt.savefig("after.png")

        margin_x = min(np.min(trajectory[:, 0]), np.min(width - trajectory[:, 0])) - 1
        margin_y = min(np.min(trajectory[:, 1]), np.min(height - trajectory[:, 1])) - 1

        for i, frame in enumerate(self.frames):
            x, y = trajectory[i]
            self.frames[i] = frame[y - margin_y:y + margin_y, x - margin_x:x + margin_x]

    @staticmethod
    def trajectory_smooth(trajectory, n):
        curr_sum_x = np.sum(trajectory[:n, 0])
        curr_sum_y = np.sum(trajectory[:n, 1])
        x = []
        y = []

        for i in range(10, len(trajectory)):
            curr_sum_x -= trajectory[i - n, 0]
            curr_sum_x += trajectory[i, 0]
            curr_sum_y -= trajectory[i - n, 1]
            curr_sum_y += trajectory[i, 1]

            x.append(curr_sum_x // n)
            y.append(curr_sum_y // n)

        first = n // 2
        trajectory[first:first + len(x), 0] = x
        trajectory[first:first + len(y), 1] = y
