# LVideo
A video format somewhat inspired by MinVideo. Can be insanely large but overall easy to understand without needing encodings.
## Header:
```
Name:          0x00-0x03 (4-Bytes)
Version:       0x04      (1-Byte)
Format:        0x05      (1-Byte)
Compression:   0x06      (1-Byte)
FPS:           0x07      (1-Byte)
Width:         0x08-0x0B (4-Bytes)
Height:        0x0C-0x0F (4-Bytes)
Original File: 0x10-0x20 (16-Bytes)
```
### Understanding the Header:
```
         00 01 02 03 04 05 06 07 08 09 0A 0B 0C 0D 0E 0F
         ================================================
00000000 4C 56 49 44 01 01 00 3C E0 01 00 00 F0 00 00 00 : LVID...<à...ð...
00000010 74 68 69 73 5F 69 73 5F 66 69 6C 65 6E 61 6D 65 : this_is_filename
00000020 .. .. .. .. .. .. .VideoData. .. .. .. .. .. .. : ................
00000030 .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. .. : ................
00000040 
```
