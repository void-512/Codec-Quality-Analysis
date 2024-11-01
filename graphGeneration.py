import os
import sys
import matplotlib
import platform
if platform.system() == 'Darwin':
    matplotlib.use('MacOSX')
else:
    matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

# generateGraph(df): generate graphs with given Data Frame
# df: DataFrame with necessary information
def generateGraph(df, save, path):
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
    if save:
        plt.savefig(path)
    else:
        plt.show()