import tkinter as tk
from tkinter import simpledialog, messagebox, filedialog
import subprocess
import os

class NpmProjectSetupApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Node.js Project Setup")
        
        self.folder_path = None
        self.npm_path = "C:\\Program Files\\nodejs\\npm.cmd"
        
        self.setup_ui()
        
    def setup_ui(self):
        self.root.geometry("400x200")
        self.root.configure(bg="#282c34")
        
        self.folder_label = tk.Label(self.root, text="No folder selected", bg="#282c34", fg="#abb2bf", font=("Helvetica", 12))
        self.folder_label.pack(pady=10)
        
        btn_choose_folder = tk.Button(self.root, text="Choose Folder", command=self.choose_folder, bg="#61afef", fg="#282c34", font=("Helvetica", 12))
        btn_choose_folder.pack(pady=10)
        
        self.btn_init = tk.Button(self.root, text="Initialize npm project and install nodemon", command=self.run_npm_init, state=tk.DISABLED, bg="#98c379", fg="#282c34", font=("Helvetica", 12))
        self.btn_init.pack(pady=10)
        
        self.btn_install = tk.Button(self.root, text="Install library", command=self.install_library, state=tk.DISABLED, bg="#e06c75", fg="#282c34", font=("Helvetica", 12))
        self.btn_install.pack(pady=10)

    def choose_folder(self):
        self.folder_path = filedialog.askdirectory()
        if self.folder_path:
            self.folder_label.config(text=f"Selected folder: {self.folder_path}")
            self.btn_init.config(state=tk.NORMAL)
            self.btn_install.config(state=tk.NORMAL)
        else:
            self.folder_label.config(text="No folder selected")
            self.btn_init.config(state=tk.DISABLED)
            self.btn_install.config(state=tk.DISABLED)
    
    def run_npm_init(self):
        if self.folder_path:
            try:
                subprocess.run([self.npm_path, 'init', '-y'], cwd=self.folder_path, check=True)
                subprocess.run([self.npm_path, 'install', '--save-dev', 'nodemon'], cwd=self.folder_path, check=True)
                package_json_path = os.path.join(self.folder_path, 'package.json')
                with open(package_json_path, 'r') as file:
                    package_json = file.read()
                
                package_json = package_json.replace(
                    '"scripts": {',
                    '"scripts": {\n    "start": "nodemon server.js",'
                )
                
                with open(package_json_path, 'w') as file:
                    file.write(package_json)
                
                messagebox.showinfo("Success", "npm project initialized and nodemon installed successfully.")
            except subprocess.CalledProcessError as e:
                messagebox.showerror("Error", f"An error occurred: {e}")
    
    def install_library(self):
        if self.folder_path:
            library_name = simpledialog.askstring("Input", "Enter the library to install:")
            if library_name:
                try:
                    subprocess.run([self.npm_path, 'install', library_name], cwd=self.folder_path, check=True)
                    messagebox.showinfo("Success", f"{library_name} installed successfully.")
                except subprocess.CalledProcessError as e:
                    messagebox.showerror("Error", f"An error occurred: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = NpmProjectSetupApp(root)
    root.mainloop()
