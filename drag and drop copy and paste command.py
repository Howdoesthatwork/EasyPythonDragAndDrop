import tkinter as tk
from tkinter import messagebox, filedialog
import os
from tkinterdnd2 import DND_FILES, TkinterDnD
import pyperclip
import sys
from PIL import Image, ImageTk

# File to track whether the user guide has been shown
GUIDE_FILE = 'user_guide_shown.txt'

def show_user_guide():
    """Display the user guide in a popup window."""
    guide_text = (
        "Welcome to the Drag-and-Drop Python Command Copier!\n\n"
        "This application allows you to quickly create and copy commands to run Python scripts "
        "from the command line by simply dragging and dropping your Python files onto the window.\n\n"
        "What You Need to Do:\n"
        "1. Run the Application: Start the application by running the Python script. "
        "This will open a small window at the upper middle left of your screen that remains on top of other windows.\n"
        "2. Drag and Drop a Python File: Locate a Python file (with a .py extension) on your computer. "
        "Click and drag the file into the application window.\n"
        "3. Automatic Command Generation: Once you drop the Python file into the window, the application will "
        "automatically create a command that changes the directory to where the Python file is located and executes the file.\n"
        "4. Command Copied to Clipboard: The generated command will be copied to your clipboard automatically. "
        "You will see the command displayed in the input field of the application window.\n"
        "5. Use the Command: You can now paste the command into your terminal or command prompt to run your Python script.\n\n"
        "What You Get:\n"
        "- Efficiency: Quickly create commands to run your Python scripts without manually typing the path and filename.\n"
        "- Clipboard Integration: The command is copied to your clipboard automatically, so you can easily use it elsewhere.\n"
        "- User-Friendly Interface: A simple drag-and-drop interface that requires no additional configuration.\n\n"
        "Important Notes:\n"
        "- Make sure the file you drop is a valid Python script (.py file). If you drop a file with a different extension, "
        "a warning message will inform you.\n"
        "- The application is designed to stay on top of other windows for easy access."
    )
    
    messagebox.showinfo("User Guide", guide_text)

def check_user_guide():
    """Check if the user guide has been shown before."""
    if not os.path.exists(GUIDE_FILE):
        show_user_guide()
        with open(GUIDE_FILE, 'w') as f:
            f.write("User guide shown")

def on_drop(event):
    file_path = event.data.strip().strip('{}')
        
    if file_path.endswith('.py'):
        directory = os.path.dirname(file_path)
        filename = os.path.basename(file_path)

        cd_command = f'cd "{directory}" && '
        python_command = f'python "{filename}"'
        command = cd_command + python_command
        
        pyperclip.copy(command)
        input_entry.delete(0, tk.END)
        input_entry.insert(0, command)
    else:
        messagebox.showwarning("Invalid File", "Please drop a Python (.py) file.")

def load_image():
    """Open a file dialog to select an image."""
    image_path = filedialog.askopenfilename(
        title="Select an Image",
        filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")]
    )
    
    if image_path:
        load_and_display_image(image_path)

def load_and_display_image(image_path):
    """Load and display the selected image."""
    global photo  # Keep a reference to avoid garbage collection
    image = Image.open(image_path)
    image = image.resize((580, 300), Image.LANCZOS)  # Resize image to fit the canvas
    photo = ImageTk.PhotoImage(image)

    # Clear the canvas and display the selected image
    canvas.delete("all")
    canvas.create_image(0, 0, anchor=tk.NW, image=photo)

# Set up the main window
root = TkinterDnD.Tk()
root.title("Drag and Drop Python File")
root.geometry("600x400")
root.attributes('-topmost', True)
root.geometry(f"600x400+0+0")  # Upper middle left

# Display Python version
python_version_label = tk.Label(root, text=f"Python Version: {sys.version}", bg='black', fg='white')
python_version_label.pack(pady=10)

# Create a canvas to hold the default red dot or user image
canvas = tk.Canvas(root, bg='black', width=600, height=300)
canvas.pack()

# Draw a small red dot with a ring around it
def draw_default_dot():
    dot_radius = 20
    ring_radius = dot_radius + 5
    canvas.create_oval(290 - ring_radius, 150 - ring_radius, 290 + ring_radius, 150 + ring_radius, fill='red', outline='red')
    canvas.create_oval(290 - dot_radius, 150 - dot_radius, 290 + dot_radius, 150 + dot_radius, fill='red', outline='red')

draw_default_dot()

# Button to load an image
load_image_button = tk.Button(root, text="Load Image", command=load_image)
load_image_button.pack(pady=10)

# Create a label to display the image (not needed since we draw on the canvas)
# image_label = tk.Label(root)
# image_label.pack()

# Entry widget for displaying the command
input_entry = tk.Entry(root, width=80)
input_entry.pack(pady=20)

# Check if the user guide needs to be shown
check_user_guide()

# Register drag and drop functionality
root.drop_target_register(DND_FILES)
root.dnd_bind('<<Drop>>', on_drop)

# Start the application
root.mainloop()
