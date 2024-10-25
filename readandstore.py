import pandas as pd
import pickle

# separateExtension(inputFile): Remove the extension name of {inputFile}.
# fileName: string, file name to be processed
# return
#   string: name of file
#   string: extension of file
def separateExtension(fileName):
    extensionLocation = fileName.rfind('.')
    return fileName[:extensionLocation:1], fileName[extensionLocation::1]

# generateConfigDF(configFileName): Generate a DataFrame storing the config
# configFileName: string, path to the config file
# return
#   DataFrame: file name and file extension of videos
#   DataFrame: desired codecs
#   DataFrame: desired bitrates
def generateConfigDF(configFileName):
    pklNameList = []
    pklExtensionList = []
    pklCodecList = []
    pklBitratesList = []

    # Read config
    file = open(configFileName, 'r')
    videosList = file.readline().split()
    codecsList = file.readline().split()
    bitratesList = file.readline().split()

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

def storeConfigToPKL(dfVideo, dfCodec, dfBitrate):
    with open('data.pkl', 'wb') as file:
        pickle.dump((dfVideo, dfCodec, dfBitrate), file)