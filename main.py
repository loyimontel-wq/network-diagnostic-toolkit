import tkinter as tk
from tkinter import ttk
from tkinter import scrolledtext
import subprocess 
import socket
import threading

def run_ping_thread():

    thread = threading.Thread(
        target=ping_host
    )

    thread.start()



def save_log(message):

    try:

        with open(
            "results.txt",
            "a",
            encoding="utf-8"
        ) as file:

            file.write(message + "\n")

    except Exception as e:

        output_box.insert(
            tk.END,
            f"Log Error: {e}\n"
        )

def check_port():

    host = host_entry.get()

    port = port_entry.get()

    if not host or not port:

        output_box.insert(
            tk.END,
            "Please enter both host and port.\n"
        )

        return

    try:

        port = int(port)

        sock = socket.socket(
            socket.AF_INET,
            socket.SOCK_STREAM
        )

        sock.settimeout(3)

        result = sock.connect_ex(
            (host, port)
        )

        output_box.insert(
            tk.END,
            "\n=== PORT CHECK ===\n"
        )

        if result == 0:

            message = f"Port {port} is OPEN"

            output_box.insert(
                tk.END,
                message + "\n"
            )

            save_log(message)

        else:

            message = f"Port {port} is CLOSED"

            output_box.insert(
                tk.END,
                message + "\n"
            )

            save_log(message)

        sock.close()

    except Exception as e:

        output_box.insert(
            tk.END,
            f"Port Check Error: {e}\n"
        )

def dns_lookup():

    host = host_entry.get()

    if not host:
        output_box.insert(
            tk.END,
            "Please enter a host.\n"
        )
        return

    try:

        ip_address = socket.gethostbyname(host)

        output_box.insert(
            tk.END,
            f"\n=== DNS LOOKUP ===\n"
        )

        message = (
            f"{host} -> {ip_address}"
        )

        output_box.insert(
            tk.END,
            message + "\n"
        )

        save_log(message)
    except Exception as e:

        output_box.insert(
            tk.END,
            f"DNS Error: {e}\n"
        )

def ping_host():

    host = host_entry.get()

    if not host:
        output_box.insert(tk.END, "Please enter a host.\n")
        return

    try:

        result = subprocess.run(
            ["ping", host],
            capture_output=True,
            text=True
        )

        output_box.insert(tk.END, "\n=== PING RESULTS ===\n")
        output_box.insert(tk.END, result.stdout)
        save_log(result.stdout)

    except Exception as e:

        output_box.insert(
            tk.END,
            f"Error: {e}\n"
        )

def clear_output():

    output_box.delete(
        "1.0",
        tk.END
    )

root = tk.Tk()

root.title("Network Diagnostic Toolkit v1.0")
root.geometry("1000x700")


title_label = ttk.Label(
    root,
    text="Network Diagnostic Toolkit",
    font=("Arial", 18, "bold")
)

title_label.pack(pady=15)

input_frame = ttk.LabelFrame(
    root,
    text=" Input "
)

input_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

host_label = ttk.Label(
    input_frame,
    text="Host:"
)

host_label.grid(
    row=0,
    column=0,
    padx=5
)

host_entry = ttk.Entry(
    input_frame,
    width=40
)

host_entry.grid(
    row=0,
    column=1,
    padx=5
)

port_label = ttk.Label(
    input_frame,
    text="Port:"
)

port_label.grid(
    row=0,
    column=2,
    padx=5
)

port_entry = ttk.Entry(
    input_frame,
    width=10
)

port_entry.grid(
    row=0,
    column=3,
    padx=5
)



button_frame = ttk.LabelFrame(
    root,
    text=" Actions "
)

button_frame.pack(
    fill="x",
    padx=10,
    pady=10
)

ping_button = ttk.Button(
    button_frame,
    text="Ping Host",
    command=run_ping_thread
)

ping_button.grid(
    row=0,
    column=0,
    padx=5
)

dns_button = ttk.Button(
    button_frame,
    text="DNS Lookup",
    command=dns_lookup
)

dns_button.grid(
    row=0,
    column=1,
    padx=5
)

port_button = ttk.Button(
    button_frame,
    text="Check Port",
    command=check_port
)

port_button.grid(
    row=0,
    column=2,
    padx=5
)

clear_button = ttk.Button(
    button_frame,
    text="Clear Output",
    command=clear_output
)

clear_button.grid(
    row=0,
    column=3,
    padx=5
)

# ======================
# Output Box
# ======================

output_frame = ttk.LabelFrame(
    root,
    text=" Output "
)

output_frame.pack(
    fill="both",
    expand=True,
    padx=10,
    pady=10
)

output_box = scrolledtext.ScrolledText(
    output_frame,
    width=100,
    height=25,
    font=("Consolas", 10)
)

output_box.pack(
    fill="both",
    expand=True,
    padx=5,
    pady=5
)

status_label = ttk.Label(
    root,
    text="Ready",
    anchor="w"
)

status_label.pack(
    fill="x",
    side="bottom"
)

root.mainloop()
