import serial
import tkinter as tk


ser = serial.Serial('/dev/ttyS0', 9600, timeout=2)
root = tk.Tk()
root.title("Hex File Transfer")

# Function to send hex_records Raspberry -> STM
def send_hex_record(record):
    # You send size of record to STM and tell stm the first one byte it will received size of each record (for example)	
   # size = len(record)
    ser.write( record.encode())
    print(record)
    # after STM Received each record it will send OK and raspberry will received it to send another Recode.....
    response = ser.read(2).decode() 
    #response = ser.read(ser.inWaiting).decode()
    print(response)
    # check if Rasp received another thing it will raise error
    
    if response != 'ok':
        print('Error:', response)
                
    #  Show Communication between STM , Raspberry
    display.insert(tk.END, "Sent: " + record)
    display.insert(tk.END, "Received: " + response + "\n")
    return response
# Read the hex file
try:
    with open('ITI_STM32F401CC.hex', 'r') as f:
        hex_file = f.readlines()
except FileNotFoundError:
    print("Error: Hex file not found.")
    
    exit()

display = tk.Text(root, height=20, width=80)
display.pack()

# Send each record, its size, and check for receipt
for record in hex_file:
    #if record[7:9] == "01":
     #  break
       # flag=1
        # End-of-file (EOF) record received
        # EOF record identified by the record type in the eighth and ninth position of the hex record being equal to "01". 
       # if you want to do thing
    
    try:
        check =send_hex_record(record)
        #if flag == 1:
         # break
    except Exception as e:
        display.insert(tk.END, str(e) + "\n")
        display.insert(tk.END, "Transfer failed.\n")
        break
    else:
    # If All File Transferred Successfully
        if check == "ok":
            display.insert(tk.END, "Transfer * successful.\n")
        else:
            print("waiting")
ser.close()
root.mainloop()








