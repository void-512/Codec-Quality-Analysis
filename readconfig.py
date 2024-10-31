import pandas as pd
import configparser
import tempfile
import os
import shutil

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

    '''

    pwd = None

    if not configObj.has_section('workdir') or not configObj.has_option('workdir', 'dir'):
        pwd = ensureEnv(None, cfg)
    else:
        pwd = configObj.get('workdir', 'dir')
        ensureEnv(pwd, cfg)

    os.chdir(pwd)
    '''
    
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

# ensureEnv(pwd, cfg): check if work directory exists. If pwd doesn't exist, use the default TEMP folder
#   and write to the config file. If pwd exist, doesn't do anything.
# pwd: string, path to work directory
# cfg: string, path to config file
# return string: path to work directory
def ensureEnv(pwd, cfg):
    if pwd is None:
        folder = 'codec compare environment'
        workdir = os.path.join(tempfile.gettempdir(), folder)
        if not os.path.isdir(workdir):
            os.mkdir(workdir)
        else:
            deleteFolder(workdir)
            os.mkdir(workdir)

        with open(cfg, 'w') as configfile:
            configObj = configparser.ConfigParser()
            configObj.read(cfg)
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

# deleteFolder(path): delete folder at {path} and all of its contents
# path: string, path to target
def deleteFolder(path):
    try:
        shutil.rmtree(path)
        return
    except FileNotFoundError:
        return