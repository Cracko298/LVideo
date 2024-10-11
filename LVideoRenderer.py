import pyaudio, wave, threading, mmap, time, zlib, os, pygame, lz4.frame, zstandard, io
from tkinter import filedialog

def load_video_data(video_file):
    with open(video_file, 'rb') as f:
        mmapped_file = mmap.mmap(f.fileno(), 0, access=mmap.ACCESS_READ)
        mmapped_file.seek(0x04)
        includeAudio = int.from_bytes(mmapped_file.read(0x01), byteorder='little', signed=False)
        mmapped_file.seek(0x05)
        videoFormat = int.from_bytes(mmapped_file.read(0x01), byteorder='little', signed=False)
        mmapped_file.seek(0x06)
        videoCompression = int.from_bytes(mmapped_file.read(0x01), byteorder='little', signed=False)
        mmapped_file.seek(0x07)
        fps = int.from_bytes(mmapped_file.read(0x01), byteorder='little', signed=False)
        mmapped_file.seek(0x08)
        width = int.from_bytes(mmapped_file.read(0x04), byteorder='little', signed=False)
        mmapped_file.seek(0x0C)
        height = int.from_bytes(mmapped_file.read(0x04), byteorder='little', signed=False)
        mmapped_file.seek(0x10)
        audioOffset = int.from_bytes(mmapped_file.read(0x06), byteorder='little', signed=False)
        mmapped_file.seek(0x16)
        name = str(mmapped_file.read(0x0A).decode('utf-8')).replace('\0','')
        mmapped_file.seek(0x20)
        compressedVideoData = mmapped_file.read(audioOffset - 0x20)
        if includeAudio == 1:
            mmapped_file.seek(audioOffset)
            compressedAudio = mmapped_file.read()
        else:
            compressedAudio = b''

    if videoCompression == 1:
        audioData = zlib.decompress(compressedAudio)
        videoData = zlib.decompress(compressedVideoData)
    elif videoCompression == 2:
        audioData = lz4.frame.decompress(compressedAudio)
        videoData = lz4.frame.decompress(compressedVideoData)
    elif videoCompression == 3:
        cctx = zstandard.ZstdDecompressor()
        audioData = cctx.decompress(compressedAudio)
        videoData = cctx.decompress(compressedVideoData)
    else:
        audioData = compressedAudio
        videoData = compressedVideoData

    return includeAudio, videoFormat, fps, width, height, audioData, videoData, name

def get_wav_properties(audio_data):
    with wave.open(io.BytesIO(audio_data), 'rb') as wav_file:
        channels = wav_file.getnchannels()
        sample_width = wav_file.getsampwidth()
        sample_rate = wav_file.getframerate()
        frame_count = wav_file.getnframes()
        audio_frames = wav_file.readframes(frame_count)
    return channels, sample_rate, sample_width

def play_audio(pcm_data):
    channels, sample_rate, sample_width = get_wav_properties(pcm_data)
    def _play():
        p = pyaudio.PyAudio()
        stream = p.open(format=p.get_format_from_width(sample_width),
                        channels=channels,
                        rate=sample_rate,
                        output=True)

        stream.write(pcm_data)
        stream.stop_stream()
        stream.close()
        p.terminate()

    threading.Thread(target=_play, daemon=True).start()

def render_video(video_file):
    includeAudio, videoFormat, fps, width, height, audioData, videoData, name = load_video_data(video_file)

    pygame.init()
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    frame_size = width * height * 3
    num_frames = len(videoData) // frame_size
    if videoFormat == 1:
        vForm = "BGR"
    else:
        vForm = "RGB"
    frames = [pygame.image.frombuffer(videoData[i * frame_size:(i + 1) * frame_size], (width, height), vForm) for i in range(num_frames)]

    running = True
    current_frame = 0
    audio_thread = None

    def stop_audio():
        if audio_thread is not None and audio_thread.is_alive():
            audio_thread.join()

    play_audio(audioData)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.blit(frames[current_frame], (0, 0))
        pygame.display.flip()
        current_frame = (current_frame + 1) % num_frames
        if current_frame == 0 and includeAudio and audioData:
            stop_audio() 
            audio_thread = threading.Thread(target=play_audio, args=(audioData,), daemon=True)
            audio_thread.start()

        clock.tick(fps)

    stop_audio()
    pygame.quit()

video_file = filedialog.askopenfilename(
    defaultextension=".lvid",
    filetypes=[("LVideo files", "*.lvid;*.liv;*.vidl")],
    initialdir=os.getcwd(),
    title="Load LVideo File"
)

if video_file:
    render_video(video_file)
