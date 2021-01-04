#/usr/bin/sh
#A script to grab dependancies for locally hosting CSE
#Tested on CentOS7
install()
{
  sudo yum install git -y 
  sudo yum install python3 -y #For cent. Ubuntu = sudo apt-get install python3    Python3 might be installed by default on Ubuntu 
  sudo python3 -m pip install argh
  sudo python3 -m pip install opencv-python
  sudo python3 -m pip install flask
  sudo python3 -m pip install mss
  sudo python3 -m pip install urllib3
  sudo python3 -m pip install flask-pymongo
  sudo python3 -m pip install flask-bcrypt
  sudo python3 -m pip install bson
  sudo python3 -m pip install -U Werkzeug==0.16.0 #Fixes a dependency error https://stackoverflow.com/questions/61628503/flask-uploads-importerror-cannot-import-name-secure-filename
  sudo python3 -m pip install flask_socketio
  sudo python3 -m pip install requests
  sudo firewall-cmd --zone=public --permanent --add-service=http #ufw is not installed on centos minimal. This firewall setting may be different on Ubuntu
}
showIP()
{
  echo your IP is below
  ip a
}
update()
{
	sudo yum update
}
gitme()
{
	cd ../
	git clone https://github.com/7248510/CSE-Analytics.git
}
install
#gitme #Only use gitme if you clone the scripts directory. This is uncommented by default because I'm putting the script in the CSE directory.
showIP
#update