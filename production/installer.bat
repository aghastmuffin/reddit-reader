@echo off
setlocal

:: Create the assets directory if it doesn't exist
set /p choice="Do you want to install Reddit Reader? (y/n): "

if /i "%choice%"=="y" (

    if not exist "./RedditReader" (
        mkdir "./RedditReader"
    )
    if not exist "./RedditReader/assets" (
        mkdir "./RedditReader/assets"
    )
    echo Downloading RedditReader.py
    curl -o "./RedditReader/RedditReader.py" "https://raw.githubusercontent.com/aghastmuffin/reddit-reader/main/production/RedditReader.py"
    echo Success, collecting required modules. (NOTE: on first run, more downloads might be required by these modules; it will happen automatically)
    curl -o "requirements.txt" "https://raw.githubusercontent.com/aghastmuffin/reddit-reader/main/production/requirements.txt"
    echo Modules collected successfully, downloading.
    pip install -r requirements.txt
    echo Downloading assets
    curl -o "./RedditReader/assets/Logo.png" "https://raw.githubusercontent.com/aghastmuffin/reddit-reader/main/production/assets/Logo.png"
    curl -o "./RedditReader/assets/Logov2.png" "https://raw.githubusercontent.com/aghastmuffin/reddit-reader/main/production/assets/Logov2.png"
    curl -o "./RedditReader/assets/full_logo.png" "https://raw.githubusercontent.com/aghastmuffin/reddit-reader/main/production/assets/full_logo.png"
    curl -o "./RedditReader/assets/instagram.png" "https://raw.githubusercontent.com/aghastmuffin/reddit-reader/main/production/assets/instagram.png"
    curl -o "./RedditReader/assets/tiktok_icon.png" "https://raw.githubusercontent.com/aghastmuffin/reddit-reader/main/production/assets/tiktok_icon.png"
    curl -o "./RedditReader/assets/youtube.png" "https://raw.githubusercontent.com/aghastmuffin/reddit-reader/main/production/assets/youtube.png"
    
    echo Download completed. Cleaning up
    if exist requirements.txt (
        del requirements.txt
    )
) else (
    echo Installation aborted. (No changes were made to the system.)
)

endlocal
