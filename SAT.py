import tkinter as tk
from tkinter import scrolledtext
import Tail
import webbrowser
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Google Spreadsheet configuration
SPREADSHEET_NAME = "Copy of Season Helper - v4"
CREDENTIALS_FILE = "oauthkey.json"

sandboxProtocol = "sandboxgame://?lwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiOTMzY2NhMzYtZDZmZC00YTIzLWFjOWEtM2I4ZjI1YzEwMjllIiwiYWNjZXNzTGV2ZWwiOiJnYW1lIn0sImlhdCI6MTY3OTM1MTA1MSwiZXhwIjoxNjgxOTQzMDUxfQ.YlwKJ2zd4DlAhntOzG6qwQ_cZd7NdRm_4XPDT3bGLNo&lexp="
environmentProtocol = "&env=prod"

def startExperience(experience_id):
    url = sandboxProtocol + experience_id + environmentProtocol
    print("Opening URL:", url)  # Print the URL before opening it
    try:
        webbrowser.open(url)
    except Exception as e:
        print("Error opening URL:", e)

def read_experiences_from_spreadsheet():
    # Connect to the Google Spreadsheet
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(CREDENTIALS_FILE, scope)
    client = gspread.authorize(creds)
    sheet = client.open(SPREADSHEET_NAME).sheet1


    # Read the experiences data from the spreadsheet
    data = sheet.get_all_values()

    # Extract the experiences with names and IDs
    experiences = {}  # Dictionary to store experience names and IDs
    for row in data[1:]:  # Skip the header row
        experience_name, experience_id = row[1], row[0]
        experiences[experience_name] = experience_id
        
    return experiences

def launch_selected_experiences():
    experiences = read_experiences_from_spreadsheet()  # Get the experiences dictionary
    selected_experiences = [experience_name for experience_var, experience_name in zip(experience_vars, experiences) if experience_var.get() == 1]
    print("Selected experiences:", selected_experiences)  # Debug print
    for experience_name in selected_experiences:
        experience_id = experiences.get(experience_name)
        print("Experience Name:", experience_name)
        print("Experience ID: ", experience_id)
        if experience_id:
            startExperience(experience_id)
            Tail.tail()

# Create a Tkinter GUI to select experiences
root = tk.Tk()
root.title("Sandbox Automation Tools")

# Create a frame to hold the canvas and scrollbar
frame = tk.Frame(root)
frame.pack()

# Create a canvas to display the list of experiences
canvas = tk.Canvas(frame, width=800, height=600)
canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar for the canvas
scrollbar = tk.Scrollbar(frame, command=canvas.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Configure the canvas to use the scrollbar
canvas.config(yscrollcommand=scrollbar.set)
canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

# Create a frame inside the canvas to hold the checkboxes
inner_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=inner_frame, anchor="nw")

# Read experiences from the Google Spreadsheet
experiences = read_experiences_from_spreadsheet()

# Create Tkinter variables for each experience checkbox
experience_vars = [tk.IntVar() for _ in experiences]

# Create checkboxes for each experience
for idx, experience_name in enumerate(experiences.keys()):
    tk.Checkbutton(inner_frame, text=experience_name, variable=experience_vars[idx]).pack(anchor=tk.W)

# Create a button to launch selected experiences
launch_button = tk.Button(root, text="Launch Selected Experiences", command=launch_selected_experiences)
launch_button.pack()

# Start the Tkinter main loop
root.mainloop()