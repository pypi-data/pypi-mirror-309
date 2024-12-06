#!/bin/bash

blank="\033[0m"
error="\033[31m"
success="\033[32m"
load="\033[33m"
dir=""

echo -e "${load}Initializing Lilliepy App...${blank}"
git init

read -p "Provide App's Name: " name
read -p "Flask M.C.V server or single file Flask server (1 or 2): " type

if [ "$type" == "1" ]; then
    git clone https://github.com/websitedeb/Lilliepy-2.0
    dir="Lilliepy-2.0"
    echo "selected Flask M.V.C server..."
elif [ "$type" == "2" ]; then
    git clone https://github.com/websitedeb/Lilliepy-1.0
    dir="Lilliepy-1.0"
    echo "selected single file Flask server..."
else
    echo -e "${error}Invalid selection...${blank}"
    exit 1
fi

if [ -d "$dir" ]; then
    mv "$dir" "$name"
    if [ $? -eq 0 ]; then
        echo "Downloading dependencies..."
        cd "$name" || exit 1
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo -e "${success}Created Lilliepy App!${blank}"
        else
            echo -e "${error}An error occurred while downloading the dependencies...${blank}"
        fi
    else
        echo -e "${error}An error occurred while renaming the app...${blank}"
    fi
else
    echo -e "${error}An error occurred while creating the app...${blank}"
fi
