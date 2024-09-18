import sys, requests, pyttsx3, sys, subprocess, yt_dlp, wave, os
from PyQt6.QtWidgets import *
from PyQt6.QtGui import QIcon, QPixmap
from PyQt6.QtCore import Qt
from tkinter import messagebox
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from vosk import SetLogLevel, KaldiRecognizer, Model
import ctypes
from ctypes import wintypes

headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}


a_accelerator = "libx264"
#callback functions defined here
def getfont():
    # Define necessary types
    LF_FACESIZE = 32
    LF_FULLFACESIZE = 64

    class LOGFONT(ctypes.Structure):
        _fields_ = [
            ("lfHeight", wintypes.LONG),
            ("lfWidth", wintypes.LONG),
            ("lfEscapement", wintypes.LONG),
            ("lfOrientation", wintypes.LONG),
            ("lfWeight", wintypes.LONG),
            ("lfItalic", wintypes.BYTE),
            ("lfUnderline", wintypes.BYTE),
            ("lfStrikeOut", wintypes.BYTE),
            ("lfCharSet", wintypes.BYTE),
            ("lfOutPrecision", wintypes.BYTE),
            ("lfClipPrecision", wintypes.BYTE),
            ("lfQuality", wintypes.BYTE),
            ("lfPitchAndFamily", wintypes.BYTE),
            ("lfFaceName", wintypes.WCHAR * LF_FACESIZE)
        ]

    # Define callback function
    def EnumFontFamiliesExProc(lpelfe, lpntme, FontType, lParam):
        fonts.append(lpelfe.contents.lfFaceName)
        return 1

    # Define function prototype
    EnumFontFamiliesExProcProto = ctypes.WINFUNCTYPE(
        wintypes.INT, ctypes.POINTER(LOGFONT), ctypes.POINTER(wintypes.LONG), wintypes.DWORD, wintypes.LPARAM
    )
    EnumFontFamiliesExProc = EnumFontFamiliesExProcProto(EnumFontFamiliesExProc)

    # Load gdi32.dll
    gdi32 = ctypes.WinDLL("gdi32")

    # Load user32.dll
    user32 = ctypes.WinDLL("user32")

    # Get device context
    hdc = user32.GetDC(None)

    # Prepare LOGFONT
    lf = LOGFONT()
    lf.lfCharSet = 1  # DEFAULT_CHARSET

    # Prepare list to store font names
    fonts = []

    # Enumerate fonts
    gdi32.EnumFontFamiliesExW(hdc, ctypes.byref(lf), EnumFontFamiliesExProc, 0, 0)

    # Release device context
    user32.ReleaseDC(None, hdc)

    return fonts


def generate_text_clip(text, duration):
    #return TextClip(text, fontsize=50, color='white', bg_color='black').set_duration(duration)
    selected_font = font_choice.currentText()
    if selected_font != None and selected_font != "":
        return TextClip(text, fontsize=50, color='grey', font=f"{selected_font}", bg_color="black").set_duration(duration)
    else:
        return TextClip(text, fontsize=50, color='grey', font="8514OEM", bg_color="black").set_duration(duration)
    

class Word:
    ''' A class representing a word from the JSON format for vosk speech recognition API '''

    def __init__(self, dict):
        '''
        Parameters:
          dict (dict) dictionary from JSON, containing:
            conf (float): degree of confidence, from 0 to 1
            end (float): end time of the pronouncing the word, in seconds
            start (float): start time of the pronouncing the word, in seconds
            word (str): recognized word
        '''

        self.conf = dict["conf"]
        self.end = dict["end"]
        self.start = dict["start"]
        self.word = dict["word"]

    def to_string(self):
        ''' Returns a string describing this instance '''
        return "{:20} from {:.2f} sec to {:.2f} sec, confidence is {:.2f}%".format(
            self.word, self.start, self.end, self.conf*100)
    def times(self):
        ''' Returns a tuple with start and end times '''
        return (self.start, self.end)
    def word(self):
        ''' Returns the recognized word '''
        return self.word
    def all(self):
        return self.word, self.start, self.end, self.conf*100

def filechoose():
    global file_vid
    global reset_file
    file_vid, _ = QFileDialog.getOpenFileName(window, "Select Video File", "", "Video Files (*.mp4)")
    if file_vid:
        filechose.setText("File Chosen")
        filechose.setEnabled(False)
        reset_file = QPushButton("Slect a different file")
        reset_file.clicked.connect(reset_filechoose)
        layout.insertRow(layout.rowCount() - 1, reset_file)  # Insert reset_button before the last row (start button)


def reset_filechoose():
    global file_vid
    global reset_file
    filechose.setText("Select File")
    filechose.setEnabled(True)
    layout.removeRow(reset_file)
    file_vid = None


def valid_chk():
    global file_vid
    if reddit_url.text() == "" or not (reddit_url.text().startswith("https://reddit.com") or reddit_url.text().startswith("https://www.reddit.com")):
        messagebox.showerror("Reddit Reader ERROR", "Naming Schema: Please enter a valid Reddit URL, starting with https://reddit.com")
        return
    if len(yt_url.text()) < 1 and 'file_vid' not in globals():
        messagebox.showerror("Reddit Reader ERROR", "Naming Schema: Please enter either a Youtube URL or select a file, not both.")
        return
    if yt_url.text() != "" and (yt_url.text().startswith("https://youtube.com") or yt_url.text().startswith("https://www.youtube.com")):
        file_vid = yt_url.text()
        print("set ytdwnload to true because", "yt_url.text() is: '" + yt_url.text() + "'")
        yt_download = True
    elif yt_url.text() == "":
        yt_download = False
    else:
        messagebox.showerror("Reddit Reader ERROR", "Naming Schema: Please enter a valid Youtube URL, starting with https://youtube.com, or provide a valid file.")
        return
    url = requests.get(f"{reddit_url.text()}.json", headers=headers) #replace with reddit_url.text()
    if url.status_code == 200: #success
        tts = pyttsx3.init()
        story = str(url.json()[0]['data']['children'][0]['data']['selftext'])
        tts.save_to_file(f"{url.json()[0]['data']['children'][0]['data']['selftext']}", "voiceover.mp3") #potentially see if I can store this content in a variable, not a file.
        tts.runAndWait()
    else:
        print(url.status_code)
        print("^ Unexpected Code from reddit.com")
        if url.status_code.starttswith("4") or url.status_code.starttswith("5"): #client or server error
            print("You may have been banned from reddit.com. Please try again later. Or you entered a malformed URL.")
        sys.exit()
    #handle the downloading of the youtube video
    print(yt_download)
    if yt_download:
        yt_url1 = yt_url.text()
        ydl_opts = {
            'outtmpl': 'output.mp4'
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download(yt_url1)
            videoclip = VideoFileClip("output.mp4")
    else:
        videoclip = VideoFileClip(file_vid)
    #concatenate the video clips
    audioclip = AudioFileClip("voiceover.mp3")
    if videoclip is not None and audioclip is not None:
        vdur = videoclip.duration
        adur = audioclip.duration
    """if vdur == adur or vdur+5 == adur: #why 
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        #videoclip.write_videofile("pvideo.mp4")"""
    if vdur >= adur:
        #audioclip = CompositeAudioClip([audioclip, audioclip.subclip(adur - 1)])
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        #videoclip.write_videofile("pvideo.mp4")
    os.system("ffmpeg -y -i voiceover.mp3 -ac 1 -ar 22050 voiceover.wav")
    audio_filename = "voiceover.wav"
    custom_Word = Word
    model = Model(lang="en-us")
    wf = wave.open(audio_filename, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    # recognize speech using vosk model
    while True:
        import json  # python for some reason doesn't recognize that this was previously imported. Glitch.
        data = wf.readframes(4000)
        if len(data) == 0:
            break
        if rec.AcceptWaveform(data):
            part_result = json.loads(rec.Result())
            results.append(part_result)
    part_result = json.loads(rec.FinalResult())
    results.append(part_result)
    list_of_Words = []
    for sentence in results:
        if len(sentence) == 1:
            # sometimes there are bugs in recognition 
            # and it returns an empty dictionary
            # {'text': ''}
            continue
        for obj in sentence['result']:
            w = custom_Word(obj)  # create custom Word object
            list_of_Words.append(w)  # and add it to list
    maindict = {}
    wf.close()  # close audiofile
    from collections import OrderedDict
    import json
    list_of_Words = []
    for sentence in results:
        if len(sentence) == 1:
            continue
        for obj in sentence['result']:
            w = custom_Word(obj)  # create custom Word object
            list_of_Words.append(w)  # and add it to list

    wf.close()  # close audiofile
    timestamped = []
    """
    with open('timestamped.txt', 'w') as f:
        for word in list_of_Words:
            theword = word.all()
            # f.write(', '.join(map(str, theword)))
            f.write(f"{theword[0]},{theword[1]},{theword[2]}")
            f.write('\n')
        f.close()
    """
    for word in list_of_Words:
        theword = word.all()
        timestamped.append(f"{theword[0]}, {theword[1]}, {theword[2]}")
    #start 3

    # Define the text and its timings
    text_clips = []

    for line in timestamped:
        try:
            lsplit = line.split(",")
            word = str(lsplit[0])
            stime = float(lsplit[1])
            etime = float(lsplit[2])
            text_clips.append({"text": word, "start": stime, "end": etime})
        except IndexError:
            pass
        except:
            print("unexpected error")
            pass
    clips = []
    last_end = 0

    # Group the words into chunks of 4
    for i in range(0, len(text_clips) - 3, 4):
        clip1 = text_clips[i]
        clip2 = text_clips[i + 1]
        clip3 = text_clips[i + 2]
        clip4 = text_clips[i + 3]

        # Combine the words and timings
        combined_text = " ".join([clip1["text"], clip2["text"], clip3["text"], clip4["text"]])
        combined_start = clip1["start"]
        combined_end = clip4["end"]

        # Cut the videoclip into a small clip
        video_clip = videoclip.subclip(last_end, combined_end)
        last_end = combined_end

        # Generate the text clip
        text_clip = generate_text_clip(combined_text, combined_end - combined_start)
        text_clip = text_clip.set_start(0).set_position('center')

        # Add the text to the videoclip clip
        video_clip_with_text = CompositeVideoClip([video_clip, text_clip])

        clips.append(video_clip_with_text)

    # Concatenate the clips back together
    videoclip_with_text = concatenate_videoclips(clips)

    # Write the videoclip to a file
    if not os.path.exists("finalvideoclip.mp4"):
        videoclip_with_text.write_videofile("finalvideoclip.mp4", codec=f'{a_accelerator}', fps=24)
    else:
        from tkinter import simpledialog
        new_f_name = simpledialog.askstring("File Exists Error", "The default name of finalvideoclip.mp4 already exists. Please provide an alternate name, including .mp4 at the end. Press ok when done.")
        if new_f_name != None and new_f_name != "" and not os.path.exists(new_f_name):
            videoclip_with_text.write_videofile(f"{new_f_name}", codec=f'{a_accelerator}', fps=24)
        else:
            while True:
                new_f_name = simpledialog.askstring("File Exists Error", f"The default name of {new_f_name}.mp4 already exists. Please provide an alternate name, including .mp4 at the end. Press ok when done.")
                if new_f_name != None and new_f_name != "" and not os.path.exists(new_f_name):
                    videoclip_with_text.write_videofile(f"{new_f_name}", codec=f'{a_accelerator}', fps=24)
                    break
    

if __name__ == "__main__":
    logo_pathf = os.path.join(os.path.dirname(__file__), "assets", "full_logo.png")
    logo_path = os.path.join(os.path.dirname(__file__), "assets", "Logov2.png")
    app = QApplication(sys.argv)
    window = QWidget()
    window.setWindowTitle('Reddit Reader (UNPAID)')
    window.setGeometry(100, 100, 280, 320)
    font_types = getfont()

    pixmap_unc = QPixmap(logo_pathf)
    logo = QLabel()
    pixmap_unc = pixmap_unc.scaled(window.width(), 100, aspectRatioMode=Qt.AspectRatioMode.KeepAspectRatio)  # 1 is Qt.AspectRatioMode.KeepAspectRatio
    logo.setPixmap(pixmap_unc)

    layout = QFormLayout()
    # Add widgets to the layout
    reddit_url = QLineEdit()
    font_choice = QComboBox()
    font_choice.addItems(font_types)
    yt_url = QLineEdit()
    filechose = QPushButton("Select File")

    start = QPushButton("Start Video Generation")
    #layout.setVerticalSpacing(20)
    layout.addRow(logo)
    layout.addRow("Reddit URL:", reddit_url)
    layout.addRow("Font:", font_choice)
    layout.addRow("Youtube URL:", yt_url)
    layout.addRow("Select your own .mp4", filechose)
    layout.addRow(start)
    window.setLayout(layout)
    #add signals/callbacks to onchange functions
    filechose.clicked.connect(filechoose)
    
    start.clicked.connect(valid_chk)
    
    
    window.setWindowIcon(QIcon(logo_path))
    window.show()
    sys.exit(app.exec())
