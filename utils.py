import tkinter as tk
from tkinter import messagebox
import smtplib
from email.mime.text import MIMEText
import json
import os

def load_config():
    CONFIG_FILE = "config.json"
    if not os.path.exists(CONFIG_FILE):
        default_config = {
            "admin_email": "admin@example.com",
            "sender_email": "sender@example.com",
            "sender_password": "your_password_here"
        }
        with open(CONFIG_FILE, 'w') as f:
            json.dump(default_config, f)
        print("Created default config.json. Please update with valid email credentials.")
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)

def send_alert_email(admin_email, sender_email, sender_password):
    msg = MIMEText("Unauthorized access attempt detected.")
    msg['Subject'] = "Security Alert"
    msg['From'] = sender_email
    msg['To'] = admin_email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, admin_email, msg.as_string())
        server.quit()
        print("Alert email sent.")
    except Exception as e:
        print(f"Failed to send email: {e}")

def view_file(file_path):
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        view_window = tk.Toplevel()
        view_window.title(os.path.basename(file_path))
        text_area = tk.Text(view_window)
        text_area.insert(tk.END, content)
        text_area.pack(fill='both', expand=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not open file: {e}")

def create_file_window(protected_dir, refresh_callback):
    create_window = tk.Toplevel()
    create_window.title("Create New File")
    file_name_label = tk.Label(create_window, text="File Name:")
    file_name_entry = tk.Entry(create_window)
    content_label = tk.Label(create_window, text="Content:")
    content_text = tk.Text(create_window, height=10)
    save_button = tk.Button(create_window, text="Save", command=lambda: save_file())

    file_name_label.pack(padx=5, pady=5)
    file_name_entry.pack(padx=5, pady=5)
    content_label.pack(padx=5, pady=5)
    content_text.pack(padx=5, pady=5)
    save_button.pack(pady=10)

    def save_file():
        file_name = file_name_entry.get()
        if file_name:
            file_path = os.path.join(protected_dir, file_name)
            with open(file_path, 'w') as f:
                f.write(content_text.get("1.0", tk.END))
            create_window.destroy()
            refresh_callback()
        else:
            messagebox.showerror("Error", "File name cannot be empty.")