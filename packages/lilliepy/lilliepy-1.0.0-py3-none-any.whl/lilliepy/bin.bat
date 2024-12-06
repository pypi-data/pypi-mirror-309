@echo off

set blank=07
set error=04
set success=02
set load=01
set dir=

color %load%
echo Initializing Lilliepy App...
git init

set /p name=Provide App's Name: 
set /p type=Flask M.C.V server or single file Flask server (1 or 2): 

if "%type%"=="1" (
    git clone https://github.com/websitedeb/Lilliepy-2.0
    set dir=Lilliepy-2.0
    echo selected Flask M.V.C server...
) else if "%type%"=="2" (
    git clone https://github.com/websitedeb/Lilliepy-1.0
    set dir=Lilliepy-1.0
    echo selected single file Flask server...
) else (
    color %error%
    echo Invalid selection...
    pause
    exit
)

if not "%dir%"=="" (
    ren "%dir%" "%name%"
    if %errorlevel% equ 0 (
        echo Downloading dependencies...
        cd "%name%"
        pip install -r requirements.txt
        if %errorlevel% equ 0 (
            color %success%
            echo Created Lilliepy App!
            pause
        ) else (
            color %error%
            echo An error occurred while downloading the dependencies...
            pause
        )
    ) else (
        color %error%
        echo An error occurred while renaming the app...
        pause
    )
) else (
    color %error%
    echo An error occurred while creating the app...
    pause
)

cls
color %blank%
exit
