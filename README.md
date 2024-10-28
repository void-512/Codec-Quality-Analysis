# A codec quality comparison program
Depends on pandas to analysis data and matplotlib to graph

Requires ffmpeg in the system to transcode and make PSNR logs

Usage:

Put your video in the same folder with .py files

create a "input.txt" file in the format:
video1 video2
codec1 codec2
bitrate1 bitrate2

run "python generate log.py" for log generation
run "graph generation.py" for PSNR graphs
