import sys
# for windows
# sys.path.append('D:\\temp\\Experiment Python')
import psnr
import transcoder
import readconfig

dfVideo, dfCodec, dfBitrate = readconfig.generateConfigDF('input.txt')
df = transcoder.videosGenerator(dfVideo['Full Name'], dfCodec['Codec'], dfBitrate['Bitrate'])
df.to_pickle('data.pkl')
psnr.generateLogs(df)