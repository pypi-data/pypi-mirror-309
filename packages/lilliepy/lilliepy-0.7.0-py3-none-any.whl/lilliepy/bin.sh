#!/bin/bash

blank=07
error=04
success=02
load=01


set_color() {
  case $1 in
    $load) echo -e "\033[34m" ;;  
    $success) echo -e "\033[32m" ;;  
    $error) echo -e "\033[31m" ;;  
    $blank) echo -e "\033[0m" ;;  
  esac
}

set_color $load
echo "Initializing Lilliepy App..."


git init


read -p "Provide App's Name: " name


git clone https://github.com/websitedeb/Lilliepy-2.0
if [ $? -eq 0 ]; then
    
    mv "Lilliepy-2.0" "$name"
    if [ $? -eq 0 ]; then
        echo "Downloading dependencies..."
        cd "$name" || exit
        pip install -r requirements.txt

        if [ $? -eq 0 ]; then
            set_color $success
            echo "Created Lilliepy App!"
        else
            set_color $error
            echo "An error occurred while downloading the dependencies..."
        fi
    else
        set_color $error
        echo "An error occurred while renaming the app..."
    fi
else
    set_color $error
    echo "An error occurred while creating the app..."
fi


set_color $blank
exit 0