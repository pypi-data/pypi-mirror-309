@echo off

set blank=07
set error=04
set success=02
set load=01

color %load%
echo Initializing Lilliepy App...
git init
set /p name=Provide App's Name:

git clone https://github.com/websitedeb/Lilliepy-2.0
if %errorlevel% equ 0 (
    ren "Lilliepy-2.0" "%name%"
    if %errorlevel% equ 0 (
        echo Downloading dependencies...
        cd %name%
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