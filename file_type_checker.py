import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from plyer import notification
from tkinter import Tk, filedialog

# Define magic numbers for file types with associated danger levels
MAGIC_NUMBERS = {
    'JPEG': ('FFD8FF', 1),
    'PNG': ('89504E47', 1),
    'GIF': ('47494638', 1),
    'PDF': ('25504446', 2),
    'ZIP': ('504B0304', 3),
    'RAR': ('52617221', 3),
    'EXE': ('4D5A', 10),                   
    'DLL': ('4D5A', 10),                   
    'DOC': ('D0CF11E0A1B11AE1', 5),       
    'DOCX': ('504B0304', 5),              
    'XLS': ('D0CF11E0A1B11AE1', 5),       
    'XLSX': ('504B0304', 5),              
    'PPT': ('D0CF11E0A1B11AE1', 5),       
    'PPTX': ('504B0304', 5),              
    'JS': ('2F2A', 9),                    
    'BAT': ('4D5A', 9),                   
    'SH': ('2321', 9),                    
    'ISO': ('4344303031', 8),             
    'LNK': ('4C00000001140200', 8)
}

# Function to convert danger level to a verbal description
def danger_level_description(danger_level):
    if danger_level <= 3:
        return "Low Risk"
    elif danger_level <= 6:
        return "Moderate Risk"
    elif danger_level <= 8:
        return "High Risk"
    else:
        return "Very High Risk"

# Function to read file magic number
def get_file_signature(file_path):
    try:
        with open(file_path, 'rb') as file:
            file_header = file.read(8).hex().upper()
            return file_header
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

# Function to detect file type and get its danger level
def detect_file_type(file_path):
    file_signature = get_file_signature(file_path)
    if file_signature is None:
        return None, None
    
    for file_type, (magic_number, danger_level) in MAGIC_NUMBERS.items():
        if file_signature.startswith(magic_number):
            return file_type, danger_level
    
    return "Unknown", None

# Notification function to alert the user
def notify_user(file_name, file_type, danger_level):
    title = "File Type Detected"
    
    if file_type == "Unknown":
        message = f"File: {file_name}\nType: {file_type}"
    else:
        risk_description = danger_level_description(danger_level)
        message = (f"File: {file_name}\n"
                   f"Type: {file_type}\n"
                   f"Danger Level: {danger_level}/10 ({risk_description})")
    
    if danger_level is not None and danger_level >= 7:
        message += "\nWarning: This file type is considered highly dangerous!"
    
    notification.notify(
        title=title,
        message=message,
        app_name='File Type Detector',
        timeout=10
    )

# Event handler class for directory monitoring
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            file_path = event.src_path
            file_name = os.path.basename(file_path)

            # Check the file type
            file_type, danger_level = detect_file_type(file_path)
            
            # Notify the user
            notify_user(file_name, file_type, danger_level)
            risk_description = danger_level_description(danger_level)
            print(f"Detected {file_type} for {file_name} "
                  f"(Danger Level: {danger_level}/10 - {risk_description})")

# Main function to monitor a directory
def monitor_directory(path_to_watch):
    event_handler = FileHandler()
    observer = Observer()
    observer.schedule(event_handler, path_to_watch, recursive=False)
    
    observer.start()
    print(f"Monitoring directory: {path_to_watch}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()

# Function to check file type for a selected file
def check_file_type():
    # Use Tkinter to open a file selection dialog
    root = Tk()
    root.withdraw()  # Hide the root window

    # Update the root and call file dialog after a slight delay to avoid any issues
    root.update()
    file_path = filedialog.askopenfilename(title="Select a file to check")
    
    if file_path:
        file_name = os.path.basename(file_path)
        file_type, danger_level = detect_file_type(file_path)
        
        if file_type:
            notify_user(file_name, file_type, danger_level)
            risk_description = danger_level_description(danger_level)
            print(f"Detected {file_type} for {file_name} "
                  f"(Danger Level: {danger_level}/10 - {risk_description})")
        else:
            print("Could not determine the file type.")
    else:
        print("No file selected.")
    
    root.destroy()  # Properly close the Tkinter instance

# Main entry point
if __name__ == "__main__":
    # Ask the user if they want to monitor a directory or check a file
    choice = input("Enter '1' to monitor a directory or '2' to check a file: ")

    if choice == '1':
        path_to_watch = input("Please enter the directory you want to monitor: ")

        # Validate if the provided directory exists
        if not os.path.isdir(path_to_watch):
            print(f"The directory '{path_to_watch}' does not exist.")
        else:
            monitor_directory(path_to_watch)
    elif choice == '2':
        check_file_type()
    else:
        print("Invalid option.")
