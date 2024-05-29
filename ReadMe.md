![redditreader-high-resolution-logo-transparent](https://github.com/aghastmuffin/reddit-reader/assets/78246775/683588d8-9ca2-4c71-9c26-13a005a0a6d7)
[![Buy Me a Coffee](https://studio.buymeacoffee.com/assets/img/qr-logo.svg)](https://www.buymeacoffee.com/aghastmuffin)
# RedditReader Installation
simply download your choice of the contents of either the seperated folder (recommended) or the onefile folder (depricated) or run `gh repo clone aghastmuffin/reddit-reader` and locate the folder you wish to use. Please also ensure that you have [FFMPEG](https://www.gyan.dev/ffmpeg/builds/) use gyan.dev and install the normal ffmpeg, not minimal. Whilst it is not tested with [BtbN](https://github.com/BtbN/FFmpeg-Builds) it should work. The program also requires the use of [ImageMagick](https://imagemagick.org/script/download.php) download or check if it is installed through `magick` (note: sometimes ffmpeg and magick won't work in cmd, and only in powershell. If it still isn't working, ensure both ffmpeg and imagemagick are on PATH, and restart all terminals). This program is only tested on windows and it is recommended to have an external graphics card (but not needed). 16+ GB memory (the more the merrier) and enough storage to hold this and a couple of files (shouldn't be more than 1 gb at the very most). A multicore CPU, and that's about it! Most processing is done on-system so you might want some more beefy components or to outsource to [google colab](https://colab.research.google.com/) or [repl.it](https://repl.it")

Order of execution
---
I don't recommend using the pre "compiled" onefile as it makes debugging or a random error in one of the scripts a pain in the butt, i have also stopped maintaining it. It will work, just not with the new fixes and features supplied to the multifile version.
for the onefile it's pretty self explanitory. Run the onefile.
for the multi one i'll explain. So basically there are 2 ways to execute these files. One of them is through the preprovided runner script (runner.py) (note: please ensure that the files are all in the same UNPACKED directory, if they are, then everything should work fine. If they aren't then some errors might occur.)
But whatever the case, run it in this order:
 - redditv3.py
 - vosktst.py
 - subtitler.py
---
We also now have a [website](https://aghastmuffin.github.io/reddit-reader/) where you can download reddit-reader (latest). It's pretty basic right now, but I'm planning to get some more done soon.
