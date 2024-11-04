# A codec quality comparison program

A tool for evaluating and comparing the PSNR (Peak Signal-to-Noise Ratio) of various video encoders at different bitrates

FFMPEG is required in the system

Make sure the "_internal" folder is in the same directory as the executable file

## Configuration File Setup

The configuration file defines the parameters for generating PSNR logs

The example.cfg is an example of config

Format:

> [config]

> reference = video1 video2 ...

> bitrate = bitrate1 bitrate2 ...

> [codec]

> <codec_name> = <codec> <parameters>

[config] section:

reference: Lists the video files to be used as references.

bitrate: Specifies the target bitrates for encoding each video.

[codec] section:

Define each codec with an optional name label and any additional parameters. The codec name label will appear in generated graphs.

## How to generate data

Each video will have a transcoded version with given label and bitrates, so the total number of generated videos will be reference x label x bitrate

The following command will generate logs and store the PSNR data into "data.pkl" file:
> codec-compare -c example.cfg log

To export the data, use "-export" option:
> codec-compare -c example.cfg log -export data.pkl

The program will skip logs that already have been generated, to generate log and overwrite original logs, use "-noskip" option:
> codec-compare -c example.cfg log -noskip

## How to graph
Make sure a "data.pkl" exists in the work directory

Show the plot with following command:
> codec-compare graph

To save the figure to system, or in some situations the figure cannot be shown, use the "-save" command to save it to the system:
> codec-compare graph -save result.png

## How to merge data
To merge the data generated by different operations, use the "merge" command:
> codec-compare merge -i <.pkl files>

The command will generate a new "data.pkl" at the work folder

## How to clean the work folder
The "clean" command will delete logs folder and all videos generated:
> codec-compare -c example.cfg clean

# How the release version is built?
Need pandas, ffmpeg-python, matplotlib, and pyinstaller

Build with command:
> pyinstaller codec-compare.py -p graphGeneration.py -p psnr.py -p readconfig.py -p transcoder.py
