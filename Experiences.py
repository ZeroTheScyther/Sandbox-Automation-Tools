import tkinter as tk
from tkinter import scrolledtext
import Tail
import webbrowser
import time

sandboxProtocol = "sandboxgame://?lwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiOTMzY2NhMzYtZDZmZC00YTIzLWFjOWEtM2I4ZjI1YzEwMjllIiwiYWNjZXNzTGV2ZWwiOiJnYW1lIn0sImlhdCI6MTY3OTM1MTA1MSwiZXhwIjoxNjgxOTQzMDUxfQ.YlwKJ2zd4DlAhntOzG6qwQ_cZd7NdRm_4XPDT3bGLNo&lexp=a591db1c-04c1-4ac2-a3ce-5bdeacfac704&env=prod"

def startExperience(url):
    webbrowser.open(url)

def start_experience():
    startExperience("sandboxgame://?lwt=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7ImlkIjoiOTMzY2NhMzYtZDZmZC00YTIzLWFjOWEtM2I4ZjI1YzEwMjllIiwiYWNjZXNzTGV2ZWwiOiJnYW1lIn0sImlhdCI6MTY5MTQzMzI0NSwiZXhwIjoxNjk0MDI1MjQ1fQ.8Xoq0X_EVDE2CnRlju2zGd8b_TGN-zg1E24oblCDpDQ&lexp=2350e804-d4f9-4817-8568-69aa4f522a4d&env=prod")
    process_name = "The Sandbox.exe"
    while not Tail.check_process_running(process_name):
        log_area.insert(tk.END, f"The process '{process_name}' is not running. Waiting...\n")
        log_area.see(tk.END)  # Scroll to the end to keep the latest logs visible
        log_area.update()
        time.sleep(5)

    Tail.tail()

if __name__ == "__main__":
    window = tk.Tk()
    window.title("Sandbox Automation Tools")

    log_area = scrolledtext.ScrolledText(window, width=80, height=20)
    log_area.pack(padx=10, pady=10)

    start_button = tk.Button(window, text="Start Experience", command=start_experience)
    start_button.pack(pady=5)

    window.mainloop()