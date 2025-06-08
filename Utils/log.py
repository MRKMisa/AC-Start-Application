import traceback
from datetime import datetime
import time

def log_errors(exc_type, exc_value, exc_traceback):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d | %H:%M:%S")

    with open("Logs/errors.log", "a") as f:
        f.write(f"---ERROR--- | {time.time()} | {timestamp}\n")
        traceback.print_exception(exc_type, exc_value, exc_traceback, file=f)

        f.write(f"\n")
    
    write_script_end()
    exit()

def write_script_start():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d | %H:%M:%S")

    with open("Logs/output.log", "w") as f:
        f.write(f"{time.time()} | {timestamp} |--------Script start--------\n")

def write_script_end():
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d | %H:%M:%S")

    with open("Logs/output.log", "r") as f:
        line = f.readline()
        
    script_time = time.time()-float(line.split(" |")[0])

    with open("Logs/output.log", "a") as f:
        f.write(f"{time.time()} | {timestamp} |--------Script end--------| script run: {script_time}s\n")

def write_script_output(output):
    now = datetime.now()
    timestamp = now.strftime("%Y-%m-%d | %H:%M:%S")

    with open("Logs/output.log", "r") as f:
        line = f.readline()
        
    script_time = time.time()-float(line.split(" |")[0])

    with open("Logs/output.log", "a") as f:
        f.write(f"{time.time()} | {timestamp} |{output}| time from script start: {script_time}s\n")


if __name__ == "__main__":
    write_script_start()
    time.sleep(0.2)
    write_script_output("ahoj")
    time.sleep(0.2)
    write_script_end()