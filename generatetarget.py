'''
    This file generate the videos with required codec and bitrate.
'''

import os
import subprocess

# Read desired files, codecs, and bitrates
# input_file: string
def readparameter(input_file):
    file = open(input_file, 'r')

    videos = file.readline()
    codecs = file.readline()
    bitrates = file.readline()

    videos_list = videos.split()
    codecs_list = codecs.split()
    bitrates_list = bitrates.split()

    return videos_list, codecs_list, bitrates_list

# Remove the extension name of {input_file}.
# input_file: string
def removeExtension(input_file):
    extensionLocation = input_file.rfind('.')
    return input_file[:extensionLocation:1]

# Generate videos with desired codec and bitrate.
# input_file: string
# codec: string
# bitrate: string
def singleVideoGenerator(input_file, codec, bitrate):

    codec = codec.lower()
    bitrate = bitrate.upper()

    input_name = removeExtension(input_file)

    try:
        command = [
            'ffmpeg',
            '-i', input_file,
            '-c:v', codec,                              # Desired codec
            '-b:v', bitrate,                            # Desired bitrate
            '-an',                                      # Mute
            codec + '_' + bitrate + '.mp4'              # Output file 
        ]

        # Ensure HEVC video playable on QuickTime Player
        if (codec.find('hevc') != -1) or (codec.find('265') != -1):
            command.insert(-1, '-vtag')
            command.insert(-1, 'hvc1')

        # Run the FFmpeg command
        subprocess.run(command, check=True)

        print(f"Generation success: {codec}_{bitrate}.mp4")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running FFmpeg: {e}")

# Generate videos with desired codecs and bitrates, each video will have a result with every codec and bitrate from parameter list.
# input_files: list
# codecs: list
# bitrates: list
def videosGenerator(input_files, codecs, bitrates):
    for input_video in input_files:
        for codec in codecs:
            foldername = removeExtension(input_video) + '_' + codec
            if not os.path.exists(foldername):
                os.makedirs(foldername)
            os.chdir(foldername)
            for bitrate in bitrates:
                singleVideoGenerator('../' + input_video, codec, bitrate)
            os.chdir('..')


videos, codecs, bitrates = readparameter('parameters.txt')
videosGenerator(videos, tcodecs, bitrates)
