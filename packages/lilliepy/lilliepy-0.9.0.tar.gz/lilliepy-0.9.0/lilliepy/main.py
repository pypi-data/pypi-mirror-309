import subprocess as sbp
import os, sys

module_dir = os.path.dirname(os.path.abspath(__file__))

def create_bat():
    try:
        bat_file_path = os.path.join(module_dir, "bin.bat")
        sbp.run([bat_file_path], shell=True, check=True)
    except sbp.CalledProcessError as e:
        print(f"Error running .bat file: {e}")
        sys.exit(1)

def create_sh():
    try:
        sh_file_path = os.path.join(module_dir, "bin.sh")
        sbp.run(["bash", sh_file_path], check=True)
    except sbp.CalledProcessError as e:
        print(f"Error running .sh file: {e}")
        sys.exit(1)

def create(_os = "windows"):
    if _os == "windows" or _os == "batch" or _os == "cmd" or _os == "bat":
        create_bat()
    elif _os == "linus" or _os == "mac" or _os == "shell" or _os == "sh":
        create_sh()
    else:
        create_sh()

def version():
    return 'LilliePy Version : 0.9.0'