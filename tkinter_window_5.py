import tkinter as tk
from tkinter import ttk
import csv
import os
import webbrowser

# Function to update category dropdown
def update_category():
    new_category = new_category_entry.get()
    if new_category:
        current_values = list(category_dropdown['values'])
        current_values.append(new_category)
        category_dropdown['values'] = current_values
        new_category_entry.delete(0, tk.END)

# Function to populate Treeview from CSV
def populate_listbox():
    for row in item_tree.get_children():
        item_tree.delete(row)
    
    if os.path.exists('inventory.csv'):
        with open('inventory.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header row
            for row in csv_reader:
                item_tree.insert("", tk.END, values=(row[0], row[1], row[2], row[3], row[4], row[5]))

# Function to update notes
def update_notes():
    selected = item_tree.selection()
    if selected:
        item = selected[0]
        new_notes = notes_text.get(1.0, tk.END).strip()
        
        rows = []
        with open('inventory.csv', 'r') as f:
            csv_reader = csv.reader(f)
            rows = [row for row in csv_reader]
        
        for i, row in enumerate(rows[1:], start=1):
            if row[0] == item_tree.item(item, "values")[0]:
                rows[i][6] = new_notes  # Update the notes in the selected row
                break
        
        with open('inventory.csv', 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(rows)
        
        populate_listbox()

# Function to open link of selected item
def open_link():
    selected = item_tree.selection()
    if selected:
        item = selected[0]
        with open('inventory.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                if row[0] == item_tree.item(item, "values")[0]:
                    webbrowser.open(row[4])
                    break

# Function to populate notes when an item is selected
def populate_notes(event):
    selected = item_tree.selection()
    if selected:
        item = selected[0]
        with open('inventory.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                if row[0] == item_tree.item(item, "values")[0]:
                    notes_text.delete(1.0, tk.END)
                    notes_text.insert(tk.END, row[6])
                    break

# Initialize main window
root = tk.Tk()
root.title("Inventory Management")

# Initialize frames
input_frame = tk.Frame(root)
input_frame.pack(side=tk.LEFT, padx=10, pady=10)

notes_frame = tk.Frame(root)
notes_frame.pack(side=tk.LEFT, padx=10, pady=10)

stats_frame = tk.Frame(root)
stats_frame.pack(side=tk.LEFT, padx=10, pady=10)

# Initialize widgets for input frame
tk.Label(input_frame, text="Item").grid(row=0, column=0)
item_entry = tk.Entry(input_frame)
item_entry.grid(row=0, column=1)

tk.Label(input_frame, text="Cost").grid(row=1, column=0)
cost_entry = tk.Entry(input_frame)
cost_entry.grid(row=1, column=1)

tk.Label(input_frame, text="QTY").grid(row=2, column=0)
qty_entry = tk.Entry(input_frame)
qty_entry.grid(row=2, column=1)

tk.Label(input_frame, text="Vendor").grid(row=3, column=0)
vendor_entry = tk.Entry(input_frame)
vendor_entry.grid(row=3, column=1)

tk.Label(input_frame, text="Link").grid(row=4, column=0)
link_entry = tk.Entry(input_frame)
link_entry.grid(row=4, column=1)

tk.Label(input_frame, text="Category").grid(row=5, column=0)
category_var = tk.StringVar()
category_dropdown = ttk.Combobox(input_frame, textvariable=category_var)
category_dropdown.grid(row=5, column=1)
category_dropdown['values'] = ('Electronics', 'Furniture', 'Stationary')

# For adding new Category
tk.Label(input_frame, text="New Category").grid(row=6, column=0)
new_category_entry = tk.Entry(input_frame)
new_category_entry.grid(row=6, column=1)
add_category_button = tk.Button(input_frame, text="Add", command=update_category)
add_category_button.grid(row=6, column=2)

# Initialize widgets for notes frame
tk.Label(notes_frame, text="Inventory Items").grid(row=0, column=0)
tree_frame = tk.Frame(notes_frame)
tree_frame.grid(row=1, column=0, columnspan=2)

# Create Treeview with Scrollbar
scrollbar = tk.Scrollbar(tree_frame, orient=tk.VERTICAL)
item_tree = ttk.Treeview(tree_frame, columns=("Name", "Cost", "QTY", "Vendor", "Link", "Category"), yscrollcommand=scrollbar.set, show='headings')
scrollbar.config(command=item_tree.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

item_tree.pack(side=tk.LEFT, fill=tk.BOTH)
for col in ("Name", "Cost", "QTY", "Vendor", "Link", "Category"):
    item_tree.heading(col, text=col)
    item_tree.column(col, width=100)

# Function to populate entry fields and notes when an item is selected
def populate_fields_and_notes(event):
    selected = item_tree.selection()
    if selected:
        item = selected[0]
        details = item_tree.item(item, "values")
        
        # Populate entry fields
        item_entry.delete(0, tk.END)
        item_entry.insert(0, details[0])
        
        cost_entry.delete(0, tk.END)
        cost_entry.insert(0, details[1])
        
        qty_entry.delete(0, tk.END)
        qty_entry.insert(0, details[2])
        
        vendor_entry.delete(0, tk.END)
        vendor_entry.insert(0, details[3])
        
        link_entry.delete(0, tk.END)
        link_entry.insert(0, details[4])
        
        category_var.set(details[5])

        # Populate notes
        with open('inventory.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header
            for row in csv_reader:
                if row[0] == item_tree.item(item, "values")[0]:
                    notes_text.delete(1.0, tk.END)
                    notes_text.insert(tk.END, row[6])
                    break

# Function to submit a new entry or update an existing one
def submit_entry():
    selected = item_tree.selection()
    
    item = item_entry.get()
    cost = cost_entry.get()
    qty = qty_entry.get()
    vendor = vendor_entry.get()
    link = link_entry.get()
    category = category_var.get()
    
    # Read the existing rows
    rows = []
    if os.path.exists('inventory.csv'):
        with open('inventory.csv', 'r') as f:
            csv_reader = csv.reader(f)
            rows = [row for row in csv_reader]

    if selected:  # Update operation
        item_id = selected[0]
        for i, row in enumerate(rows[1:], start=1):
            if row[0] == item_tree.item(item_id, "values")[0]:
                rows[i] = [item, cost, qty, vendor, link, category, rows[i][6]]
                break
    else:  # Insert operation
        rows.append([item, cost, qty, vendor, link, category, ""])
    
    # Write the rows back to the CSV
    with open('inventory.csv', 'w', newline='') as f:
        csv_writer = csv.writer(f)
        csv_writer.writerows(rows)
    
    populate_listbox()

# Function to delete an entry
def delete_entry():
    selected = item_tree.selection()
    if selected:
        item_id = selected[0]
        
        # Read existing rows
        rows = []
        with open('inventory.csv', 'r') as f:
            csv_reader = csv.reader(f)
            rows = [row for row in csv_reader]
        
        # Remove the selected row
        for i, row in enumerate(rows[1:], start=1):
            if row[0] == item_tree.item(item_id, "values")[0]:
                del rows[i]
                break
        
        # Write the updated rows back to the CSV
        with open('inventory.csv', 'w', newline='') as f:
            csv_writer = csv.writer(f)
            csv_writer.writerows(rows)
        
        populate_listbox()

# Replace the existing submit button with this new one
submit_button = tk.Button(input_frame, text="Submit", command=submit_entry)
submit_button.grid(row=7, column=1, pady=10)

# Add a delete button
delete_button = tk.Button(input_frame, text="Delete", command=delete_entry)
delete_button.grid(row=7, column=2, pady=10, padx=5)

# Add a double-click event to populate the entry fields and notes
item_tree.bind('<Double-1>', populate_fields_and_notes)

# Global variable to keep track of the sort order
sort_by = {'column': None, 'reverse': False}

# Sorting function
def treeview_sort_column(tv, col):
    global sort_by
    
    # Retrieve the items from the Treeview widget
    items_list = [(tv.set(k, col), k) for k in tv.get_children('')]

    if col in ["Cost", "QTY"]:  # Columns that should be sorted as numbers
        # Convert to float for sorting
        items_list = [(float(x) if x else 0.0, k) for x, k in items_list]

    # Sort the items
    items_list.sort(reverse=sort_by['reverse'])

    # Rearrange the items in the Treeview
    for index, (_, k) in enumerate(items_list):
        tv.move(k, '', index)

    # Reverse the sort order for the next time
    sort_by['column'] = col
    sort_by['reverse'] = not sort_by['reverse']

    # Update the header arrow accordingly
    tv.heading(col, command=lambda: treeview_sort_column(tv, col))
    
# Bind the function to the Treeview columns
for col in ("Name", "Cost", "QTY", "Vendor", "Link", "Category"):
    item_tree.heading(col, text=col, command=lambda _col=col: treeview_sort_column(item_tree, _col))


tk.Label(notes_frame, text="Notes").grid(row=2, column=0)
notes_text = tk.Text(notes_frame, width=30, height=10)
notes_text.grid(row=3, column=0, padx=5, pady=5)

# Populate Treeview when application starts
populate_listbox()

def update_statistics():
    stats = {}  # Dictionary to hold stats per category
    total_value = 0.0  # Total value across all categories
    
    if os.path.exists('inventory.csv'):
        with open('inventory.csv', 'r') as f:
            csv_reader = csv.reader(f)
            next(csv_reader)  # Skip header row
            
            for row in csv_reader:
                category = row[5]
                cost = float(row[1]) if row[1] else 0.0
                qty = int(row[2]) if row[2] else 0
                
                if category not in stats:
                    stats[category] = {'value': 0.0, 'count': 0}
                
                stats[category]['value'] += cost * qty
                stats[category]['count'] += qty
                total_value += cost * qty
    
    # Update the 'stats_text' widget with the calculated stats
    stats_text.delete(1.0, tk.END)
    stats_text.insert(tk.END, "Inventory Statistics\n")
    stats_text.insert(tk.END, "="*20 + "\n")
    
    for category, data in stats.items():
        stats_text.insert(tk.END, f"Category: {category}\n")
        stats_text.insert(tk.END, f"  Total Value: ${data['value']}\n")
        stats_text.insert(tk.END, f"  Item Count: {data['count']}\n")
        stats_text.insert(tk.END, "-"*20 + "\n")
        
    stats_text.insert(tk.END, f"Total Inventory Value: ${total_value}\n")

# Initialize widgets for stats frame
tk.Label(stats_frame, text="Statistics").grid(row=0, column=0)
stats_text = tk.Text(stats_frame, width=30, height=10)
stats_text.grid(row=1, column=0, padx=5, pady=5)

# Add a button to update statistics
update_stats_button = tk.Button(stats_frame, text="Update Stats", command=update_statistics)
update_stats_button.grid(row=2, column=0, pady=5)

# Initially populate statistics
update_statistics()

# For opening link of selected item
open_link_button = tk.Button(notes_frame, text="Open Link", command=open_link)
open_link_button.grid(row=4, column=0, pady=5)

# For updating notes
update_notes_button = tk.Button(notes_frame, text="Update Notes", command=update_notes)
update_notes_button.grid(row=5, column=0, pady=5)

# Add a double-click event to populate the entry fields and notes
item_tree.bind('<Double-1>', populate_fields_and_notes)

# Function to populate category dropdown from CSV
def populate_categories_from_csv():
    categories = set()
    with open('inventory.csv', 'r') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  # Skip header row
        for row in csvreader:
            categories.add(row[5])  # Assuming category is in the 6th column (0-indexed)
    category_dropdown['values'] = list(categories)

# Populate categories when the application starts
populate_categories_from_csv()

root.mainloop()