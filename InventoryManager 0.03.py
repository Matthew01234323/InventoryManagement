#Uses tkinter library for everything that is graphically based
import tkinter as tk

# Creates the main window
root = tk.Tk()
root.title("InventoryManager")
root.geometry("1200x800")  # Sets the window size

#Variables for the frames. This is so I can change the size of the frames more easily in the future
optionsWidth = 252
optionsHeight = 800

# Function to close the application
def exit_application():
    root.destroy()
      # Closes the window


# Creates a frame on the left for the buttons. I am calling them options.
options_frame = tk.Frame(root)
options_frame.place (x=0, y = 0, width = optionsWidth, height = optionsHeight)

#Creates a frame on the top of the screen for the different data types. I am calling them datatype.
datatype_grid = tk.Frame(root, bg ="black")
datatype_grid.place (x= optionsWidth, y = 0, width = 1200-optionsWidth)

datatype = ["Name", "Date added", "Quantity", "Type", "Item ID"]

""""
#Creates the name column seperatly since it is wider than the others
datatypeDisplay = tk.Label(datatype_grid, text="Name", width=25, font=("Arial", 16))
datatypeDisplay.grid(row=0, column=0, padx=0, pady=35, sticky="w")  # Use grid to place in row 0 and increment column
"""

for i in range(4):  # Sets the weight of every column but 'name' to 1
    datatype_grid.grid_columnconfigure(i+1, weight=1)
#Sets the weight of 'name' to two, so it has double the space
datatype_grid.grid_columnconfigure(0, weight=2)

#Creates the datatype columns
for i, item in enumerate(datatype):
    datatypeDisplay = tk.Label(datatype_grid, text=item, font=("Arial", 16), height = 4 )
    datatypeDisplay.grid(row=0, column=i, padx=1, pady=0, sticky = "nsew")  # Use grid to place in rows and increment column


# Creates multiple buttons and add them to the frame
options = ["Add", "Delete", "Edit", "Search", "Cancel", "Save", "Exit"]

# Ensure each button takes up 1/7th of the space within the frame - options_frame
for item in options:
    optionsDisplay = tk.Button(options_frame, text=item, width=17, font=("Arial", 16))
    optionsDisplay.pack(fill=tk.BOTH, expand=True)

      # Assign the exit function to the Exit button
    if item == "Exit":
        optionsDisplay.config(command=exit_application)


# Loads and displays the data in the file
def load_data():
    with open("data.txt", "r") as file:
        data = file.readlines()
        for i, line in enumerate(data):
            # Create a Label for each line of data and place it in the grid below the datatype labels
            data_display = tk.Label(datatype_grid, text=line.strip(), font=("Arial", 14))
            data_display.grid(row=i+1, column=0, columnspan=5, padx=0, pady=5, sticky="w")  # Spanning all columns

# Load data from data.txt into the GUI
load_data()

# Run the Tkinter main loop
root.mainloop()

