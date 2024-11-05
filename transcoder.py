import os
import ffmpeg
import readconfig
import subprocess
import pandas as pd

# singleVideoGenerator(originalVideo, codec, bitrate, path): Generate videos with desired codec and bitrate.
# originalVideo: string, path to video as reference
# codec: string, desired codec name
# bitrate: string, desired bitrate
# path: string, folder that the generated video will be stored
# parm: string, parameter to ffmpeg when transcoding the video
# return string: name of generated video
def singleVideoGenerator(originalVideo, codec, bitrate, path, parm):
    outputFileName = bitrate + '.mp4'
    outputPath = os.path.join(path, outputFileName)

    command = [
        'ffmpeg',
        '-i', originalVideo,
        '-vcodec', codec,
        '-b:v', bitrate,
        '-bufsize', str(2 * int(bitrate[:-1])) + bitrate[-1],
        '-an',
        '-loglevel', 'quiet',
        outputPath
    ]

    command = command[:5] + parm + command[5:]

    if not os.path.isfile(outputPath):
        try:
            subprocess.run(command, check=True)
            print(f"Generation success: {outputPath}, actual bitrate {getBitrate(outputPath)}")
        except subprocess.CalledProcessError as e:
            print(f"An error occurred while running FFmpeg: {e.stderr}")
            
    else:
        print(f"{outputPath} already existed, skip")
    
    return outputFileName

# videosGenerator(originalVideos, codecs, bitrates): Generate videos with desired codecs and bitrates, 
# each video will have a result with every codec and bitrate from parameter list.
# dfVideo: DataFrame, names of reference videos
# dfCodec: DataFrame, names of desired codecs
# dfBitrate: DataFrame, desired bitrates
# return DataFrame: stores the position information of videos and logs
def videosGenerator(dfVideo, dfCodec, dfBitrate):
    references = dfVideo['Full Name']
    labelList = dfCodec['Label']
    bitrates = dfBitrate['Bitrate']

    originalVideoNames = []
    originalVideoPath = []
    currentVideoPath = []
    labels = []
    currentVideoBitrate = []
    currentVideoLogLocation = []

    for inputVideo in references:
        for label in labelList:
            codec = dfCodec.loc[dfCodec['Label'] == label, 'Codec'].values[0]
            parm = dfCodec.loc[dfCodec['Label'] == label, 'Parm'].values[0]
            originalVideoName = os.path.basename(readconfig.separateExtension(inputVideo)[0])
            foldername = os.path.basename(originalVideoName) + '_' + label
            
            if not os.path.exists(foldername):
                os.makedirs(foldername)

            for bitrate in bitrates:
                generatedVideoFullName = singleVideoGenerator(inputVideo, codec, bitrate, foldername, parm)
                currentVideoPwd = os.path.join(foldername, generatedVideoFullName)
                originalVideoNames.append(originalVideoName)
                originalVideoPath.append(inputVideo)
                currentVideoPath.append(currentVideoPwd)
                labels.append(label)
                currentVideoBitrate.append(getBitrate(currentVideoPwd))
                currentVideoLogLocation.append('logs' + '/' + foldername + '_' + bitrate + '.log')

    df = pd.DataFrame({'Reference Name': originalVideoNames,
                        'Reference Path': originalVideoPath,
                        'Current Path': currentVideoPath,
                        'Label': labels,
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