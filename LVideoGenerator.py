import os, cv2, sys, zlib, lz4, zstandard
from PIL import Image
from tkinter import filedialog
from audio_extract import extract_audio

def helpMessage():
    print(f"""
    python {os.path.basename(__file__)} [inputVideoFilePath] [videoFormat] [videoCompression] [outputVideoFolderPath]
        Program Flags:
            [inputVideoFilePath]
                Value: String
                    - PATH to your Input File (not a directory).
            [videoFormat]
                Value: Integer
                    0 = RGB
                    1 = BGR
            [videoCompression]
                Value: Integer
                    0 = None
                    1 = zlib
                    2 = lz4
                    3 = zstandard
            [outputVideoFolderPath]
                Value: String
                    - PATH to your Output Directory (not a file).
    """)

try:
    inputVideoPath = str(sys.argv[0])
    inputVideoName, extension = os.path.splitext(os.path.basename(__file__))
    videoFormat = int(sys.argv[1])
    videoCompression = int(sys.argv[2])
    try:
        outputPath = f"{str(sys.argv[3])}\\{inputVideoName}.lvid"
        if os.path.exists(os.path.dirname(outputPath)):
            pass
        else:
            raise IndexError
    except IndexError:
        outputPath = f".\\{inputVideoName}.lvid"
except IndexError:
    helpMessage()
    sys.exit()

def extractVideoAudio(videoPath, videoName):
    extract_audio(input_path=f"{videoPath}", output_path=f'.\\{videoName}.wav', output_format='wav')

def extractVideoFrames():
    print("Fix this.")




























