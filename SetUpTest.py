import subprocess
import sys
import time
import logging
import os
# import requests
# from watchdog.observers import Observer
# from watchdog.events import LoggingEventHandler


def Installpip():
	# subprocess.call("python -m pip install PyYAML", shell = True)
	subprocess.call("python -m pip install argh", shell = True)
	# subprocess.call("python -m pip install argparse", shell = True)
	# subprocess.call("python -m pip install pathtools", shell = True)
	# subprocess.call("python -m pip install virustotal-api", shell = True)
	# subprocess.call("python -m pip install watchdog", shell = True)
	subprocess.call("python -m pip install opencv-python", shell = True)
	subprocess.call("python -m pip install flask", shell = True)
	subprocess.call("python -m pip install flask-socketio", shell = True)
	subprocess.call("python -m pip install mss", shell = True)
	subprocess.call("python -m pip install urllib3", shell = True)
	subprocess.call("python -m pip install flask-pymongo", shell = True)
	subprocess.call("python -m pip install flask-bcrypt", shell = True)
	subprocess.call("python -m pip install bson", shell = True)

def FileWatcher():
	print("Cntr + C to stop watchdog")
	if __name__ == "__main__":
	    logging.basicConfig(level=logging.INFO,
	                        format='%(asctime)s - %(message)s',
	                        datefmt='%Y-%m-%d %H:%M:%S')
	    path = sys.argv[1] if len(sys.argv) > 1 else '.'
	    event_handler = LoggingEventHandler()
	    observer = Observer()
	    observer.schedule(event_handler, path, recursive=True)
	    observer.start()
	    try:
	        while True:
	            time.sleep(1)
	    except KeyboardInterrupt:
	        observer.stop()
	    observer.join()

def VirusTotalSend():
	url = 'https://www.virustotal.com/vtapi/v2/file/scan'
	params = {'apikey': '53074e57c64d3b33a36d8bd638319b23295b20be787922febe3e6c6bc8f5ca1c'}
	files = {'file': ('npp.7.6.3.Installer.exe', open('npp.7.6.3.Installer.exe', 'rb'))}
	response = requests.post(url, files=files, params=params)
	print(response.json())

def VirusTotalReport():
	url = 'https://www.virustotal.com/vtapi/v2/file/report'
	params = {'apikey': '53074e57c64d3b33a36d8bd638319b23295b20be787922febe3e6c6bc8f5ca1c', 'resource': '9d95e003f63da579778670ef6c7e08f257a17ba8c39921f178a04f531539ac80'}
	response = requests.get(url, params=params)
	print(response.json())



def back():
	print("We are now going back...")
	os.system('cls')
	choice()

def choice():
	print("What would you like to do?\n")
	print("-----------------------------------")
	print("1 --------------------- FileWatcher\n")
	print("2 --------------------- VirusTotalSend\n")
	print("3 --------------------- VirusTotalReport\n")
	print("4 --------------------- Install Depedencies\n")
	print("0 --------------------- Quit\n")
	choice = eval(input())
	if choice == 0:
		pass

	if choice == 1:
		FileWatcher()
		back()


	if choice == 2:
		VirusTotalSend()
		back()


	if choice == 3:
		VirusTotalReport()
		back()


	if choice == 4:
		Installpip()
		back()

choice()
