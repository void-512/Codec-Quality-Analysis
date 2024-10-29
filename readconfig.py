import pandas as pd
import pickle
import configparser
import tempfile
import os
import shutil
import sys

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

    pwd = None

    if not configObj.has_section('workdir') or not configObj.has_option('workdir', 'dir'):

        pwd = ensureEnv(None, configObj, cfg)
    else:
        pwd = configObj.get('workdir', 'dir')
        ensureEnv(pwd, configObj, cfg)

    os.chdir(pwd)
    
    pklNameList = []
    pklExtensionList = []
    pklCodecList = []
    pklBitratesList = []

    # Unify upper/lower cases
    for i in range(len(codecsList)):
        codecsList[i] = codecsList[i].lower()
    for i in range(len(bitratesList)):
        bitratesList[i] = bitratesList[i].upper()

    for video in videosList:
        videoName, videoExtension = separateExtension(video)
        pklNameList.append(videoName)
        pklExtensionList.append(videoExtension)
    for codec in codecsList:
        pklCodecList.append(codec)
    for bitrate in bitratesList:
        pklBitratesList.append(bitrate)

    dfVideo = pd.DataFrame({'Full Name': videosList, 'Name': pklNameList, 'Extension': pklExtensionList})
    dfCodec = pd.DataFrame({'Codec': pklCodecList})
    dfBitrate = pd.DataFrame({'Bitrate': pklBitratesList})
    return dfVideo, dfCodec, dfBitrate

def ensureEnv(pwd, configObj, cfg):
    if pwd is None:
        folder = 'codec compare environment'
        workdir = os.path.join(tempfile.gettempdir(), folder)
        if not os.path.isdir(workdir):
            os.mkdir(workdir)
        else:
            deleteFolder(workdir)
            os.mkdir(workdir)
        with open(cfg, 'w') as configfile:
            if not configObj.has_section('workdir'):
                configObj.add_section('workdir')
            configObj.set('workdir', 'dir', workdir)
            configObj.write(configfile)
            configfile.close()
    elif not os.path.isdir(pwd):
        os.mkdir(pwd)
        workdir = pwd
    else:
        workdir = pwd

    return workdir

def deleteFolder(path):
    try:
        shutil.rmtree(path)
        return
    except FileNotFoundError:
        return