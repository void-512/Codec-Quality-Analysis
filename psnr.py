import os
import re
import sys
import subprocess
import pandas as pd

# generateSingleLog(reference, target, logfile): Generate a PSNR log with given reference and video
# reference: string, path to video as reference
# target: string, path to video to be compared
# logfile: string, path to log that will be generated
def generateSingleLog(reference, target, logfile):
    command = [
        'ffmpeg', '-i', reference, '-i', target,
        '-lavfi', f'psnr=stats_file={logfile}', 
        '-loglevel', 'quiet',
        '-f', 'null', '-'
    ]
    subprocess.run(command)

    print(f'PSNR log for {logfile} finished')

# constructDF(logfile): Construct a DataFrame based on the PSNR logs
# logfile: string, path to log to construct DataFrame
# return DataFrame: DataFrame to store PSNR logs
def constructDF(logfile):
    n_values = []
    psnr_avg_values = []

    with open(logfile, 'r') as file:
        for line in file:
            records = line.split()
            n = int(records[0].split(':')[1])
            psnr_avg = float(records[5].split(':')[1])
            n_values.append(n)
            psnr_avg_values.append(psnr_avg)

    return pd.DataFrame({'n': n_values, 'psnr_avg': psnr_avg_values})

# generateLogs(logInformation): Generate PSNR logs for all generated videos to log folder
# logInformation: DataFrame, storing the location information of logs
def generateLogs(logInformation):
    if not os.path.exists('logs'):
        os.makedirs('logs')
    for index, data in logInformation.iterrows():
        logFile = data['Log Location']
        if not os.path.isfile(data['Log Location']):
            generateSingleLog(data['Reference Path'], data['Current Path'], logFile)
        else:
            print(f"{logFile} already exist, skip")
        
# getAvgPSNR(logFile): calculate the PSNR based on one log
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

# insertPSNRToDF(df): add a column of PSNR for all logs in df
# df: DataFrame of log information
def insertPSNRToDF(df):
    PSNR = []
    for log in df['Log Location']:
        PSNR.append(getAvgPSNR(log))
    df['PSNR'] = PSNR