import tkinter as tk
from tkinter import filedialog
import fitz  # PyMuPDF
import re
import json

# Function to extract text from a PDF file and save it to a text file
def extract_text_from_pdf(pdf_file, text_file):
    text = ""
    doc = fitz.open(pdf_file)  # Open the PDF file
    for page_num in range(doc.page_count):  # Iterate through pages
        page = doc[page_num]  # Get the current page
        text += page.get_text()  # Append page text to the text variable

    with open(text_file, 'w', encoding='utf-8') as text_output:  # Write text to a file
        text_output.write(text)

# Function to extract name, phone number, and email from text
def extract_information_from_text(text_file):
    with open(text_file, 'r', encoding='utf-8') as text_input:  # Open text file
        text = text_input.read()  # Read the content

    # Regular expressions for name, phone number, and email
    name_pattern = r"([A-Z]+ [A-Z]+)"
    phone_pattern = r"(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})"
    email_pattern = r"([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4})"

    name_match = re.search(name_pattern, text)  # Search for name pattern
    phone_match = re.search(phone_pattern, text)  # Search for phone pattern
    email_match = re.search(email_pattern, text)  # Search for email pattern

    # Extract and return the results
    name = name_match.group() if name_match else "Name not found"
    phone = phone_match.group() if phone_match else "Phone number not found"
    email = email_match.group() if email_match else "Email not found"

    return name, phone, email

# Function to open a file dialog for selecting a PDF file
def browse_file():
    file_path = filedialog.askopenfilename()  # Open file dialog
    if file_path:
        result_label.config(text="Selected File: " + file_path)  # Display the selected file path
        submit_button.config(state=tk.NORMAL)  # Enable the "Submit" button
        submit_button['command'] = lambda: submit_file(file_path)  # Set the "Submit" button's command
    else:
        result_label.config(text="No file selected")  # Display a message if no file is selected
        submit_button.config(state=tk.DISABLED)  # Disable the "Submit" button

# Function to process the selected PDF file, extract information, and save it to a JSON file
def submit_file(pdf_file):
    text_file = 'output.txt'  # Text file to save extracted text
    extract_text_from_pdf(pdf_file, text_file)  # Extract text from the selected PDF
    name, phone, email = extract_information_from_text(text_file)  # Extract information from the text

    # Create a dictionary with the extracted information
    extracted_info = {
        "Name": name,
        "Phone Number": phone,
        "Email": email
    }

    json_string = json.dumps(extracted_info, indent=4)  # Convert the dictionary to a JSON string

    with open("output.json", "w") as json_file:  # Write the JSON string to a JSON file
        json_file.write(json_string)

    result_label.config(text="Name: " + name + "\nPhone Number: " + phone + "\nEmail: " + email)  # Update the result label
    print("Extracted information saved to 'output.json'")  # Print a message

root = tk.Tk()  # Create the main window
root.title("PDF Text Extractor")  # Set the window title

result_label = tk.Label(root, text="No file selected", wraplength=300, fg='blue', width=50, height=15)  # Create a label
result_label.pack(pady=10)  # Place the label in the window

browse_button = tk.Button(root, text="Browse", command=browse_file, width=10, height=2)  # Create the "Browse" button
browse_button.pack(pady=5)  # Place the "Browse" button in the window

submit_button = tk.Button(root, text="Submit", state=tk.DISABLED, width=10, height=2)  # Create the "Submit" button
submit_button.pack(pady=5)  # Place the "Submit" button in the window

root.mainloop()  # Start the main event loop
