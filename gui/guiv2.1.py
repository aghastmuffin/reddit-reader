"""포스터야 위해"""
#============================imports=============================
import tkinter as tk
import customtkinter as ctk
from customtkinter import *
import requests, pyttsx3, sys, subprocess, os, glob, json, os, wave, fontfinder
from pytube import YouTube
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from vosk import Model, KaldiRecognizer, SetLogLevel
from tkinter import ttk
from tkinter import messagebox, filedialog, messagebox
import subprocess

#================================================================
#============================config==============================
SetLogLevel(-1)
hq = True #High Quality Download of YT Video: False=Any Quality, True=High Quality
sttm = -1 # as long as number is negative, acts as FALSE indicator, if above, then use specified number
endtm = 0 #0 is false, which means that only 5 seconds plus the audio time will be included. AS OF CURRENT VERSION, IF ONE OF THESE IS FLIPPED TO TRUE, BOTH VALUES WILL BE EXPECTED.
txt = False #deprecated
cleaner = True #Recommended value: True.
accelerator = "h264_nvenc"
sub_font = "8514OEM"
a_accelerator = "libx264"
downnumb = 0 #DONT EDIT THIS PLS
speakmode = 2 #DONT EDIT THIS PLS
warn = 0 #DONT EDIT THIS PLS DEBUGGING ONLY :)
#================================================================
#============================variables===========================
headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
allf = glob.glob("*")
YT_file_path = ""
#================================================================
#============================functions===========================
def cls():
    os.system("cls")
def getfonts(li):
    li.extend(fontfinder.getfont())
def on_progress(stream, chunk, file_handle, bytes_remaining):
    global downnumb
    total_size = stream.filesize
    bytes_downloaded = total_size - bytes_remaining
    percentage = (bytes_downloaded / total_size) * 100
    cls()
    if downnumb == 1:
        print("Downloading.")
        downnumb = downnumb + 1
    if downnumb == 2:
        print("Downloading..")
        downnumb = downnumb + 1
    if downnumb == 3:
        print("Downloading...")
        downnumb = downnumb + 1
    print(f"{percentage:.2f}%")
def download(url, fname):
        if hq == True:
            yt = YouTube(url)
            a = yt.streams.get_highest_resolution()
            #yt.register_on_progress_callback(on_progress)
            print("starting download, the program may freeze. Please give up to 20 minutes based off of wifi speeds. \n (or if nothing is happening in task manager, end and restart this process)")
            a.download(filename=f'{fname}')
            print("success")
        if hq == False:
            yt = YouTube(url)
            a = yt.streams.first()
            #yt.register_on_progress_callback(on_progress)
            a.download()
def check_input(event):
    value = event.widget.get()
    if value == '':
        font_pick['values'] = f_lst
    else:
        data = [item for item in f_lst if value.lower() in item.lower()]
        font_pick['values'] = data
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
def lastmsg(*args):
    messagebox.showwarning("Remember this!", "Please remember to drag the stuff you want to keep from this session into another folder, as on running this script, the files that have been generated will be cleared to save storage. (simply create a folder called saved or whatever, and store your files you wish to keep from this session there. (this only applies to the files that this program DIRECTLY generated.)")
    root.destroy()
    sys.exit()
def start():
    url = requests.get(url=(L_placeholder.get("1.0", "end-1c") + ".json"), headers=headers)
    print((L_placeholder.get("1.0", "end-1c") + ".json"))
    if url.status_code == 200:
        print(url.json()[0]['data']['children'][0]['data']['selftext'])
        tts = pyttsx3.init()
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
            messagebox.showwarning("Error", f"This IP has probably been banned from the site. Turn OFF VPNs, and/or web proxies. (REDDIT: {url.status_code}).")

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
        videoclip.write_videofile("pvideo.mp4") #NOTE CHECK THAT VIDEO IS SAME LENGTH AS VOICEOVER ALSO MAKE IN NEW DIR CALLED SOMETHING DIFFERENT.
    else:
        new_audioclip = CompositeAudioClip([audioclip])
        videoclip.audio = new_audioclip
        try:
            new_clip = videoclip.set_duration(adur + 5) 
        except:
            pass
        print(vdur, adur)
        #resize video
        try:
            resized_clip = new_clip.resize(height=int(videoclip.size[0] * 16 / 9))
        except:
            print("[warn] error, special rsize clip failed.")
            resized_clip = videoclip.resize(height=int(videoclip.size[0] * 16 / 9))
        try:
            new_clip.write_videofile("pvideo.mp4", codec=f"{accelerator}")
        except:
            print("clipping failed")
            try:
                resized_clip.write_videofile("pvideo.mp4", codec=f"{accelerator}")
            except:
                print("Failed rendering video with nvidia codec, install CUDA, or add AMD to config.")
                print("use CPU: True")
                resized_clip.write_videofile("pvideo.mp4")
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
        return TextClip(text, fontsize=50, color='grey', font="8514OEM", bg_color="black").set_duration(duration)
def start_third():
    video = VideoFileClip("pvideo.mp4")

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
        video_with_text.write_videofile("finalvideo.mp4", codec=f'{a_accelerator}', fps=24)
    else:
        from tkinter import simpledialog
        new_f_name = simpledialog.askstring("File Exists Error", "The default name of finalvideo.mp4 already exists. Please provide an alternate name, including .mp4 at the end. Press ok when done.")
        if new_f_name != None and new_f_name != "" and not os.path.exists(new_f_name):
            video_with_text.write_videofile(f"{new_f_name}", codec=f'{a_accelerator}', fps=24)
        else:
            while True:
                new_f_name = simpledialog.askstring("File Exists Error", f"The default name of {new_f_name}.mp4 already exists. Please provide an alternate name, including .mp4 at the end. Press ok when done.")
                if new_f_name != None and new_f_name != "" and not os.path.exists(new_f_name):
                    video_with_text.write_videofile(f"{new_f_name}", codec=f'{a_accelerator}', fps=24)
                    break
    # Function to generate text clip
#================================================================
#============================prep================================
print("using this file is against Advance Publications's Reddit's TOS, as well as Alphabet's YouTube's TOS. Using this service MAY cause a ban on your account or IP address.")
try:
    if cleaner == True:
        os.remove("voiceover.mp3")
        os.remove("video.mp4")
        os.remove("pvideo.mp4")
        os.remove("voiceover.wav")
        os.remove("timestamped.txt")
except:
    pass

#================================================================
if __name__ == "__main__":
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

    reddit_get_clicked = tk.StringVar() 
    reddit_get_clicked.set("Nothing Selected")
    reddit_get_clicked.trace_add("write", reddit_click_callback)
    warninglabel = tk.Label(root, text="using this file is against Advance Publications's Reddit's TOS, as well as Alphabet's YouTube's TOS. Using this service MAY cause a ban on your account or IP address.")
    reddit_get_drop = tk.OptionMenu(root, reddit_get_clicked, *["Topposts", "Homepage Experimental", "AITA", "Custom Subreddit"])
    reddit_get_drop_info = ctk.CTkLabel(root, text="Enter a Valid Reddit URL: ")
    showpth = tk.Label(root, text="Placeholder Text", background="#242424", foreground="white")
    button2 = ctk.CTkButton(root, text="Start", command=lambda: start())
    L_placeholder = ctk.CTkTextbox(root, height=0, state=tk.DISABLED)
    font_pick_info = CTkLabel(root, text="Select a font for the subtitles: ")
    font_pick = ttk.Combobox(root, values=f_lst)

    cons = tk.Text(root)
    cons.configure(state="disabled")
    warninglabel.pack(anchor="nw")
    reddit_get_drop.pack(anchor="nw", pady=20)
    reddit_get_drop_info.pack(anchor="w", pady=10)
    L_placeholder.pack(anchor="w", pady=10, padx=20)
    font_pick_info.pack(anchor="w", pady=10)
    font_pick.pack(anchor="w")
    font_pick_info.bind('<Destroy>', lastmsg)
    L_placeholder.bind('<KeyRelease>', check_input)
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
    cons.pack()
    root.geometry("400x400")
    root.mainloop()
else:
    print("please run this file normally. This is a GUI program, and cannot be imported.")
