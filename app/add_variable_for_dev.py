import subprocess
import platform

if __name__ == "__main__":
    if platform.system() == "Windows":
        subprocess.call("set PYTHONPATH=%cd%", shell=True) #not working...
    else:
        #TODO: implement
        subprocess.call("ENV pwd", shell=True)

