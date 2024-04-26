#helpful article for optimization: https://stackoverflow.com/questions/63837260/ffmpeg-with-moviepy
import requests, pyttsx3, sys, subprocess, os, wave, json
from pytube import YouTube
from moviepy.editor import *
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from vosk import Model, KaldiRecognizer, SetLogLevel

warn = 0 #DONT EDIT THIS PLS DEBUGGING ONLY :)
hq = True #High Quality Download of YT Video: False=Any Quality, True=High Quality
sttm = -1 # as long as number is negative, acts as FALSE indicator, if above, then use specified number
endtm = 0 #0 is false, which means that only 5 seconds plus the audio time will be included. AS OF CURRENT VERSION, IF ONE OF THESE IS FLIPPED TO TRUE, BOTH VALUES WILL BE EXPECTED.
txt = False
accelerator = "h264_nvenc"
def cls():
    os.system("cls")
downnumb = 0
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
headers = {'User-Agent': r'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
if warn == 1:
    print("[warn]: using this file is against Advance Publications's Reddit's TOS, as well as Alphabet's YouTube's TOS. Using this service MAY cause a ban on your account or IP address.")
    print("[warn]: Before using this file, ensure that pytube is up to date!")
print("RedditReader V3")
print("1. Topposts")
print("2. AITA")
print("3. Custom")
print("(LEAVE BLANK FOR OPTION 2)")
try:
    a = int(input("Which number do you want? "))
except:
    a = 3
if a == 1 or a == 2 or a == 3:
    pass
else:
    a = 3
print(a)

if a == 1:
    query = "https://reddit.com/.json"
    print("not supported")
if a == 2:
    query = "https://www.reddit.com/r/AmItheAsshole/.json"
if a == 3:
    print("Enter URL of custom reddit post. We'll do the rest.")
    query = input("URL: ")
    query = query + ".json"
speakmode = 2

#f = open(".txt", "r")
#query = "https://www.reddit.com/r/AmItheAsshole/comments/17g2iv7/aita_for_outshining_the_bride.json"

url = requests.get(url=query, headers=headers)
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
    if url.status_code == 403:
        print("[warn]: this ip has probably been banned from the site. Turn OFF vpns, and web proxies")
    sys.exit()

#rmaudo = subprocess.check_output(["ffmpeg", "-i", "video.mp4", "-an", "pvideo.mp4"])#ffmpeg -i input_video.mp4 -an output_video.mp4 - REMOVAL OF AUDIO FROM VIDEO FILE
print("GRAB REDDIT SUCCESSFUL!")
print("1/5...")
print("continue")
input("PRESS ENTER: ")
cls()
print("Download Youtube/Find Video to overlay \n (THIS PROCESS WILL ONLY DOWNLOAD THE VIDEO, AS OF VERSION 2, YOU MUST CUT THE VIDEO TO SPECIFIED PERAMETERS YOURSELF.) \n THIS WILL CHANGE LATER.")
print("Enter Custom URL:")
yturl = input("")
if yturl.startswith("https://") and yturl != "":
    download(yturl, "video.mp4")
else:
    print("Hmm. We couldn't seem to find anything that matches that url. We will use a preprovided video in that same directory (video.mp4), you may move one there now")
    input("press enter when video move is completed: ")
#else:
#    download("https://", yturl)
#    print("[warn]: please Include https:// in front of the youtube url!")

#newreaudo = subprocess.check_output(["ffmpeg", "-i", "video.mp4", "-i", "voiceover.mp3", "-map", "0:v", "-map", "1:a", "c:v", "copy", "-shortest", "pvideo.mp4"])#ffmpeg -i video.mp4 -i audio.wav -map 0:v -map 1:a -c:v copy -shortest output.mp4
videoclip = VideoFileClip("video.mp4")
audioclip = AudioFileClip("voiceover.mp3")
vdur = videoclip.duration
adur = audioclip.duration
if vdur == adur or vdur+5 == adur:
    new_audioclip = CompositeAudioClip([audioclip])
    videoclip.audio = new_audioclip
    videoclip.write_videofile("pvideo.mp4") #NOTE CHECK THAT VIDEO IS SAME LENGTH AS VOICEOVER ALSO MAKE IN NEW DIR CALLED SOMETHING DIFFERENT.
else:
    """
        if sttm < -1 and endtm < 0:
            ffmpeg_extract_subclip("pvideo.mp4", 0, adur+5, targetname="pvideo.mp4")
        elif sttm > -1:
            ffmpeg_extract_subclip("pvideo.mp4", sttm, sttm+endtm+5, targetname="pvideo.mp4") #THESE ARE NOT RECOMMENDED, AS IT MAY MESS UP PROGRAM, NO CHECKS IN PLACE YET.
        elif endtm > 0:
            ffmpeg_extract_subclip("pvideo.mp4", 0, endtm, targetname="pvideo.mp4")
        else:
            print("unexpected error occured.")
    """
    #ffmpeg_extract_subclip("pvideo.mp4", 0, adur+5, targetname="pvideo.mp4") WE DONT CUT THE VIDEO- FIX THIS
    #CUTTING VIDEO DONE, NOW WE WRITE AUDIO!!
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
SetLogLevel(-1)
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
os.system("ffmpeg -i voiceover.mp3 -ac 1 -ar 22050 voiceover.wav")
audio_filename = "voiceover.wav"
custom_Word = Word
model = Model(lang="en-us")
wf = wave.open(audio_filename, "rb")
rec = KaldiRecognizer(model, wf.getframerate())
rec.SetWords(True)

# get the list of JSON dictionaries
results = []
# recognize speech using vosk model
while True:
    data = wf.readframes(4000)
    if len(data) == 0:
        break
    if rec.AcceptWaveform(data):
        part_result = json.loads(rec.Result())
        results.append(part_result)
part_result = json.loads(rec.FinalResult())
results.append(part_result)

# convert list of JSON dictionaries to list of 'Word' objects
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


# convert list of JSON dictionaries to list of 'Word' objects
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
        if word != "":
            f.write('\n')
    f.close()

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

# Function to generate text clip
def generate_text_clip(text, duration):
    return TextClip(text, fontsize=50, color='white', bg_color='black').set_duration(duration)

# Add text clips to the video
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
    text_clip = text_clip.set_start(0).set_position(('center', 'bottom'))

    # Add the text to the video clip
    video_clip_with_text = CompositeVideoClip([video_clip, text_clip])

    clips.append(video_clip_with_text)

# Concatenate the clips back together
video_with_text = concatenate_videoclips(clips)

# Write the video to a file
video_with_text.write_videofile("finalvideo.mp4", codec='libx264', fps=24)
