# PythonVidStab

Python Video Stabilization project.

To run:
Create virutalenv:
$ python3 -m venv ENV
On windows, run:
$ Set-ExecutionPolicy Unrestricted -Scope Process
$ ENV\Scripts\activate
On Linux:
$source ENV/bin/activate
install all requirements:
$ pip install -r requirements.txt

Depending on configuration, it might also be necessary to download ffmpeg:
https://www.ffmpeg.org/download.html
extract it and drop contents (ffmpeg and ffrpobe) inside ENV\Scripts
