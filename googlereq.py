import subprocess
#This is a simple google script to get you all the pip requirements
print("This script assumes you have Python3.")
subprocess.call("pip3 install oauth2client", shell=True)
subprocess.call("pip3 install PyOpenSSl", shell=True)
subprocess.call("pip3 install gspread", shell=True)
