import os
import sys
import psnr
import argparse
import transcoder
import readconfig
import pandas as pd
import graphGeneration

dfVideo, dfCodec, dfBitrate = None, None, None

def parserHandler():
    parser = argparse.ArgumentParser(usage="codec-compare.py [-h] [-c CONFIG_FILE] {log, graph, clean} <options>")
    parser.add_argument("-c", type=str, help="Specify the config file")

    subparsers = parser.add_subparsers(dest="command", metavar="")

    logParser = subparsers.add_parser("log", help="Generate log")
    logParser.add_argument("-noskip", action="store_true", help="Not skipping files already existed, regenerate them")
    logParser.add_argument("-export", type=str, help="Export .pkl files, can be merged with other .pkl files")

    graphParser = subparsers.add_parser("graph", help="Show PSNR plot")
    graphParser.add_argument("-save", type=str, help="Save picture to [PATH]")

    cleanParser = subparsers.add_parser("clean", help="Remove working folder")

    mergeParser = subparsers.add_parser("merge", help="Merge multiple .pkl files generated by the program and export to ./data.pkl")
    mergeParser.add_argument("-i", nargs="+", help="Specify path to .pkl files")

    args = parser.parse_args()
    return args

def generateLog(noskip, path):
    if noskip:
        clean('retain reference')
        generateLog(False, path)
    else:
        videoData = transcoder.videosGenerator(dfVideo['Full Name'], dfCodec['Codec'], dfBitrate['Bitrate'])
        psnr.generateLogs(videoData)
        psnr.insertPSNRToDF(videoData)
        videoData.to_pickle(path)

def clean(scope):
    nameList = dfVideo['Name']
    codecList = dfCodec['Codec']
    if scope == 'all':
        readconfig.deleteFolder(os.getcwd())
    elif scope == 'retain reference':
        readconfig.deleteFolder(os.path.join(os.getcwd(), 'logs'))
        for name in nameList:
            for codec in codecList:
                folder = name + '_' + codec
                readconfig.deleteFolder(os.path.join(os.getcwd(), folder)) 

def showGraph(save, path):
    graphingDF = pd.read_pickle('data.pkl')
    graphGeneration.generateGraph(graphingDF, save, path)

def mergeDF(pklPaths):
    result = None
    for pklFile in pklPaths:
        if os.path.exists(pklFile):
            df = pd.read_pickle(pklFile)
            result = pd.concat([result, df], axis=0)
        else:
            sys.exit(f'{pklFile} doesn\'t exist')
    print(result)
    result.to_pickle('data.pkl')

def main():
    args = parserHandler()
    global dfVideo, dfCodec, dfBitrate
    if args.command == 'clean':
        if args.c:
            dfVideo, dfCodec, dfBitrate = readconfig.generateConfigDF(args.c)
            clean('retain reference')
            sys.exit('Generated files deleted')
        else:
            sys.exit('Please specify the config file with -c')

    if args.command == 'log':
        if args.c:
            dfVideo, dfCodec, dfBitrate = readconfig.generateConfigDF(args.c)
            generateLog(args.noskip, args.export or 'data.pkl')
        else:
            sys.exit('Please specify the config file with -c')

    if args.command == 'graph':
        if args.save:
            showGraph(True, args.save)
        else:
            showGraph(False, None)

    if args.command == 'merge':
        mergeDF(args.i)

if __name__ == "__main__":
    main()
