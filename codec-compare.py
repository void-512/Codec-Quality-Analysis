import sys
import os
import pandas as pd
# for windows
# sys.path.append('D:\\temp\\Experiment Python')
import psnr
import transcoder
import readconfig
import argparse
import graphGeneration

dfVideo, dfCodec, dfBitrate = None, None, None

def parserHandler():
    parser = argparse.ArgumentParser(usage="codec-compare.py [-h] [-c CONFIG_FILE] {log, graph, clean} [-s PIC_PATH]")
    parser.add_argument("-c", type=str, help="Specify the config file")

    subparsers = parser.add_subparsers(dest="command", metavar="")

    logParser = subparsers.add_parser("log", help="Generate log")
    logParser.add_argument("-noskip", action="store_true", help="Not skipping files already existed, regenerate them")

    graphParser = subparsers.add_parser("graph", help="Show PSNR plot")
    graphParser.add_argument("-save", type=str, help="Save picture to [PATH]")

    exportParser = subparsers.add_parser("export", help="Export video data, need")

    cleanParser = subparsers.add_parser("clean", help="Remove working folder")

    mergeParser = subparsers.add_parser("merge", help="Merge multiple .pkl files generated by the program and export to [workdir]/data.pkl")
    mergeParser.add_argument("-i", nargs="+", help="Specify path to .pkl files")

    args = parser.parse_args()
    return args

def generateLog(noskip):
    if noskip:
        clean('retain reference')
        generateLog(false)
    else:
        videoData = transcoder.videosGenerator(dfVideo['Full Name'], dfCodec['Codec'], dfBitrate['Bitrate'])
        videoData.to_pickle('data.pkl')
        psnr.generateLogs(videoData)

def clean(scope):
    nameList = dfVideo['Name']
    codecList = dfVideo['Codec']
    if scope == 'all':
        readconfig.deleteFolder(os.getcwd())
    elif scope == 'retain reference':
        readconfig.deleteFolder(os.path.join(os.getcwd(), 'logs'))
        for name in nameList:
            for codec in codecList:
                folder = name + '_' + codec
                readconfig.deleteFolder(os.path.join(os.getcwd(), folder)) 

def showGraph(save, path):
    graphingDF = graphGeneration.loadPickle('data.pkl')
    graphGeneration.insertPSNRToDF(graphingDF)
    graphGeneration.generateGraph(graphingDF, save, path)

def mergeDF(pklPaths):
    result = None
    for pklFile in pklPaths:
        if os.path.exists(pklFile):
            df = graphGeneration.loadPickle(pklFile)
            result = pd.concat([result, df], axis=0)
        else:
            sys.exit(f'{pklFile} doesn\'t exist')
    result.to_pickle('data.pkl')

def main():
    args = parserHandler()
    global dfVideo, dfCodec, dfBitrate
    if args.command == 'clean':
        clean('all')
        sys.exit(f'{os.getcwd()} deleted')
    elif args.c:
        config = args.c
        dfVideo, dfCodec, dfBitrate = readconfig.generateConfigDF(config)
    else:
        sys.exit('Please specify the config file with -c')

    if args.command == 'log':
        if args.noskip:
            generateLog(True)
        else:
            generateLog(False)

    if args.command == 'graph':
        if args.save:
            showGraph(True, args.save)
        else:
            showGraph(False, None)
            
    if args.command == 'merge':
        mergeDF(args.i)

if __name__ == "__main__":
    main()