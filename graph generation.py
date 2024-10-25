import pandas as pd
import re

# loadPickle(pkl): load dataframe from pkl  and make necessary process for graphing
# pkl: string, path to .pkl file
# return DataFrame: DataFrame necessary for graphing
def loadPickle(pkl):
    graphingDF = pd.read_pickle('data.pkl')
    graphingDF.drop(['Reference Path', 'Current Path'], axis=1, inplace=True)
    graphingDF['Bitrate'] = graphingDF['Bitrate'].apply(convertToNumeric)
    return graphingDF

# convertToNumeric(value): change the bitrate '1k' '2m' to corresponding numeric values
# value: string, bitrate
# return float: numeric value of bitrate
def convertToNumeric(value):
    if value.endswith('K'):
        return float(value[:-1]) * 1_000
    elif value.endswith('M'):
        return float(value[:-1]) * 1_000_000
    elif value.endswith('G'):
        return float(value[:-1]) * 1_000_000_000
    else:
        return float(value)

# getAvgPSNR(logFile): calculate the PSNR based on 1 log
# logFile: string, path to log
# return float: average PSNR in the log
def getAvgPSNR(logFile):
    frameAvgList = []
    pattern = r'psnr_avg:(\d+\.\d+)'
    with open(logFile, 'r') as file:
        for line in file:
            match = re.search(pattern, line)
            if match:
                framePSNR = float(match.group(1))
                frameAvgList.append(framePSNR)
    return sum(frameAvgList) / len(frameAvgList)

# getAllPSNR(df): add a column of PSNR for all logs in df
# df: DataFrame of log information
def getAllPSNR(df):
    PSNR = []
    for log in df['Log Location']:
        PSNR.append(getAvgPSNR(log))
    df['PSNR'] = PSNR

graphingDF = loadPickle('data.pkl')
grouped = graphingDF.groupby(['Reference Name', 'Codec'])

getAllPSNR(graphingDF)
    
for group_name, group_data in grouped:
    print(f"Group: {group_name}")
    print(group_data)
    print()

