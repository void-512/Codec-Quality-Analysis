# A codec quality comparison program

A program for you to compare PSNR of video encoders under different bitrates

## How to generate data
Write a config file as the "example.cfg" in the repo.

Each video will have a transcoded version with given codecs and bitrates, so the total number of generated videos will be reference x codec x bitrate

The following command will generate logs and store the PSNR data into "data.pkl" file:
> codec-compare -c example.cfg log

If you want to export the data to merge with other data, you can use "-export" option:
> codec-compare -c example.cfg log -export data.pkl

The program will skip logs that already have been generated, so if you want to generate log and overwrite original file, you can use "-noskip" option:
> codec-compare -c example.cfg log -noskip

## How to graph
You'll need a 'data.pkl' file in the work directory

Show the plot with following command:
> codec-compare graph

If you want to save the figure to system, or in some situations the figure cannot be shown, use the "-save" command to save it to the system:
> codec-compare graph -save result.png

## How to merge data
If you want to merge the data with the data generated elsewhere, you can use the "merge" command:
> codec-compare merge -i <.pkl files>

The command will generate a new "data.pkl" at the work folder

## How to clean the work folder
The "clean" command will delete logs folder and all videos generated:
> codec-compare clean