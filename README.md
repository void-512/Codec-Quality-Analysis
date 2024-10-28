# A codec quality comparison program
Depends on pandas to analysis data and matplotlib to graph

Requires ffmpeg in the system to transcode and make PSNR logs

Usage:

1. Put your video in the same folder with .py files

2. create a "input.txt" file in the format:

video1 video2

codec1 codec2

bitrate1 bitrate2

3.
run "python generate log.py" for log generation

run "python graph generation.py" for PSNR graphs
