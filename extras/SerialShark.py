import serial
import os
import subprocess
import signal
import time

serial_port = "/dev/ttyUSB0"
board_rate = 921600
filename = "capture.pcap"
connection_established = False

# TODO: Replace print with log to a file

while not connection_established:
    try:
        ser = serial.Serial(serial_port, board_rate)
        connection_established = True
    except:
        print("[!] Serial connection failed... Retrying...")
        time.sleep(2)
        continue

print("[+] Serial connected. Name: " + ser.name)
f = open(filename,'wb')

has_started = False
while not has_started:
    line = ser.readline()
    if b"<<START>>" in line:
        has_started = True
        print("[+] Stream started...")
    else:
        print(f"Error: {line}")

print("[+] Starting up wireshark...")
cmd = "tail -f -c +0 " + filename + " | wireshark -k -i -"
p = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                       shell=True, preexec_fn=os.setsid)

try:
    while True:
        ch = ser.read()
        f.write(ch)
        f.flush()
except KeyboardInterrupt:
    print("[+] Stopping...")
    os.killpg(os.getpgid(p.pid), signal.SIGTERM)

f.close()
ser.close()
print("[+] Done.")
