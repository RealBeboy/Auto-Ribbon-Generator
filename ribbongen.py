import os
import tkinter as tk
from tkinter import messagebox, filedialog
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont

def create_ribbon_image(name, template_path, font_path, ribbon_width, ribbon_height):
    # Load the ribbon template
    template = Image.open(template_path).convert("RGBA")
    template = template.resize((ribbon_width, ribbon_height), Image.Resampling.LANCZOS)
    draw = ImageDraw.Draw(template)
    
    # Start with a large font size
    font_size = 100  
    font = ImageFont.truetype(font_path, size=font_size)
    
    # Dynamically adjust font size to fit within the ribbon
    while True:
        # Calculate text size
        text_bbox = draw.textbbox((0, 0), name, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]
        
        # Check if the text fits within the ribbon
        if text_width <= ribbon_width * 0.5 and text_height <= ribbon_height * 1:
            break
        font_size -= 2  # Reduce font size and check again
        font = ImageFont.truetype(font_path, size=font_size)
        
        # If the font size gets too small, truncate the text
        if font_size < 20:
            name = name[:ribbon_width // 10] + "..."  # Truncate and add ellipsis
            break
    
    # Calculate the position of the text (center it)
    text_bbox = draw.textbbox((0, 0), name, font=font)
    text_width = text_bbox[2] - text_bbox[0]
    text_height = text_bbox[3] - text_bbox[1]
    
    x = (ribbon_width - text_width) // 2
    offset = 10  # Fine-tune vertical alignment
    y = (ribbon_height - text_height) // 3.5 - offset
    
    # Draw the name on the ribbon
    draw.text((x, y), name, font=font, fill="black")
    
    return template


def generate_pdf(names, template_path, font_path, output_pdf_path):
    try:
        # A4 size in pixels at 300 DPI
        a4_width, a4_height = 2480, 3508
        ribbons_per_row = 2  # 2 columns
        rows_per_page = 10   # 10 rows
        ribbon_width = a4_width // ribbons_per_row
        ribbon_height = a4_height // rows_per_page
        
        # Create an A4 canvas
        a4_canvas = Image.new("RGBA", (a4_width, a4_height), "white")
        
        # Generate and place each ribbon on the canvas
        for i, name in enumerate(names):
            if i >= ribbons_per_row * rows_per_page:
                break  # Stop if exceeding 20 ribbons
            
            # Create the ribbon image
            ribbon = create_ribbon_image(name, template_path, font_path, ribbon_width, ribbon_height)
            
            # Calculate position on the A4 canvas
            col = i % ribbons_per_row
            row = i // ribbons_per_row
            x = col * ribbon_width
            y = row * ribbon_height
            
            # Paste the ribbon onto the canvas
            a4_canvas.paste(ribbon, (x, y))
        
        # Convert the A4 canvas to RGB to remove transparency
        rgb_canvas = Image.new("RGB", a4_canvas.size, "white")  # Create a white background
        rgb_canvas.paste(a4_canvas, (0, 0), mask=a4_canvas)  # Composite with transparency mask
        
        # Save the A4 sheet as PDF
        rgb_canvas.save(output_pdf_path, "PDF")
        
        return True  # Successful completion
    except Exception as e:
        print(f"Error: {e}")
        return False  # Error occurred

# GUI Setup
def start_generation():
    # Get names from the input field
    names_input = names_entry.get("1.0", "end-1c")
    
    # Convert all names to uppercase
    names = names_input.upper().splitlines()
    
    if not names:
        messagebox.showerror("Error", "Please enter some names.")
        return
    
    # Automatically detect current directory for paths
    current_dir = os.path.dirname(os.path.abspath(__file__))
    programfiles_dir = os.path.join(current_dir, "programfiles")  # Folder where template and font are located
    
    # Ensure the folder exists
    if not os.path.exists(programfiles_dir):
        messagebox.showerror("Error", f"Programfiles folder not found at {programfiles_dir}.")
        return
    
    template_path = os.path.join(programfiles_dir, "ribbon_template.png")
    font_path = os.path.join(programfiles_dir, "arial.ttf")  # Make sure the font is in the 'programfiles' folder
    
    # Prompt the user to select the save location and filename
    output_pdf_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])
    
    if not output_pdf_path:
        messagebox.showerror("Error", "You must choose a file location to save the PDF.")
        return
    
    # Log the file path
    log_text.insert(tk.END, f"Generating PDF:\nPDF: {output_pdf_path}\n\n")
    log_text.yview(tk.END)
    
    # Start the generation process
    success = generate_pdf(names, template_path, font_path, output_pdf_path)
    
    if success:
        log_text.insert(tk.END, f"Successfully generated: {output_pdf_path}\n")
    else:
        log_text.insert(tk.END, f"Error: Failed to generate PDF.\n")
    
    log_text.yview(tk.END)

# Create the main window
root = tk.Tk()
root.title("Ribbon Generator")
root.geometry("600x800")
root.config(padx=20, pady=20)

# Frame for the input fields
input_frame = tk.Frame(root)
input_frame.pack(fill="both", expand=True)

# Labels and Entries for inputs
names_label = tk.Label(input_frame, text="Enter Names (one per line):", font=("Arial", 12, "bold"))
names_label.pack(pady=10)
names_entry = tk.Text(input_frame, height=10, width=50, font=("Arial", 12))
names_entry.pack(pady=10)

# Frame for the log area
log_frame = tk.Frame(root)
log_frame.pack(fill="both", expand=True)

# Log text area
log_text = tk.Text(log_frame, height=10, width=50, font=("Arial", 10), wrap="word")
log_text.pack(pady=10)

# Generate Button
generate_button = tk.Button(root, text="Generate PDF", command=start_generation, font=("Arial", 14), bg="#4CAF50", fg="white", width=20, height=2)
generate_button.pack(pady=10)

# Run the GUI
root.mainloop()
