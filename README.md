# LVideo
- A video format somewhat inspired by MinVideo. Can be insanely large but overall easy to understand without needing encodings.
- Supports 8-Bit Raw PCM Unencoded.
## Header:
```
Name:             0x00-0x03 (4-Bytes)   (String)
Include Audio:    0x04      (1-Byte)    (Integer)
Format:           0x05      (1-Byte)    (Integer)
Compression:      0x06      (1-Byte)    (Integer)
FPS:              0x07      (1-Byte)    (Integer)
Width:            0x08-0x0B (4-Bytes)   (Integer)
Height:           0x0C-0x0F (4-Bytes)   (Integer)
Audio Offset:     0x10-0x05 (6-Bytes)   (Integer)
Seg. OG Name:     0x16-0x1F (10-Bytes)  (String)
```
### Understanding the Header:
```
         00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
         ================================================
00000000 4C 56 49 44 01 01 00 3C E0 01 00 00 F0 00 00 00 : LVID...<à...ð...
00000010 61 5F 66 69 6C 65 6E 61 6D 65 38 20 47 DD 37 10 : a_filename8 GÝ7.
00000020 .. .. .. .. .. .. .VideoData. .. .. .. .. .. .. : ................
00000030 .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. : ................
00000040 
```
### Help Message:
```
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
```
