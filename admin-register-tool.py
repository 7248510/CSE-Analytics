import json
import requests
import datetime
import os
import subprocess
from flask import Flask, render_template, url_for, request, session, redirect, Markup, flash, send_file
from flask_pymongo import PyMongo
from pymongo import MongoClient
from flask_bcrypt import Bcrypt
#Import the pip dependencies
app = Flask(__name__)
crypt = Bcrypt(app)
#Change database name depending
app.config['MONGO_DBNAME'] = 'CSE'
#Creates the connection to the local host
app.config['MONGO_URI'] = 'mongodb://localhost:27017/CSE'
mongo = PyMongo(app)

print("Welcome to the admin panel.")
#options = "If you need to register please press 1, you need an account for the web application to work.\nIf you already have an account please press 2."
#print(options)
#selection = eval(input())
#Registration begins
#if (selection == 1):
print("Lets register.")
print("Please enter your email address")
email = input()
print("Please input your first name")
firstname = input()
print("Please enter your last name")
lastname = input()
print("Please enter your password")
password = input()
mongo.db.users.insert_one({'email' : email,'password' : crypt.generate_password_hash(password), 'firstname' : firstname, 'lastname' : lastname, 'admin' : 'true'})
print("Your information is now in the database")
  #Begin registration

# if (selection == 2):
#     print("You have now been logged in")
#     print("To list all of your users first name and email address please press 1.")
#     #print("To get VirusTotal information please press 2.")
#     choice = eval(input())
#     if choice == 1:
#         listfname = mongo.db.users_information.distinct('firstname')
#         listemail = mongo.db.users_information.distinct('Email-address')
#         print(listfname)
#         print(listemail)
#         print("If you would like to get specific user information please press 1.\nif not press 2.")
#         specific = eval(input())
#         if specific == 1:
#             searchchoice = eval(input())
#             if searchchoice == 1:
#                 print("Please input the first name")
#                 firstname = input()
#                 searchfirstname = mongo.db.users_information.find_one({'firstname' : firstname})
#
#             if searchchoice == 2:
#                 print("Please enter the email for the user")
#                 email = input()
#                 searchemail = mongo.db.users_information.find_one({'Email-address' : email})
#                 print(searchemail)
#         if specific == 2:
#             print("Closing program now.")
#ctrl + slash(Will comment out all of the lines highlighted.)
