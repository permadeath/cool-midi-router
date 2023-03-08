# A simple program for to route MIDI messages from one device to another.

import mido
import mido.backends.rtmidi
import tkinter as tk
from tkinter import ttk
import threading

# Create GUI
root = tk.Tk()
root.title("Cool MIDI Router")
root.geometry("570x250")
root.minsize(570, 250)
root.maxsize(570, 250)
root.iconbitmap("bob.ico")

# Add background image
c = tk.Canvas(root, bg="gray16", height=200, width=200)
filename = tk.PhotoImage(file="bg.png")
background_label = tk.Label(root, image=filename)
background_label.place(x=0, y=0, relwidth=1, relheight=1)


# Flag to control MIDI routing loop
routing = False


# Function to route MIDI data from input to output
def route_midi_data():
    global routing

    # Get selected input and output ports and format them
    input_index = input_menu.get()
    input_port = input_ports[formatted_input_ports.index(input_index)]
    output_index = output_menu.get()
    output_port = output_ports[formatted_output_ports.index(output_index)]

    # Check if the input and output device is the same and if so, disallow routing
    input_name = input_port
    i = len(input_name) - 1
    while i >= 0 and not input_name[i].isspace():
        input_name = input_name[:i] + input_name[i + 1:]
        i -= 1

    output_name = output_port
    i = len(output_name) - 1
    while i >= 0 and not output_name[i].isspace():
        output_name = output_name[:i] + output_name[i + 1:]
        i -= 1

    if input_name == output_name:
        status_label.config(text="Invalid routing")
        status_label.config(bg="red")
        return
    else:
        # Open input and output ports
        with mido.open_input(input_port) as in_port, mido.open_output(output_port) as out_port:
            status_label.config(text=f"{input_index} → {output_index}")
            status_label.config(bg="green")

            # Loop to continuously read and send MIDI messages
            while routing:
                for msg in in_port.iter_pending():
                    out_port.send(msg)


# Function to start MIDI routing in a new thread
def start_routing_thread():
    global routing
    routing = True
    # Create new thread for MIDI routing
    routing_thread = threading.Thread(target=route_midi_data)

    # Start thread
    routing_thread.start()


# Function to stop MIDI routing
def stop_routing():
    global routing
    routing = False
    status_label.config(text="Not routing MIDI")
    status_label.config(bg="red")


# Function to stop MIDI routing and exit program
def stop_routing_and_exit():
    global routing
    routing = False
    root.destroy()


# Get available input and output ports
input_ports = mido.get_input_names()
output_ports = mido.get_output_names()

# Format port names for display
formatted_input_ports = []
for port in input_ports:
    name = port
    i = len(name) - 1
    while i >= 0 and not name[i].isspace():
        name = name[:i] + name[i + 1:]
        i -= 1
    name = name[:-1]
    formatted_input_ports.append(name)

formatted_output_ports = []
for port in output_ports:
    name = port
    i = len(name) - 1
    while i >= 0 and not name[i].isspace():
        name = name[:i] + name[i + 1:]
        i -= 1
    name = name[:-1]
    formatted_output_ports.append(name)

# Create input and output menus
input_menu = ttk.Combobox(root, values=formatted_input_ports, state="readonly")
output_menu = ttk.Combobox(root, values=formatted_output_ports, state="readonly")
input_menu.pack(pady=10)
output_menu.pack(pady=10)

# Create button to route MIDI data
route_button = tk.Button(root, text="Route MIDI Data", command=lambda: [stop_routing(), start_routing_thread()])
route_button.pack(pady=10)

# Create button to stop MIDI routing
stop_button = tk.Button(root, text="Stop MIDI Routing", command=stop_routing)
stop_button.pack(pady=10)

# Create label to show status
status_label = tk.Label(root, text="Not routing MIDI", font=("Comic Sans MS Bold", 11))
status_label.config(bg="red")
status_label.pack(pady=25)

root.protocol("WM_DELETE_WINDOW", stop_routing_and_exit)

root.mainloop()
