"""포스터야 위해"""
#TODO
#1. Add a loading bar for the GUI to show that the program is working.
#2. Add a loading bar for the video processing to show that the program is working.
#3. Add only one encoding (finializing the video) (OPTIMIZE!!!!)
#4.Add functionality for a queue, also add a "previously played" list of urls (more exactly their hashes using a minimal hashing algorithm.)
#5. Get MOVIEPY loading > loadingbar
#6. Let user know what is happening with label above loading bar
#7. add total progress loading bar
#Changelog: (since GUIv2)
#added warn at start to assure user program is running
#remove start button once clicked in favor of loading bar
#added better font-searching
#added font-showcase
#added ability to choose voice
#removed unnecesary proprietary library: fontfinder
#made more efficent, removed first unnecesary concatenate.
#added ollama ai (requires you to install ollama @https://ollama.com/ for ai commentary
print("RedditReaderV2(GUI) - by u/aghastmuffin")
print("This program is attempting to start up. Please wait. (avg 1-4 seconds for initializing.)")
#============================imports=============================
try:
    import tkinter as tk
    import customtkinter as ctk
    from customtkinter import *
    import requests, pyttsx3, sys, subprocess, os, glob, json, os, wave, zlib, ctypes
    from pytube import YouTube
    from moviepy.editor import *
    from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
    from moviepy.video.compositing.concatenate import concatenate_videoclips
    from vosk import Model, KaldiRecognizer, SetLogLevel
    from tkinter import ttk
    from tkinter import messagebox, filedialog, messagebox
    import subprocess
    import threading
    from proglog import ProgressBarLogger
    from ctypes import wintypes
except:
    print("Error importing modules. Please install the required modules.")
    print("autoinstall? (y/n):")
    if input("> ").lower == "y":
        print("installing modules...")
        try:
            import tkinter, subprocess, json, os, requests, glob
        except:
            print("core python modules missing. these cannot be installed. Please install python (not minimal) and try again.")
            exit()
        try:
            import pyttsx3
        except:
            os.system("pip install pyttsx3")
            exit()
        try:
            import pytube
        except:
            os.system("pip install pytube")
            exit()
        try:
            import moviepy
            os.system("magick")
        except:
            os.system("pip install moviepy")
            import webbrowser
            webbrowser.open("https://imagemagick.org/script/download.php#windows")
            print("https://imagemagick.org/script/download.php#windows. please install this")
            exit()
        try:
            import vosk
        except:
            os.system("pip install vosk")
            exit()
        try:
            import customtkinter
        except:
            os.system("pip install customtkinter")
            exit()
#================================================================
#============================config==============================
SetLogLevel(-1)
hq = True #High Quality Download of YT Video: False=Any Quality, True=High Quality
sttm = -1 # as long as number is negative, acts as FALSE indicator, if above, then use specified number
endtm = 0 #0 is false, which means that only 5 seconds plus the audio time will be included. AS OF CURRENT VERSION, IF ONE OF THESE IS FLIPPED TO TRUE, BOTH VALUES WILL BE EXPECTED.
txt = False #deprecated
cleaner = True #Recommended value: True.
#codec = "h264_nvenc"
codec = None
sub_font = "8514OEM"
#codec = "libx264"
downnumb = 0 #DONT EDIT THIS PLS
speakmode = 2 #DONT EDIT THIS PLS
warn = 0 #DONT EDIT THIS PLS DEBUGGING ONLY :)
fps_v = 24
#================================================================
#============================variables===========================
headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
allf = glob.glob("*")
YT_file_path = ""
runned = 0
voice_mapper = {}
#================================================================
#============================functions===========================
def cls():
    os.system("cls")
def getfonts(li):
    li.extend(getfont())
def on_progress(chunk, file_handle, bytes_remaining):
    global progress_bar
    global a
    try:
        total_size = a.filesize
        bytes_downloaded = total_size - bytes_remaining
        pct_completed = bytes_downloaded / total_size * 100
        print(f"Status: {round(pct_completed, 2)} %")
        update_progress_bar(progress_bar, pct_completed)
    except:
        print("callback failed. WARN")
def download(url, fname):
        global a
        if hq == True:
            yt = YouTube(url)
            a = yt.streams.get_highest_resolution()
            
            yt.register_on_progress_callback(on_progress)
            messagebox.showinfo("Info", "starting download, the program may freeze. Please give up to 20 minutes based off of wifi speeds. \n (or if nothing is happening in task manager, end and restart this process)")
            a.download(filename=f'{fname}')
            messagebox.showinfo("Info", "Download Complete. (success!)")
        if hq == False:
            yt = YouTube(url)
            a = yt.streams.first()
            #yt.register_on_progress_callback(on_progress)
            a.download()
def showcase_fnt(*args):
    f_sample_txt.config(font=(font_pick.get(), 12))
def check_font_input(event):
    value = event.widget.get().lower()
    if value == '':
        data = f_lst
    else:
        data = []
        for item in f_lst:
            if item.lower().startswith(value):
                print(item)
                data.append(item)
                
    # Update the list of items in the ComboBox
    update_combobox(data)
def update_combobox(data):
    # Clear the ComboBox
    font_pick['values'] = []
    
    # Add new filtered items
    font_pick['values'] = data
    
    # If the ComboBox is empty, show all items
    if not data:
        font_pick['values'] = f_lst
def on_radiobutton_change():
    selected_option = YT_selected_var.get()
    for entry in YT_entries:
        entry.configure(state=tk.DISABLED)  # Disable all entries initially
    if selected_option in YT_entry_dict:
        YT_entry_dict[selected_option].configure(state=tk.NORMAL)  # Enable the associated entry
    if selected_option == "Presaved Video":
        YT_file_path = filedialog.askopenfilename()
        showpth.config(text=YT_file_path)
    elif len(selected_option) > 0:
        showpth.config(text="No File Selected")
def reddit_click_callback(*args):
    if reddit_get_clicked.get() == "Custom Subreddit":
        L_placeholder.configure(state="normal", height=10)
def fetch_codecs():
    """Fetches codecs using FFmpeg command."""
    result = subprocess.run(["ffmpeg", "-codecs"], capture_output=True, text=True)
    if result.returncode != 0:
        raise Exception("FFmpeg command failed. Ensure FFmpeg is installed and accessible.")
    return result.stdout
def video_codecs():
    """Extracts and prints available video codecs."""
    codecs_output = fetch_codecs()
    print("Available Video Codecs:")
    for line in codecs_output.splitlines():
        if 'V' in line[:8]:  # Video codecs are marked with 'V' in the output
            codec_info = " ".join(line.split()[1:])
            print(codec_info)

def audio_codecs():
    """Extracts and prints available audio codecs."""
    codecs_output = fetch_codecs()
    print("Available Audio Codecs:")
    for line in codecs_output.splitlines():
        if 'A' in line[:8]:  # Audio codecs are marked with 'A' in the output
            codec_info = " ".join(line.split()[1:])
            print(codec_info)
def lastmsg(*args):
    global runned
    if warn == 1:
        runned += 1
        if runned == 1:
            os.system("py lastwarning.py")
            sys.exit()
def get_voices():
    voices_li = []
    if 'engine' not in globals():
        engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    for voice in voices:
        voice_mapper[voice.name] = voice.id
    for voice in voices:
        voices_li.append(voice.name)
    return voices_li
def update_progress_bar(progress_bar, progress):
    progress_bar['value'] = progress
    root.update_idletasks()
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
def get_gpu_manufacturer():
    try:
        result = subprocess.run(["nvidia-smi"], capture_output=True, text=True)
        if result.returncode == 0:
            return "NVIDIA"
        result = subprocess.run(["lspci"], capture_output=True, text=True)
        if "AMD" in result.stdout:
            return "AMD"
        elif "Intel" in result.stdout:
            return "Intel"
    except Exception as e:
        print(f"Error detecting GPU: {e}")
    return "Unknown"
def adler32(data: bytes) -> int:
    return zlib.adler32(data)
def log_story(url):
    url_e = adler32(url.encode())
    if url_e is None:
        messagebox.showwarning("Error", "Error logging story. (124).")
        yield
    if os.path.exists("log.txt"):
        with open("log.txt", "a") as f:
            f.write(f"{url_e}\n")
    else:
        with open("log.txt", "w") as f:
            f.write(f"{url_e}\n")
def check_story(url):
    if os.path.exists("log.txt"):
        with open("log.txt", "r") as f:
            lines = f.readlines()
            for line in lines:
                if adler32(url.encode()) == int(line):
                    return True
            log_story(url)
            return False
    else:
        log_story(url)
        return False
def select_codecs():
    manufacturer = get_gpu_manufacturer()
    if manufacturer == "NVIDIA":
        video_codec = "h264_nvenc"
    elif manufacturer == "AMD":
        video_codec = "h264_vce"  # Assuming VCE for H.264. Adjust as needed.
    elif manufacturer == "Intel":
        video_codec = "h264_qsv"  # Quick Sync Video for H.264
    else:
        # Fallback or generic selection
        video_codec = "libx264"
    return video_codec
def start():
    global new_clip
    global progress_bar
    button2.pack_forget()
    threading.Thread(target=root.update_idletasks).start()
    progress_bar = ttk.Progressbar(root, orient="horizontal", length=300, mode="determinate")
    progress_bar.pack(pady=20)
    check_story(L_placeholder.get("1.0", "end-1c"))
    try:
        url = requests.get(url=(L_placeholder.get("1.0", "end-1c") + ".json"), headers=headers)
    except:
        print("Error: Invalid URL")
        messagebox.showerror("Error", "Invalid URL (119). \n this error is Fatal.")
        sys.exit()
    print((L_placeholder.get("1.0", "end-1c") + ".json"))
    if url.status_code == 200:
        print(url.json()[0]['data']['children'][0]['data']['selftext'])
        tts = pyttsx3.init()
        tts.setProperty('voice', voice_mapper[new_pyttsx_voice.get()])
        if speakmode == 1: #DO NOT WRITE TO FILE, SIMPLY SAY
            tts.say(f"{url.json()[0]['data']['children'][0]['data']['selftext']}")
            tts.runAndWait()
            print("MODE INDICATES THAT PROGRAM READ THEN EXIT - SPEAKMODE=1, DEFAULT:SPEAKMODE=2")
            sys.exit()
        if speakmode == 2:
            story = f"{url.json()[0]['data']['children'][0]['data']['selftext']}"
            tts.save_to_file(f"{url.json()[0]['data']['children'][0]['data']['selftext']}", "voiceover.mp3")
            tts.runAndWait()
    else:
        print(url.status_code)
        print("^ Unexpected Code from reddit.com")
        if url.status_code.starttswith("4") or url.status_code.starttswith("5"):
            print("[warn]: this ip has probably been banned from the site. Turn OFF vpns, and/or web proxies")
            messagebox.showwarning("Error", f"This IP has probably been banned from the site. Turn OFF VPNs, and/or web proxies. (REDDIT: {url.status_code}). We have deduced this from an error code from reddit's servers. Learn more here: https://en.wikipedia.org/wiki/List_of_HTTP_status_codes")
        sys.exit()
    yt_option = YT_selected_var.get()
    print(yt_option)
    videoclip = None
    audioclip = None
    if yt_option == "Youtube Video (from url)":
        yturl = YT_entry_dict[YT_selected_var.get()].get()
        print(yturl)
        if yturl.startswith("https://") and yturl != "":
            print("dnwnld")
            download(yturl, "video.mp4")
            videoclip = VideoFileClip("video.mp4")
        else:
            print("120 error. Please enter a valid URL.")
            messagebox.showerror("Error", "Please enter a valid Youtube URL. (120). \n this error is Fatal.")
            sys.exit()
    else:
        showpth_txt = showpth.cget('text')
        if showpth_txt != "No File Selected" and showpth_txt != "Placeholder Text" and showpth_txt != "" and "mp4" in showpth_txt:
            YT_file_path = showpth_txt
            videoclip = VideoFileClip(YT_file_path)
        else:
            print("121 error. Please select a valid file.")
            messagebox.showerror("Error", "Please select a valid file. (121). \n this error is Fatal.")
            sys.exit()
    try:
        audioclip = AudioFileClip("voiceover.mp3")
    except:
        print("Error: No Audio File Found")
        messagebox.showerror("Error", "No Audio File Found (122). \n this error is Fatal.")
        sys.exit()
    if videoclip is not None and audioclip is not None:
        vdur = videoclip.duration
        adur = audioclip.duration
    else:
        print("Error: No Video or Audio File Found")
        messagebox.showerror("Error", "No Video or Audio File Found (123 (UNINIT)). \n this error is Fatal.")
        sys.exit()
    if vdur == adur or vdur+5 == adur:
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        videoclip.write_videofile("pvideo.mp4", codec=f'{codec}', fps=fps_v) #NOTE CHECK THAT VIDEO IS SAME LENGTH AS VOICEOVER ALSO MAKE IN NEW DIR CALLED SOMETHING DIFFERENT.
    else:
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        try:
            new_clip = videoclip.set_duration(adur + 5) 
        except:
            pass
        print(vdur, adur)
        #resize video
    
    start_second()


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

def start_second():
    os.system("ffmpeg -i voiceover.mp3 -ac 1 -ar 22050 voiceover.wav")
    audio_filename = "voiceover.wav"
    custom_Word = Word
    model = Model(lang="en-us")
    wf = wave.open(audio_filename, "rb")
    rec = KaldiRecognizer(model, wf.getframerate())
    rec.SetWords(True)

    results = []
    # recognize speech using vosk model
    while True:
        import json #python for some reason doesn't recognize that this was previously imported. Glitch.
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
    with open('timestamped.txt', 'w') as f:
        for word in list_of_Words:
            theword = word.all()
            #f.write(', '.join(map(str, theword)))
            f.write(f"{theword[0]},{theword[1]},{theword[2]}")
            f.write('\n')
        f.close()
    start_third()
def generate_text_clip(text, duration):
    #return TextClip(text, fontsize=50, color='white', bg_color='black').set_duration(duration)
    selected_font = font_pick.get()
    if selected_font != None and selected_font != "":
        return TextClip(text, fontsize=50, color='grey', font=f"{selected_font}", bg_color="black").set_duration(duration)
    else:
        return TextClip(text, fontsize=50, color='grey', font="8514OEM").set_duration(duration)
def start_third():
    global new_clip
    #video = VideoFileClip("pvideo.mp4")
    video = new_clip
    # Define the text and its timings
    text_clips = []

    with open("timestamped.txt", "r") as file:
        f = file.read()
        lines = f.split("\n")
        for line in lines:
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

        # Cut the video into a small clip
        video_clip = video.subclip(last_end, combined_end)
        last_end = combined_end

        # Generate the text clip
        text_clip = generate_text_clip(combined_text, combined_end - combined_start)
        text_clip = text_clip.set_start(0).set_position('center')

        # Add the text to the video clip
        video_clip_with_text = CompositeVideoClip([video_clip, text_clip])

        clips.append(video_clip_with_text)

    # Concatenate the clips back together
    video_with_text = concatenate_videoclips(clips)

    # Write the video to a file
    if not os.path.exists("finalvideo.mp4"):
        video_with_text.write_videofile("finalvideo.mp4", codec=f'{codec}', fps=fps_v)
    else:
        from tkinter import simpledialog
        new_f_name = simpledialog.askstring("File Exists Error", "The default name of finalvideo.mp4 already exists. Please provide an alternate name, including .mp4 at the end. Press ok when done.")
        if new_f_name != None and new_f_name != "" and not os.path.exists(new_f_name):
            video_with_text.write_videofile(f"{new_f_name}", codec=f'{codec}', fps=fps_v)
        else:
            while True:
                new_f_name = simpledialog.askstring("File Exists Error", f"The default name of {new_f_name}.mp4 already exists. Please provide an alternate name, including .mp4 at the end. Press ok when done.")
                if new_f_name != None and new_f_name != "" and not os.path.exists(new_f_name):
                    video_with_text.write_videofile(f"{new_f_name}", codec=f'{codec}', fps=fps_v)
                    break
    # Function to generate text clip
#================================================================
#============================prep================================
print("using this file is against Advance Publications's Reddit's TOS, as well as Alphabet's YouTube's TOS. Using this service MAY cause a ban on your account or IP address.")
try:
    if cleaner == True:
        try:
            os.remove("voiceover.mp3")
        except:
            pass
        try:
            os.remove("video.mp4")
        except:
            pass
        try:
            os.remove("pvideo.mp4")
        except:
            pass
        try:
            os.remove("voiceover.wav")
        except:
            pass
        try:
            os.remove("timestamped.txt")
        except:
            pass
except:
    pass

#================================================================
if __name__ == "__main__":
    if codec == None:
        codec = select_codecs()
    print("spawning GUI...")
    root = ctk.CTk()
    root.title("RedditReaderV2(GUI)")
    root.wm_attributes('-transparentcolor','#4A412A') #called ugliest color in the world
    YT_selected_var = tk.StringVar(value="Youtube Video (from url)")
    YT_options = ["Youtube Video (from url)", "Presaved Video"]
    YT_entries = []
    YT_entry_dict = {}
    # Create radiobuttons and corresponding entry widgets
    f_lst = []
    getfonts(f_lst)
    p_lst = get_voices() #these 2 do the exact same thing, idk why I chose 2 tequniques. (they provide different data)

    reddit_get_clicked = tk.StringVar() 
    new_pyttsx_voice = tk.StringVar()
    reddit_get_clicked.set("Nothing Selected")
    reddit_get_clicked.trace_add("write", reddit_click_callback)
    warninglabel = ctk.CTkLabel(root, text="using this file is against Advance Publications's Reddit's TOS, as well as Alphabet's YouTube's TOS. Using this service MAY cause a ban on your account or IP address.")
    reddit_get_drop = tk.OptionMenu(root, reddit_get_clicked, *["Topposts", "Homepage Experimental", "AITA", "Custom Subreddit"])
    reddit_get_drop_info = ctk.CTkLabel(root, text="Enter a Valid Reddit URL: ")
    showpth = tk.Label(root, text="Placeholder Text", background="#242424", foreground="white")
    button2 = ctk.CTkButton(root, text="Start", command=lambda: start())
    L_placeholder = ctk.CTkTextbox(root, height=0, state=tk.DISABLED)
    font_pick_info = CTkLabel(root, text="Select a font for the subtitles: ")
    font_pick = ttk.Combobox(root, values=f_lst)
    f_sample_txt = tk.Label(root, text="Sample Text", font=("system", 12))
    font_pick.bind('<<ComboboxSelected>>', showcase_fnt)
    font_pick.bind('<KeyRelease>', check_font_input) #currently only works by scanning entire string, we just want startswith
    pyttsx3_voices_choice = tk.OptionMenu(root, new_pyttsx_voice, *p_lst)
#    cons = tk.Text(root)
#    cons.configure(state="disabled")
    warninglabel.pack(anchor="nw")
    reddit_get_drop.pack(anchor="nw", pady=20)
    reddit_get_drop_info.pack(anchor="w", pady=10)
    L_placeholder.pack(anchor="w", pady=10, padx=20)
    font_pick_info.pack(anchor="w", pady=10)
    font_pick.pack(anchor="w")
    f_sample_txt.pack(anchor="e")
    pyttsx3_voices_choice.pack(anchor="w", pady=10)
    font_pick_info.bind('<Destroy>', lastmsg)
    on_radiobutton_change()
    for option in YT_options:
        rb = ctk.CTkRadioButton(root, text=option, value=option, variable=YT_selected_var, command=on_radiobutton_change)
        rb.pack(anchor=tk.W)
        if option != "Presaved Video":
            entry = ctk.CTkEntry(root, state=tk.DISABLED)  # Disable entry by default
            entry.pack(anchor=tk.W, padx=20)  # Indent entry slightly
            YT_entries.append(entry)
            YT_entry_dict[option] = entry
    
    showpth.pack(anchor="w", pady=10)
    
    button2.pack(pady=20)

    root.geometry("400x600")
    root.mainloop()
else:
    print("please run this file normally. This is a GUI program, and cannot be imported.")
