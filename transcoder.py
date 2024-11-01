import os
import readconfig
import pandas as pd
import ffmpeg
import subprocess

# singleVideoGenerator(originalVideo, codec, bitrate, path): Generate videos with desired codec and bitrate.
# originalVideo: string, path to video as reference
# codec: string, desired codec name
# bitrate: string, desired bitrate
# return string: name of generated video
def singleVideoGenerator(originalVideo, codec, bitrate, path):
    outputFileName = codec + '_' + bitrate + '.mp4'
    outputPath = os.path.join(path, outputFileName)

    command = [
        'ffmpeg',
        '-i', originalVideo,
        '-vcodec', codec,
        '-b:v', bitrate,
        '-bufsize', str(2 * int(bitrate[:-1])) + bitrate[-1],
        '-an',
        outputPath
    ]

    if not os.path.isfile(path + outputFileName):
        try:
            subprocess.run(command, check=True)
            print(f"Generation success: {outputFileName}, actual bitrate {getBitrate(outputPath)}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running FFmpeg: {e.stderr}")
            
    else:
        print(f"{outputFileName} already existed, skip")
    
    return outputFileName

# videosGenerator(originalVideos, codecs, bitrates): Generate videos with desired codecs and bitrates, 
# each video will have a result with every codec and bitrate from parameter list.
# originalVideos: list, names of reference videos
# codecs: list, names of desired codecs
# bitrates: list, desired bitrates
# return DataFrame: stores the position information of videos and logs
def videosGenerator(originalVideos, codecs, bitrates):
    originalVideoNames = []
    originalVideoPath = []
    currentVideoPath = []
    currentVideoCodec = []
    currentVideoBitrate = []
    currentVideoLogLocation = []

    for inputVideo in originalVideos:
        for codec in codecs:
            originalVideoName = os.path.basename(readconfig.separateExtension(inputVideo)[0])
            foldername = os.path.basename(originalVideoName) + '_' + codec
            
            if not os.path.exists(foldername):
                os.makedirs(foldername)

            for bitrate in bitrates:
                generatedVideoFullName = singleVideoGenerator(inputVideo, codec, bitrate, foldername + '/')
                currentVideoPwd = os.path.join(foldername, generatedVideoFullName)
                originalVideoNames.append(originalVideoName)
                originalVideoPath.append(inputVideo)
                currentVideoPath.append(currentVideoPwd)
                currentVideoCodec.append(codec)
                currentVideoBitrate.append(getBitrate(currentVideoPwd))
                currentVideoLogLocation.append('logs' + '/' + foldername + '_' + bitrate + '.log')
                os.path.join('logs', foldername + '_' + bitrate + '.log')

    df = pd.DataFrame({'Reference Name': originalVideoNames,
                        'Reference Path': originalVideoPath,
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