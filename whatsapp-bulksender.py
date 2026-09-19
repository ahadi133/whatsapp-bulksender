import tkinter as tk
from tkinter import messagebox, filedialog
import pywhatkit
import os
import threading

def choose_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    entry_file_path.delete(0, tk.END)
    entry_file_path.insert(0, file_path)

def log_status(message, tag):
    status_box.config(state=tk.NORMAL)
    status_box.insert(tk.END, message + "\n", tag)
    status_box.config(state=tk.DISABLED)
    status_box.see(tk.END)

def send_message_thread():
    send_button.config(state=tk.DISABLED)
    log_status("⏳ Sending messages... Please wait.\n", "info")

    mode = contact_mode.get()
    message = entry_message.get("1.0", tk.END).strip()
    status_box.delete("1.0", tk.END)

    if not message:
        messagebox.showerror("Error", "Message cannot be empty.")
        send_button.config(state=tk.NORMAL)
        return

    numbers = []

    if mode == "single":
        number = entry_number.get().strip()
        if not number.startswith("+"):
            messagebox.showerror("Error", "Please enter the number in international format (e.g., +8801...).")
            send_button.config(state=tk.NORMAL)
            return
        numbers.append(number)

    elif mode == "multiple":
        file_path = entry_file_path.get().strip()
        if not os.path.exists(file_path):
            messagebox.showerror("Error", "Contact file not found.")
            send_button.config(state=tk.NORMAL)
            return
        with open(file_path, "r") as f:
            content = f.read()
            raw_numbers = [num.strip() for num in content.split(',')]
            for number in raw_numbers:
                if number.startswith("+"):
                    numbers.append(number)
                else:
                    log_status(f"❌ Skipped invalid: {number}", "error")

    try:
        for number in numbers:
            pywhatkit.sendwhatmsg_instantly(number, message, wait_time=10, tab_close=True)
            log_status(f"✔️ Sent to: {number}", "success")
        messagebox.showinfo("Done", "All messages processed.")
    except Exception as e:
        log_status(f"❌ Error: {str(e)}", "error")
        messagebox.showerror("Error", f"Failed to send messages:\n{e}")
    finally:
        send_button.config(state=tk.NORMAL)

def send_message():
    # Run sending in a separate thread to prevent UI freezing
    threading.Thread(target=send_message_thread).start()

def toggle_mode():
    mode = contact_mode.get()
    if mode == "single":
        entry_number.config(state=tk.NORMAL)
        entry_file_path.config(state=tk.DISABLED)
        btn_browse.config(state=tk.DISABLED)
    else:
        entry_number.config(state=tk.DISABLED)
        entry_file_path.config(state=tk.NORMAL)
        btn_browse.config(state=tk.NORMAL)

# GUI Setup
root = tk.Tk()
root.title("WhatsApp Message Sender")
root.geometry("520x580")

contact_mode = tk.StringVar(value="single")

frame_mode = tk.Frame(root)
frame_mode.pack(pady=10)
tk.Radiobutton(frame_mode, text="Single Number", variable=contact_mode, value="single", command=toggle_mode).pack(side=tk.LEFT, padx=10)
tk.Radiobutton(frame_mode, text="Upload Contact List (Comma Separated)", variable=contact_mode, value="multiple", command=toggle_mode).pack(side=tk.LEFT, padx=10)

# Single number entry
label_number = tk.Label(root, text="Phone Number (with +country code):")
label_number.pack()
entry_number = tk.Entry(root, width=40)
entry_number.pack()

# File upload for multiple numbers
label_file = tk.Label(root, text="Contact List File (.txt with comma-separated numbers):")
label_file.pack()
entry_file_path = tk.Entry(root, width=40, state=tk.DISABLED)
entry_file_path.pack()
btn_browse = tk.Button(root, text="Browse", command=choose_file, state=tk.DISABLED)
btn_browse.pack(pady=5)

# Message input
label_message = tk.Label(root, text="Enter Message:")
label_message.pack(pady=5)
entry_message = tk.Text(root, height=6, width=58)
entry_message.pack()

# Send button
send_button = tk.Button(root, text="Send WhatsApp Message(s)", command=send_message)
send_button.pack(pady=10)

# Status display box
label_status = tk.Label(root, text="Status:")
label_status.pack()
status_box = tk.Text(root, height=10, width=58, state=tk.DISABLED)
status_box.pack(pady=5)

# Text color tags
status_box.tag_config("success", foreground="green")
status_box.tag_config("error", foreground="red")
status_box.tag_config("info", foreground="blue")

toggle_mode()
root.mainloop()
