import tkinter as tk
from tkinter import ttk, filedialog
import pyperclip
import re

def read_txt_file(file_name):
    try:
        with open(file_name, 'r') as file:
            lines = file.readlines()
            print("File Opened")
    except Exception as e:
        print(f"Error opening file: {e}")
        return []

    data = []
    # Pattern to capture points in the old format (PPxx [xx:Point])
    new_pattern = re.compile(r'W\t(-?\d+\.\d+)\t(-?\d+\.\d+)\t.*\t.*\t(PP\d+ \[\d+:Point\])\t.*')

    for line in lines:
        print(line)
        match = new_pattern.match(line)
        if match:
            latitude = match.group(1)
            longitude = match.group(2)
            name = match.group(3)
            data.append({'latitude': latitude, 'longitude': longitude, 'name': name})
            print(f'Found in new format: Latitude: {latitude}, Longitude: {longitude}, Name: {name}')

    return data

def format_coordinate(coordinate):
    integer_part, decimal_part = coordinate.split('.')
    
    formatted_integer_part = ""
    for i in range(len(integer_part)):
        formatted_integer_part += integer_part[i]
        if (len(integer_part) - i - 1) % 3 == 0 and i != len(integer_part) - 1:
            formatted_integer_part += '.'

    formatted_decimal_part = ""
    for i in range(len(decimal_part)):
        formatted_decimal_part += decimal_part[i]
        if (i + 1) % 3 == 0 and i != len(decimal_part) - 1:
            formatted_decimal_part += '.'

    return f'{formatted_integer_part}.{formatted_decimal_part}'

def display_info(index):
    result = results[index]
    formatted_latitude = format_coordinate(result["latitude"])
    formatted_longitude = format_coordinate(result["longitude"])
    info_text.set(f'Point: {result["name"]}\nLatitude: {formatted_latitude}\nLongitude: {formatted_longitude}')
    pyperclip.copy(f'{formatted_latitude}\n{formatted_longitude}')

def choose_file():
    global results, current_index
    file_name = filedialog.askopenfilename(filetypes=[("TXT Files", "*.txt")])
    if file_name:
        results = read_txt_file(file_name)
        if results:
            point_names = [result['name'] for result in results]
            points_combo['values'] = point_names
            points_combo.current(0)
            current_index = 0
            display_info(0)

def select_point(event):
    global current_index
    current_index = points_combo.current()
    display_info(current_index)

root = tk.Tk()
root.title("Point")
root.resizable(False, False)

style = ttk.Style()
style.theme_use('default')
style.configure('.', foreground='black', background='white')
style.configure('TCombobox', foreground='black', background='white', padding=1)

current_index = 0
results = []

frame = ttk.Frame(root, padding="10")
frame.grid(column=0, row=0, sticky=(tk.W, tk.E, tk.N, tk.S))

choose_file_button = ttk.Button(frame, text="Choose File", command=choose_file)
choose_file_button.grid(column=0, row=0, padx=10, pady=10, columnspan=3)

point_names = []

points_combo = ttk.Combobox(frame, values=point_names)
points_combo.grid(column=0, row=1, padx=10, pady=10, columnspan=3)

points_combo.bind("<<ComboboxSelected>>", select_point)

def back():
    global current_index
    current_index = max(0, current_index - 1)
    display_info(current_index)
    points_combo.current(current_index)

back_button = ttk.Button(frame, text="Back", command=back)
back_button.grid(column=0, row=2, padx=10, pady=10)

def forward():
    global current_index
    current_index = min(len(results) - 1, current_index + 1)
    display_info(current_index)
    points_combo.current(current_index)

forward_button = ttk.Button(frame, text="Forward", command=forward)
forward_button.grid(column=1, row=2, padx=10, pady=10)

info_text = tk.StringVar()
info_label = ttk.Label(frame, textvariable=info_text)
info_label.grid(column=0, row=3, columnspan=3, padx=10, pady=10)

root.mainloop()
