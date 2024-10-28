import os
import subprocess
import readandstore
import pandas as pd
import ffmpeg

# singleVideoGenerator(originalVideo, codec, bitrate, path): Generate videos with desired codec and bitrate.
# originalVideo: string, path to video as reference
# codec: string, desired codec name
# bitrate: string, desired bitrate
# return string: name of generated video
def singleVideoGenerator(originalVideo, codec, bitrate, path):

    outputFileName = codec + '_' + bitrate + '.mp4'

    try:
        command = [
            'ffmpeg',
            '-i', originalVideo,
            '-c:v', codec,                              # Desired codec
            '-b:v', bitrate,                            # Desired bitrate
            '-an',                                      # Mute
            path + outputFileName                      # Output file 
        ]

        # Ensure HEVC video playable on QuickTime Player
        if (codec.find('hevc') != -1) or (codec.find('265') != -1):
            command.insert(-1, '-vtag')
            command.insert(-1, 'hvc1')

        if not os.path.isfile(path + outputFileName):
            subprocess.run(command, check=True)
            print(f"Generation success: {outputFileName}")
        else:
            print(f"{outputFileName} already exist, skip")

    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running FFmpeg: {e}")
    
    return outputFileName

# videosGenerator(originalVideos, codecs, bitrates): Generate videos with desired codecs and bitrates, 
# each video will have a result with every codec and bitrate from parameter list.
# originalVideos: list, names of reference videos
# codecs: list, names of desired codecs
# bitrates: list, desired bitrates
# return DataFrame: stores the position information of videos and logs
def videosGenerator(originalVideos, codecs, bitrates):
    originalVideoNames = []
    originalVideoPaths = []
    currentVideoPath = []
    currentVideoCodec = []
    currentVideoBitrate = []
    currentVideoLogLocation = []

    for inputVideo in originalVideos:
        for codec in codecs:
            originalVideoName = readandstore.separateExtension(inputVideo)[0]
            foldername = originalVideoName + '_' + codec
            
            if not os.path.exists(foldername):
                os.makedirs(foldername)

            for bitrate in bitrates:
                generatedVideoFullName = singleVideoGenerator(inputVideo, codec, bitrate, foldername + '/')
                currentVideoAbsPath = os.path.abspath(foldername + '/' + generatedVideoFullName)
                originalVideoNames.append(originalVideoName)
                originalVideoPaths.append(os.path.abspath(inputVideo))
                currentVideoPath.append(currentVideoAbsPath)
                currentVideoCodec.append(codec)
                currentVideoBitrate.append(getBitrate(currentVideoAbsPath))
                currentVideoLogLocation.append(os.path.abspath('logs') + '/' + originalVideoName + '_' + codec + '_' + bitrate + '.log')

    df = pd.DataFrame({'Reference Name': originalVideoNames,
                        'Reference Path': originalVideoPaths,
                        'Current Path': currentVideoPath,
                        'Codec': currentVideoCodec,
                        'Bitrate': currentVideoBitrate,
                        'Log Location': currentVideoLogLocation})
    return df

# getBitrate(videoFile): return the actual bitrate of video gained from ffprobe
# videoFile: string, path to the target video
# return int: bitrate of video stream
def getBitrate(videoFile):
    try:
        probe = ffmpeg.probe(videoFile)
        for stream in probe['streams']:
            if stream['codec_type'] == 'video':
                return int(stream['bit_rate'])
            else:
                print('No video stream found')
                return None
    except ffmpeg.Error as e:
        print(f"ffmpeg error: {e.stderr.decode()}")
        return None