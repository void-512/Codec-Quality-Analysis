import transcoder
import readconfig
import psnr

dfVideo, dfCodec, dfBitrate = readconfig.generateConfigDF('input.txt')
df = transcoder.videosGenerator(dfVideo['Full Name'], dfCodec['Codec'], dfBitrate['Bitrate'])
df.to_pickle('data.pkl')
psnr.generateLogs(df)