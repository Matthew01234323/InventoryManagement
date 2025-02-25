import tkinter as tk

# Create the main window
root = tk.Tk()
root.title("Tkinter Button Layout")
root.geometry("1200x800")  # Sets the window size

# Create a frame for the buttons on the left hand side, I am calling them options
options_frame = tk.Frame(root)
options_frame.place (x=0, y = 0, width = 250, height = 800)

# Create multiple buttons and add them to the frame
buttons = ["Add", "Delete", "Edit", "Search", "Cancel", "Save", "Exit"]

# Ensure each button takes up 1/7th of the space within the frame
for item in buttons:
    button = tk.Button(options_frame, text=item, width=17, font=("Arial", 16))
    button.pack(fill=tk.BOTH, expand=True)

# Run the Tkinter main loop
root.mainloop()
