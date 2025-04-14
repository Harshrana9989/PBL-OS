import tkinter as tk
from tkinter import messagebox
import os
from utils import view_file, create_file_window

class AdminFrame(tk.Frame):
    def __init__(self, parent, logout_callback):
        super().__init__(parent)
        self.logout_callback = logout_callback
        self.protected_dir = "protected_files"

        # Create widgets
        self.file_listbox = tk.Listbox(self)
        self.view_button = tk.Button(self, text="View", command=self.view_file)
        self.create_button = tk.Button(self, text="Create", command=self.create_file)
        self.delete_button = tk.Button(self, text="Delete", command=self.delete_file)
        self.logout_button = tk.Button(self, text="Logout", command=self.logout_callback)

        # Layout
        self.file_listbox.pack(fill='both', expand=True, padx=5, pady=5)
        self.view_button.pack(side='left', padx=5, pady=5)
        self.create_button.pack(side='left', padx=5, pady=5)
        self.delete_button.pack(side='left', padx=5, pady=5)
        self.logout_button.pack(side='right', padx=5, pady=5)

    def refresh_file_list(self):
        self.file_listbox.delete(0, tk.END)
        files = os.listdir(self.protected_dir)
        for file in files:
            self.file_listbox.insert(tk.END, file)

    def view_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            file_path = os.path.join(self.protected_dir, selected_file)
            view_file(file_path)
        else:
            messagebox.showinfo("Info", "Please select a file to view.")

    def create_file(self):
        create_file_window(self.protected_dir, self.refresh_file_list)

    def delete_file(self):
        selected_file = self.file_listbox.get(tk.ACTIVE)
        if selected_file:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {selected_file}?")
            if confirm:
                file_path = os.path.join(self.protected_dir, selected_file)
                os.remove(file_path)
                self.refresh_file_list()
        else:
            messagebox.showinfo("Info", "Please select a file to delete.")