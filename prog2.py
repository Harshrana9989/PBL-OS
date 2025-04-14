import tkinter as tk
from login_frame import LoginFrame
from admin_frame import AdminFrame
from readonly_frame import ReadOnlyFrame
from auth import authenticate
from utils import send_alert_email, load_config
import logging
import os

# Setup logging
logging.basicConfig(filename='access.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Ensure protected directory exists
PROTECTED_DIR = "protected_files"
if not os.path.exists(PROTECTED_DIR):
    os.makedirs(PROTECTED_DIR)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Access Control System")
        self.geometry("600x400")
        self.config = load_config()
        self.current_user = None
        self.current_role = None

        # Create frames
        self.login_frame = LoginFrame(self, self.login_callback)
        self.admin_frame = AdminFrame(self, self.logout_callback)
        self.readonly_frame = ReadOnlyFrame(self, self.logout_callback)

        # Show login frame initially
        self.login_frame.pack(fill='both', expand=True)

    def login_callback(self, username, password):
        role = authenticate(username, password)
        if role:
            self.current_user = username
            self.current_role = role
            self.login_frame.pack_forget()
            if role == 'admin':
                self.admin_frame.pack(fill='both', expand=True)
                self.admin_frame.refresh_file_list()
            elif role == 'readonly':
                self.readonly_frame.pack(fill='both', expand=True)
                self.readonly_frame.refresh_file_list()
            logging.info(f"Successful login for {username}")
        else:
            self.login_frame.show_message("Login failed. Invalid credentials.")
            logging.info(f"Failed login attempt for {username}")
            send_alert_email(self.config['admin_email'], self.config['sender_email'], self.config['sender_password'])

    def logout_callback(self):
        self.current_user = None
        self.current_role = None
        self.admin_frame.pack_forget()
        self.readonly_frame.pack_forget()
        self.login_frame.pack(fill='both', expand=True)
        self.login_frame.clear_fields()

if __name__ == "__main__":
    app = App()
    app.mainloop()