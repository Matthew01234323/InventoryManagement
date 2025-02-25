import tkinter as tk

# Creates the main window
root = tk.Tk()
root.title("InventoryManager")
root.geometry("1200x800")  # Sets the window size

#Variables for the frames. This is so I can change the size of the frames more easily in the future
optionsWidth = 252
optionsHeight = 800

# Creates a frame on the left for the buttons. I am calling them options.
options_frame = tk.Frame(root)
options_frame.place (x=0, y = 0, width = optionsWidth, height = optionsHeight)

#Creates a frame on the top of the screen for the different data types. I am calling them datatype.
datatype_grid = tk.Frame(root)
datatype_grid.place (x= optionsWidth, y = 0, width = 1200-optionsWidth)

datatype = ["Date added", "Quantity", "Type", "Item ID"]

#Creates the name column seperatly since it is wider than the others
datatypeDisplay = tk.Label(datatype_grid, text="Name", width=25, font=("Arial", 16))
datatypeDisplay.grid(row=0, column=0, padx=0, pady=35, sticky="w")  # Use grid to place in row 0 and increment column

for i in range(5):  # 5 columns
    datatype_grid.grid_columnconfigure(i, weight=1)

#Creates the remaining datatype columns
for i, item in enumerate(datatype):
    datatypeDisplay = tk.Label(datatype_grid, text=item, font=("Arial", 16), )
    datatypeDisplay.grid(row=0, column=i+1, padx=0, pady=35, sticky="w")  # Use grid to place in row 0 and increment column


# Creates multiple buttons and add them to the frame
options = ["Add", "Delete", "Edit", "Search", "Cancel", "Save", "Exit"]

# Ensure each button takes up 1/7th of the space within the frame - options_frame
for item in options:
    optionsDisplay = tk.Button(options_frame, text=item, width=17, font=("Arial", 16))
    optionsDisplay.pack(fill=tk.BOTH, expand=True)

# Add dividers between the columns using Frames
divider_width = 2
for i in range(1, 5):  # Create 4 dividers for 5 columns (between each column)
    divider = tk.Frame(datatype_grid, width=divider_width, bg="black")
    divider.grid(row=0, column=i, sticky="ns", padx=0)  # Place the divider in the correct position


# Run the Tkinter main loop
root.mainloop()

