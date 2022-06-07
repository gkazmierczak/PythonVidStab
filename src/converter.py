import cv2
import ffmpeg
import tempfile
import shutil


def convert_frames_to_greyscale(frames):
    """
    Converts video frames to greyscale
    @param frames: list - List of video frames
    """
    for i in range(len(frames)):
        frames[i] = cv2.cvtColor(frames[i], cv2.COLOR_BGR2GRAY)


def create_video_capture(input_video_path):
    """
    Creates cv2.VideoCapture object of given video file.
    @param input_video_path: str - Input video file path

    Returns:
        cv2.VideoCapture object of video given by path
    """
    return cv2.VideoCapture(input_video_path)


def video_to_frame_list(video_capture):
    """
    Reads frames from cv2.VideoCapture object.
    @param video_capture: cv2.VideoCapture - VideoCapture object

    Returns:
        List containing video frames
    """
    frames = []
    ret, frame = video_capture.read()
    while ret:
        frames.append(frame)
        ret, frame = video_capture.read()
    return frames


def write_video_to_file(output_video_name, frames, framerate, iscolor=True):
    """
    Writes video represented by frames to a file.
    @param output_video_name: str -
    @param frames: list -
    @param framerate: float -
    @param iscolor: bool -
    """
    frameSize = (len(frames[0][0]), len(frames[0]))
    fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
    output = cv2.VideoWriter(output_video_name, fourcc, framerate, frameSize, iscolor)

    for frame in frames:
        output.write(frame)
    output.release()


def mux_video_audio(videofile_path, audiofile_path, output_video_name):
    """
    Add audio to video file
    @param videofile_path: str - Input video file path
    @param audiofile_path: str - Input audio file path
    @param output_video_name: str - Output video file path
    """
    input_video = ffmpeg.input(videofile_path)
    input_audio = ffmpeg.input(audiofile_path)
    ffmpeg.concat(input_video, input_audio, v=1, a=1).output(output_video_name, vcodec="libx264").overwrite_output().run()


def repack_video(video_path):
    """
    Compress video
    @param video_path: str - Input video file path
    """
    tempdir_path = tempfile.mkdtemp()
    tempfile_name = tempdir_path + "\\tempfile.mp4"
    ffmpeg.input(video_path).output(tempfile_name, vcodec="libx264").run()
    shutil.move(tempfile_name, video_path)
    shutil.rmtree(tempdir_path)

def contains_audio(video_path):
    """
        Check if video has an audio track.
        @param video_path: str - Path to tested video
        Returns:
            bool - True if video has an audio track.
    """
    probe=ffmpeg.probe(video_path,select_streams='a')
    return probe['streams']
