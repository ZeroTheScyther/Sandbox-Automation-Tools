import os
import getpass
import time
import psutil
import subprocess
import pyautogui

class Catch5(Exception):

    pass

def get_log_filename():
    username = getpass.getuser()
    return f"C:/Users/{username}/AppData/LocalLow/TSBGAMING/The Sandbox/Player.log"

def delete_existing_log(filename):
    if os.path.exists(filename):
        try:
            os.remove(filename)
            print("Existing Player.log file deleted.")
        except OSError as e:
            print(f"Error deleting file: {e}")

def check_process_running(process_name):
    for process in psutil.process_iter(['pid', 'name']):
        if process.info['name'] == process_name:
            print("Process found!")
            return True
    return False

def exitProcess():
    print("Exitting tial.")

def log_usage(elapsed_time_playmode_client, elapsed_time_loading_client):
    try:

        # Get The Sandbox.exe process
        sandbox_process = None
        for proc in psutil.process_iter(['pid', 'name']):
            if proc.info['name'] == "The Sandbox.exe":
                sandbox_process = proc
                break

        # Get CPU usage
        if sandbox_process:
            cpu_percentages = []
            num_cores = psutil.cpu_count(logical=False)  # Use logical=False to get physical cores only
            for _ in range(5):  # Make 5 calls to get a more accurate average
                cpu_usage = sandbox_process.cpu_percent(interval=0.1)
                cpu_percentages.append(cpu_usage)
            avg_cpu_usage = sum(cpu_percentages) / len(cpu_percentages)
            avg_cpu_usage_per_core = avg_cpu_usage / num_cores
            print(f"CPU Usage of The Sandbox.exe: {avg_cpu_usage_per_core:.2f}%")

        if sandbox_process:
            sandbox_process_memory_info = sandbox_process.memory_info()
            ram_usage_bytes = sandbox_process_memory_info.rss
            ram_usage_megabytes = ram_usage_bytes / (1024 * 1024)  # Convert bytes to MBs
            print(f"RAM Usage (The Sandbox.exe): {ram_usage_megabytes:.2f} MB")

        # Determine GPU vendor and import the appropriate library
        gpu_vendor = get_gpu_vendor()
        if gpu_vendor == "NVIDIA":
            import pynvml
            pynvml.nvmlInit()
            gpu_handle = pynvml.nvmlDeviceGetHandleByIndex(0)  # Assuming only one NVIDIA GPU
            gpu_info = pynvml.nvmlDeviceGetUtilizationRates(gpu_handle)
            gpu_usage = gpu_info.gpu
            print(f"NVIDIA GPU Usage: {gpu_usage:.2f}%")
            pynvml.nvmlShutdown()
        elif gpu_vendor == "AMD":
            import pyadl
            pyadl.ADLErrorHandling.ADLErrorHandling(pyadl.ADLErrorHandling.OptionalMode.Discard)
            device_list = pyadl.ADLClock.ADLClock_GetAllDevices()
            if device_list:
                gpu_info = pyadl.ADLClock.ADLClock_GetClockInfo(device_list[0])
                gpu_usage = gpu_info.coreClock / gpu_info.maxCoreClock * 100
                print(f"AMD GPU Usage: {gpu_usage:.2f}%")
        else:
            print("GPU usage monitoring not available for the detected GPU.")

        # Convert elapsed time to minutes and seconds
        elapsed_minutes_playmode = int(elapsed_time_playmode_client // 60)
        elapsed_seconds_playmode = int(elapsed_time_playmode_client % 60)

        elapsed_minutes_loading = int(elapsed_time_loading_client // 60)
        elapsed_seconds_loading = int(elapsed_time_loading_client % 60)

        print(f"Elapsed Time (Start to Loading): {elapsed_minutes_loading:02d}:{elapsed_seconds_loading:02d}")
        print(f"Elapsed Time (Loading to Playmode): {elapsed_minutes_playmode:02d}:{elapsed_seconds_playmode:02d}")

    except psutil.NoSuchProcess:
        print("The Sandbox.exe process not found.")
    except Exception as e:
        print(f"Error: {e}")

def get_gpu_vendor():
    try:
        import pynvml
        pynvml.nvmlInit()
        device_count = pynvml.nvmlDeviceGetCount()
        pynvml.nvmlShutdown()
        if device_count > 0:
            return "NVIDIA"
    except ImportError:
        pass

    try:
        import pyadl
        return "AMD"
    except ImportError:
        pass

    return "Unknown"

def killProcess():
      subprocess.run(["taskkill", "/f", "/im", "The Sandbox.exe"])

def tail():
    process_name = "The Sandbox.exe"
    filename = get_log_filename()
    delete_existing_log(filename)
    application_start_time = time.time()

    found_playmode_client = False
    found_loading_client = False
    start_time_playmode_client = 0
    start_time_loading_client = 0
    elapsed_time_playmode_client = 0
    elapsed_time_loading_client = 0

    while not os.path.exists(filename):
        print("Waiting for Player.log to be created...")
        time.sleep(1)

    # Start the timer
    start_time = time.time()

    try:
        with open(filename, "r") as file:
            file.seek(0, os.SEEK_END)  # Go to the end of the file
            while True:

#                if not found_loading_client and time.time() - start_time > 40:
#                   raise Catch5("Application misbehaving.")

                line = file.readline().strip()
                if line:

                    if "TRANSITIONED FROM FSMState_PreparePlaymodeClient to FSMState_PlaymodeWelcomeScreen" in line:
                        print("FSMState_PlaymodeWelcomeScreen.", flush=True)
                        pyautogui.press('space')


                    if not found_playmode_client and "TRANSITIONED FROM FSMState_PlaymodeWelcomeScreen to FSMState_PlaymodeClient" in line:
                        found_playmode_client = True
                        start_time_playmode_client = time.time()
                        print("FSMState_PlaymodeClient found.", flush=True)

                    if not found_loading_client and "TRANSITIONED FROM FSMState_EstablishConnection2Server to FSMState_LoadingClient" in line:
                        found_loading_client = True
                        start_time_loading_client = time.time()
                        elapsed_time_loading_client = start_time_loading_client - start_time
                        print("FSMState_LoadingClient found.", flush=True)

                    if found_loading_client:
                        elapsed_time_playmode_client = time.time() - start_time_loading_client

                    if found_playmode_client:
                        log_usage(elapsed_time_playmode_client, elapsed_time_loading_client)
                        break


    except FileNotFoundError:
        print(f"File not found: {filename}")
    except Exception as e:
        print(f"Error: {e}")
    killProcess()