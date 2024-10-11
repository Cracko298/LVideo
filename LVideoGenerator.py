import os, cv2, sys, zlib, lz4.frame, zstandard
from PIL import Image
from audio_extract import extract_audio

def helpMessage():
    print(f"""
    python {os.path.basename(__file__)} [inputVideoFilePath] [videoFormat] [videoCompression] [includeAudio] [outputVideoFolderPath]
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
            [includeAudio]
                Value: Integer
                    0 = No (Do NOT Inlcude the Audio)
                    1 = Yes (Include the Audio)
            [outputVideoFolderPath]
                Value: String
                    - PATH to your Output Directory (not a file).
    """)
try:
    try:
        inputVideoPath = str(sys.argv[1])
        inputVideoName, extension = os.path.splitext(os.path.basename(inputVideoPath))
        videoFormat = int(sys.argv[2])
        videoCompression = int(sys.argv[3])
        includeAudio = int(sys.argv[4])
        try:
            outputPath = f"{str(sys.argv[5])}\\{inputVideoName}.lvid"
            if os.path.exists(os.path.dirname(outputPath)):
                pass
            else:
                raise IndexError
        except IndexError:
            outputPath = f".\\{inputVideoName}.lvid"
    except IndexError:
        helpMessage()
        sys.exit(1)
except ValueError:
    helpMessage()
    sys.exit(1)

def extractVideoAudio(videoPath, videoName):
    if os.path.exists(f".\\{videoName}.wav"):
        os.remove(f'.\\{videoName}.wav')
    extract_audio(input_path=f"{videoPath}", output_path=f'.\\{videoName}.wav', output_format='wav')
    return f'.\\{videoName}.wav'

def extractVideoFrames(videoPath, videoName):
    if os.path.exists(f".\\{videoName}"):
        for file in os.listdir(f".\\{videoName}"):
            os.remove(f'.\\{videoName}\\{file}')
    
    os.makedirs(f'.\\{videoName}',exist_ok=True)
    frameList = []
    cap = cv2.VideoCapture(videoPath)
    if not cap.isOpened():
        print("Error: Could not open video.")
        return

    fps = int(round(cap.get(cv2.CAP_PROP_FPS)))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    frame_count = 0
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_filename = f".\\{videoName}\\{videoName}_frame_{frame_count}.png"
        frameList.append(frame_filename)
        cv2.imwrite(frame_filename, frame)
        print(f"Saved {frame_filename}")
        frame_count += 1

    cap.release()
    return fps, width, height, frameList

def getTenCharsOfName(videoName:str):
    if len(videoName) > 10:
        return videoName[:10].encode('utf-8')
    else:
        return videoName.ljust(10, '\0').encode('utf-8')

def compileFile(fps:int, width:int, height:int, format:int, compression:int, name:str, includeAudio:int, audioOffset:int, outPath:str, data:bytearray, audio:bytearray):
    with open(outPath, 'wb') as f:
        f.write(b'LVID')
        f.write(int.to_bytes(includeAudio, 1, byteorder='little', signed=False))
        f.write(int.to_bytes(format, 1, byteorder='little', signed=False))
        f.write(int.to_bytes(compression, byteorder='little', signed=False))
        f.write(int.to_bytes(fps, 1, byteorder='little', signed=False))
        f.write(int.to_bytes(width, 4, byteorder='little', signed=False))
        f.write(int.to_bytes(height, 4, byteorder='little', signed=False))
        if int(includeAudio) == 1:
            f.write(int.to_bytes(audioOffset, 6, byteorder='little', signed=False))
        else:
            f.write(int.to_bytes(0, 6, byteorder='little', signed=False))
        f.write(getTenCharsOfName(name))
        f.write(data)
        if int(includeAudio) == 1:
            f.write(audio)
        f.close()

def extractRawFrameData(framePath, formats):
    pixel_data = bytearray()
    for file_path in framePath:
        with Image.open(file_path) as img:
            img = img.convert('RGB')
            data = list(img.getdata())
            if formats == 1:
                data = [(b, g, r) for r, g, b in data]
            
            for r, g, b in data:
                pixel_data.extend((r, g, b))
    return pixel_data

def compressData(pixelArray, compressions):
    if compressions == 1:
        return zlib.compress(pixelArray)
    elif videoCompression == 2:
        return lz4.frame.compress(pixelArray)
    elif videoCompression == 3:
        cctx = zstandard.ZstdCompressor()
        return cctx.compress(pixelArray)
    elif compressions == 0:
        return pixelArray

if __name__ == '__main__':
    outputAudioFile = extractVideoAudio(inputVideoPath, inputVideoName)
    fps, x, y, sortedFrames = extractVideoFrames(inputVideoPath, inputVideoName)
    pixels = extractRawFrameData(sortedFrames, videoFormat)
    compressedPixels = compressData(pixels, videoCompression)
    audioOff = len(compressedPixels)+0x20
    with open(outputAudioFile, 'rb') as f0:
        audioData = f0.read()
        compressedAudioData = compressData(audioData, videoCompression)
    
    compileFile(fps, x, y, videoFormat, videoCompression, inputVideoName, includeAudio, audioOff, outputPath, compressedPixels, compressedAudioData)
