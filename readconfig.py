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
    srcNameList = []
    srcExtensionList = []
    customCodecName = []
    targetCodecList = []
    codecParameterList = []
    destBitrateList = []

    configObj = configparser.ConfigParser()
    configObj.read(cfg)
    videosList = configObj.get('config','reference').split()
    bitratesList = configObj.get('config','bitrate').split()
    
    for name, parm in configObj.items('codec'):
        customCodecName.append(name)
        targetCodecList.append(parm.split()[0])
        codecParameterList.append(parm.split()[1:])

    # Unify upper/lower cases
    for i in range(len(bitratesList)):
        bitratesList[i] = bitratesList[i].upper()

    for video in videosList:
        videoName, videoExtension = separateExtension(video)
        srcNameList.append(videoName)
        srcExtensionList.append(videoExtension)
    for bitrate in bitratesList:
        destBitrateList.append(bitrate)

    dfVideo = pd.DataFrame({'Full Name': videosList, 'Name': srcNameList, 'Extension': srcExtensionList})
    dfCodec = pd.DataFrame({'Custom Codec Name': customCodecName, 'Codec': targetCodecList, 'Parm': codecParameterList})
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