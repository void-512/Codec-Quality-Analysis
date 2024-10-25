import generatetarget
import readandstore
import psnr

dfVideo, dfCodec, dfBitrate = readandstore.generateConfigDF('exampleinput.txt')
df = generatetarget.videosGenerator(dfVideo['Full Name'], dfCodec['Codec'], dfBitrate['Bitrate'])
psnr.generateLogs(df)