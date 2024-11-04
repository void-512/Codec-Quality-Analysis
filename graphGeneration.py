import os
import matplotlib

# generateGraph(df): generate graphs with given Data Frame
# df: DataFrame with necessary information
# save: boolean, determine if the figure will be saved
# path: string, path of figure if save is True
def generateGraph(df, save, path):
    # Avoid generation of font cache when unnecessary
    import matplotlib.pyplot as plt
    referenceList = df['Reference Name'].unique()
    nameList = df['Custom Name'].unique()
    for video in referenceList:
        plt.figure(figsize=(10, 6))
        plt.title(f'PSNR vs Bitrate for {video}')
        plt.xlabel('Bitrate')
        plt.ylabel('PSNR (dB)')
        filterByVideo = df[df['Reference Name'] == video]
        for name in nameList:
            filterByCodec = filterByVideo[filterByVideo['Custom Name'] == name]
            plt.plot(filterByCodec['Bitrate'], filterByCodec['PSNR'], label=f'Codec: {name}', marker='o')
        plt.legend()
        plt.grid(True)
    if save:
        plt.savefig(path)
    else:
        plt.show()