import generatetarget
import readandstore
import psnr

dfVideo, dfCodec, dfBitrate = readandstore.generateConfigDF('input.txt')
df = generatetarget.videosGenerator(dfVideo['Full Name'], dfCodec['Codec'], dfBitrate['Bitrate'])
df.to_pickle('data.pkl')
psnr.generateLogs(df)