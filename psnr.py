import os
import subprocess
import pandas as pd
import matplotlib.pyplot as plt

logFolderName = 'logs'

def generateSingleLog(reference, target, logfile):

    command = [
        'ffmpeg', '-i', reference, '-i', target,
        '-lavfi', f'psnr=stats_file={logfile}', 
        '-f', 'null', '-'
    ]

    subprocess.run(command, check=True)

    print(f'PSNR log for {target} finished')

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

def generateLogs():
    if not os.path.exists(logFolderName):
        os.makedirs(logFolderName)
    folders = []
    workDirectoryItems = os.listdir()
    for item in workDirectoryItems:
        if os.path.isdir(item) and item != logFolderName:
            folders.append(item)
    for subfolder in folders:
        transcodedItems = os.listdir()
        for video in transcodedItems:
            generateSingleLog()