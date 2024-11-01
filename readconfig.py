import os
import shutil
import pandas as pd
import configparser

# separateExtension(inputFile): Remove the extension name of {inputFile}.
# fileName: string, file name to be processed
# return
#   string: name of file
#   string: extension of file
def separateExtension(fileName):
    extensionLocation = fileName.rfind('.')
    return fileName[:extensionLocation:1], fileName[extensionLocation::1]

# generateConfigDF(cfg): Generate a DataFrame storing the config
# cfg: string, path to the config file
# return
#   DataFrame: file name and file extension of videos
#   DataFrame: desired codecs
#   DataFrame: desired bitrates
def generateConfigDF(cfg):
    configObj = configparser.ConfigParser()
    configObj.read(cfg)
    videosList = configObj.get('config','reference').split()
    codecsList = configObj.get('config','codec').split()
    bitratesList = configObj.get('config','bitrate').split()
    
    srcNameList = []
    srcExtensionList = []
    targetCodecList = []
    destBitrateList = []

    # Unify upper/lower cases
    for i in range(len(codecsList)):
        codecsList[i] = codecsList[i].lower()
    for i in range(len(bitratesList)):
        bitratesList[i] = bitratesList[i].upper()

    for video in videosList:
        videoName, videoExtension = separateExtension(video)
        srcNameList.append(videoName)
        srcExtensionList.append(videoExtension)
    for codec in codecsList:
        targetCodecList.append(codec)
    for bitrate in bitratesList:
        destBitrateList.append(bitrate)

    dfVideo = pd.DataFrame({'Full Name': videosList, 'Name': srcNameList, 'Extension': srcExtensionList})
    dfCodec = pd.DataFrame({'Codec': targetCodecList})
    dfBitrate = pd.DataFrame({'Bitrate': destBitrateList})
    return dfVideo, dfCodec, dfBitrate

# deleteFolder(path): delete folder at {path} and all of its contents
# path: string, path to target
def deleteFolder(path):
    try:
        shutil.rmtree(path)
        return
    except FileNotFoundError:
        return