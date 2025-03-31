import sqlite3
import customtkinter as ctk
from tkinter import ttk
import datetime

#Creates the database used to store the data
def create_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor ()
    cursor.execute ('''CREATE TABLE IF NOT EXISTS inventory (name TEXT, date TEXT,quantity INT, type TEXT, id INTEGER PRIMARY KEY AUTOINCREMENT)''')
    conn.commit()
    conn.close()

#Delete the selected item in the tree
def delete_selected_item(tree):
    """Delete the selected record from the database."""
    selected_item = tree.selection()  # Get the selected item
    if selected_item:
        item_values = tree.item(selected_item, "values")  # Get the values of the selected item
        item_id = item_values[4]  # Assuming 'ID' is in the fifth column

        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("DELETE FROM inventory WHERE id = ?", (item_id,))
        conn.commit()
        conn.close()

        # Remove the item from the Treeview
        tree.delete(selected_item)
        print(f"Record with ID {item_id} deleted successfully!")

#Fetches all of the data from within the database
def fetch_data_from_database():
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM inventory")
    records = cursor.fetchall()
    conn.close()
    return records

#Refreshes the database after the values have changed
def refresh_treeview(tree):
    """Refresh the Treeview with updated data from the database."""
    for row in tree.get_children():
        tree.delete(row)  # Clear existing data in Treeview
    data = fetch_data_from_database()
    for record in data:
        tree.insert("", ctk.END, values=record)



#Takes the inputted values and adds them to the database
def add_item_to_database(tree, entries):
    """Add a new record to the database."""
    name = entries[0].get()  # Get Name input
    item_type = entries[1].get()  # Get Type input
    quantity = entries[2].get()  # Get Quantity input

    if name and item_type and quantity.isdigit() and len(quantity) <= 8:  # Validate inputs
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("INSERT INTO inventory (name, date, quantity, type) VALUES (?, ?, ?, ?)",
                       (name, datetime.date.today().strftime("%Y-%m-%d"), int(quantity), item_type))
        conn.commit()
        conn.close()

        # Clear inputs after successful addition
        for entry in entries:
            entry.delete(0, ctk.END)

        # Refresh the Treeview to show the new record
        refresh_treeview(tree)
        print(f"Added {name} to the database!")
    else:
        print("Invalid input. Please check the fields.")
    
#Empties the inputs within the 'add new item' area
def clear_fields(entries):
    """Clear all input fields."""
    for entry in entries:
        entry.delete(0, ctk.END)
    print("Fields cleared!")

# Global variable to store the selected record ID
selected_record_id = None

# Edit the selected record
def edit_selected_record(tree, entries):
    global selected_record_id  # Declare global variable to store ID
    selected_item = tree.selection()  # Get the selected item
    if selected_item:
        item_values = tree.item(selected_item, "values")  # Get the values of the selected item
        # Fill the input fields with the selected item's data
        entries[0].delete(0, ctk.END)
        entries[0].insert(0, item_values[0])  # Name
        entries[1].delete(0, ctk.END)
        entries[1].insert(0, item_values[3])  # Type
        entries[2].delete(0, ctk.END)
        entries[2].insert(0, item_values[2])  # Quantity
        selected_record_id = item_values[4]  # Store the ID of the selected item
        print(f"Editing record with ID {selected_record_id}...")

# Confirm the edited record
def confirm_edited_record(tree, entries):
    global selected_record_id  # Access the stored ID
    name = entries[0].get()  # Get Name input
    item_type = entries[1].get()  # Get Type input
    quantity = entries[2].get()  # Get Quantity input
    if selected_record_id and name and item_type and quantity.isdigit() and len(quantity) <= 8:  # Validate inputs
        conn = sqlite3.connect("inventory.db")
        cursor = conn.cursor()
        cursor.execute("UPDATE inventory SET name = ?, type = ?, quantity = ? WHERE id = ?", 
                       (name, item_type, int(quantity), selected_record_id))
        conn.commit()
        conn.close()
        # Clear the input fields after editing
        clear_fields(entries)
        # Refresh the Treeview to show the updated record
        refresh_treeview(tree)
        print(f"Record with ID {selected_record_id} updated successfully!")
        selected_record_id = None  # Reset the global variable to allow adding new records
    else:
        print("Invalid input or no record selected. Ensure quantity is up to 8 digits.")


#Builts the visual interface
def create_gui():
    ctk.set_appearance_mode("System")
    ctk.set_default_color_theme("blue")

    root = ctk.CTk()
    root.title("Inventory Manager")
    root.geometry("1000x600")  # Adjust as needed

    # --- Grid Layout Configuration ---
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=10)  # Treeview (very wide)
    root.grid_columnconfigure(1, weight=1)  # Right frame

    # --- Middle Frame (Treeview Table) ---
    middle_frame = ctk.CTkFrame(root, corner_radius=0)
    middle_frame.grid(row=0, column=0, sticky="nswe", padx=10, pady=10)

    style = ttk.Style()
    style.configure("Treeview", font=("Arial", 12), padding=(0,0)) # Set cell font size to 20
    style.configure("Treeview.Heading", font=("Arial", 13, "bold"), bg ="black") # Set heading font size to 20

    tree = ttk.Treeview(middle_frame, columns=("Name", "Date", "Quantity", "Type", "ID"), show="headings")
    tree.heading("Name", text="Item Name", )
    tree.heading("Date", text="Date Added")
    tree.heading("Quantity", text="Quantity")
    tree.heading("Type", text="Type")
    tree.heading("ID", text="ID")
    tree.pack(fill=ctk.BOTH, expand=True)

    tree.column("Name", width=180)
    tree.column("Date", width=100)
    tree.column("Quantity", width=100)
    tree.column("Type", width=100)
    tree.column("ID", width=100)

    # Add Example Data
    today = datetime.date.today()


    data = fetch_data_from_database()
    for record in data:
        tree.insert("", ctk.END, values=record)

    # --- Right Frame (Search and Input) ---
    right_frame = ctk.CTkFrame(root, corner_radius=0)
    right_frame.grid(row=0, column=1, sticky="nswe", padx=10, pady=10)

    # --- Input Section ---
    input_section = ctk.CTkFrame(right_frame, corner_radius=0)
    input_section.pack(fill="x", pady=5)

    #input_label = ctk.CTkLabel(input_section, text="Add New Record")
    #input_label.pack()

    labels = ["Name", "Type", "Quantity"]
    entries = []
    for label_text in labels:
        label = ctk.CTkLabel(input_section, text=label_text, anchor="w")
        label.pack(fill="x")
        entry = ctk.CTkEntry(input_section)
        entry.pack(fill="x")
        entries.append(entry)

    input_button_frame = ctk.CTkFrame(input_section, corner_radius=0)
    input_button_frame.pack(fill="x", pady=5)
    input_add = ctk.CTkButton(input_button_frame, text="Add")
    input_add.pack(side="left", padx=5)
    input_add.configure(command=lambda: add_item_to_database(tree, entries))

    input_cancel = ctk.CTkButton(input_button_frame, text="Cancel")
    input_cancel.pack(side="left")
    input_cancel.configure(command=lambda: clear_fields(entries)) 



    # Add "Edit" and "Confirm" buttons (new line)
    input_edit_frame = ctk.CTkFrame(input_section, corner_radius=0)  # New Frame for positioning
    input_edit_frame.pack(fill="x", pady=(5, 0))  # Slight padding to separate from above buttons

    input_edit = ctk.CTkButton(input_edit_frame, text="Edit")
    input_edit.pack(side="left", padx=5)  # Positioned to the left
    input_edit.configure(command=lambda: edit_selected_record(tree, entries))

    input_confirm = ctk.CTkButton(input_edit_frame, text="Confirm")
    input_confirm.pack(side="left")  # Positioned next to the "Edit" button#
    input_confirm.configure(command=lambda: confirm_edited_record(tree, entries))

    


    # --- Search Section ---
    search_section = ctk.CTkFrame(right_frame, corner_radius=0)
    search_section.pack(fill="x", pady=5)

    search_label = ctk.CTkLabel(search_section, text="Search")
    search_label.pack(fill="x")
    search_entry = ctk.CTkEntry(search_section)
    search_entry.pack(fill="x")

    search_button_frame = ctk.CTkFrame(search_section, corner_radius=0)
    search_button_frame.pack(fill="x", pady=5)
    search_confirm = ctk.CTkButton(search_button_frame, text="Confirm")
    search_confirm.pack(side="left", padx=5)
    search_cancel = ctk.CTkButton(search_button_frame, text="Cancel")
    search_cancel.pack(side="left")

    # --- Delete/Refresh Section ---
    delete_refresh_section = ctk.CTkFrame(right_frame, corner_radius=0)
    delete_refresh_section.pack(fill="x", pady=5)

    delete_button = ctk.CTkButton(delete_refresh_section, text="Delete")
    delete_button.pack(side="left", padx=5)
    delete_button.configure(command=lambda: delete_selected_item(tree))

    refresh_button = ctk.CTkButton(delete_refresh_section, text="Refresh")
    refresh_button.pack(side="left")

        # --- Exit Button ---
    exit_button = ctk.CTkButton(right_frame, text="Exit", command=root.destroy)
    exit_button.pack(side="bottom", pady=10)  # Positioned at the bottom of the right frame

    
    
    root.mainloop()
#add_fake_data()
if __name__ == "__main__":
    create_gui()
