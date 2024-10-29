import pandas as pd
import re
import matplotlib.pyplot as plt
import os
import sys

# loadPickle(pkl): load dataframe from pkl  and make necessary process for graphing
# pkl: string, path to .pkl file
# return DataFrame: DataFrame necessary for graphing
def loadPickle(pkl):
    graphingDF = pd.read_pickle('data.pkl')
    graphingDF.drop(['Reference Path', 'Current Path'], axis=1, inplace=True)
    # Use the actual bitrate instead, so comment out the conversion of theoretical bitrate
    # graphingDF['Bitrate'] = graphingDF['Bitrate'].apply(convertToNumeric)
    return graphingDF

# convertToNumeric(value): change the bitrate '1k' '2m' to corresponding numeric values
# value: string, bitrate
# return float: numeric value of bitrate
def convertToNumeric(value):
    if value.endswith(('k', 'K')):
        return float(value[:-1]) * 1_000
    elif value.endswith(('m', 'M')):
        return float(value[:-1]) * 1_000_000
    elif value.endswith(('g', 'G')):
        return float(value[:-1]) * 1_000_000_000
    else:
        return float(value)

# getAvgPSNR(logFile): calculate the PSNR based on 1 log
# logFile: string, path to log
# return float: average PSNR in the log
def getAvgPSNR(logFile):
    frameAvgList = []
    pattern = r'psnr_avg:(\d+\.\d+)'
    try:
        with open(logFile, 'r') as file:
            for line in file:
                match = re.search(pattern, line)
                if match:
                    framePSNR = float(match.group(1))
                    frameAvgList.append(framePSNR)
    except FileNotFoundError:
        sys.exit(f"The log \'{logFile}\' doesn't exist, please run the log generation first")

    if len(frameAvgList) == 0:
        os.remove(logFile)
        sys.exit("Error in log file, please generate the log again")
        
    return sum(frameAvgList) / len(frameAvgList)

# getAllPSNR(df): add a column of PSNR for all logs in df
# df: DataFrame of log information
def getAllPSNR(df):
    PSNR = []
    for log in df['Log Location']:
        PSNR.append(getAvgPSNR(log))
    df['PSNR'] = PSNR

# generateGraph(df): generate graphs with given Data Frame
# df: DataFrame with necessary information
def generateGraph(df):
    referenceList = df['Reference Name'].unique()
    codecList = df['Codec'].unique()
    for video in referenceList:
        plt.figure(figsize=(10, 6))
        plt.title(f'PSNR vs Bitrate for {video}')
        plt.xlabel('Bitrate')
        plt.ylabel('PSNR (dB)')
        filterByVideo = df[df['Reference Name'] == video]
        for codec in codecList:
            filterByCodec = filterByVideo[filterByVideo['Codec'] == codec]
            plt.plot(filterByCodec['Bitrate'], filterByCodec['PSNR'], label=f'Codec: {codec}', marker='o')
        plt.legend()
        plt.grid(True)
    # windwos cannot display figure
    # plt.savefig('pic.png')
    plt.show()

graphingDF = loadPickle('data.pkl')
getAllPSNR(graphingDF)
generateGraph(graphingDF)