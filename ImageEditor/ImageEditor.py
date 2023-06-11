import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog
import openai
import requests
from io import BytesIO
import threading
from PIL import Image, ImageDraw, ImageTk

openai.api_key = "OPENAI_API_KEY"  # Replace with your actual OpenAI API key

# Create the main window
window = tk.Tk()
window.title("Image Viewer")
window.configure(bg="#333333")  # Set a dark background color

# Global variables
image_path = ""
image = None
canvas = None
rectangle = None

# Function to handle button click - Open Image
def open_image():
    global image_path, image, canvas, rectangle

    # Prompt the user to select an image file
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif")])

    # Open and display the selected image
    if file_path:
        image_path = file_path
        image = Image.open(file_path)

        # Center crop the biggest square from the image
        square_size = min(image.size)
        left = (image.width - square_size) // 2
        top = (image.height - square_size) // 2
        right = left + square_size
        bottom = top + square_size
        image = image.crop((left, top, right, bottom))

        window.geometry("")  # Reset the window size
        canvas.config(width=image.width, height=image.height)  # Update canvas size
        photo = ImageTk.PhotoImage(image)
        canvas.delete("all")  # Clear the canvas
        canvas.create_image(0, 0, image=photo, anchor="nw")  # Display the image on the canvas
        canvas.image = photo
        rectangle = None  # Reset the rectangle
        create_mask_button.config(state="normal")  # Enable the Create Mask button

# Function to handle button click - Create Mask
def create_mask():
    global image_path, image, rectangle

    if image and rectangle:
        # Create a mask image with the selected region as transparent
        mask = Image.new("L", image.size, 255)
        draw = ImageDraw.Draw(mask)
        draw.rectangle(rectangle, fill=0)

        # Resize the mask image using Lanczos resampling
        mask = mask.resize((image.width, image.height))

        # Create a copy of the original image with an alpha channel
        edited_image = image.convert("RGBA")

        # Apply the mask to the alpha channel of the edited image
        edited_image.putalpha(mask)

        # Save the edited image as 'mask.png' in the same directory as the original image
        edited_image.save("mask.png")

        # Open the mask image
        mask_image = Image.open("mask.png")

        # Resize the mask image to fit the canvas if necessary
        if mask_image.width > canvas.winfo_width() or mask_image.height > canvas.winfo_height():
            mask_image = mask_image.resize((canvas.winfo_width(), canvas.winfo_height()))

        # Update the canvas with the mask image
        photo = ImageTk.PhotoImage(mask_image)
        canvas.create_image(0, 0, image=photo, anchor="nw")
        canvas.image = photo

        # Show a message box indicating the image has been saved
        messagebox.showinfo("Image Saved", "Edited image has been saved as 'mask.png'")

        # Enable the Edit Image button
        edit_image_button.config(state="normal")

# Function to handle button click - Edit Image
def edit_image():
    prompt = simpledialog.askstring("Edit Image", "Enter a prompt:")
    if prompt:
        # Prepare the data for OpenAI Image API
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
        with open("mask.png", "rb") as mask_file:
            mask_data = mask_file.read()

        def process_api_call():
            # print(image_data.width, image_data.height, mask_data.size)
            # Call the OpenAI API for image editing
            edit_top = openai.Image.create_edit(
                image=image_data,
                mask=mask_data,
                prompt=prompt,
                n=1,
                size=f"{image.width}x{image.height}"  # Pass the original image size to the API
            )
            image_top_url = edit_top['data'][0]['url']

            # Fetch and save the edited image
            image_top = get_image(image_top_url)
            display_image(image_top)
            edited_image_path = image_path.replace(".png", "_edited.png")  # Append "_edited" to the file name
            image_top.save(edited_image_path, format="PNG")

            # Display a message box indicating the image has been saved
            messagebox.showinfo("Image Saved", f"Edited image has been saved as '{edited_image_path}'")

        # Create and start a new thread for API processing
        api_thread = threading.Thread(target=process_api_call)
        api_thread.start()

        # Show a message or visual indicator that the API call is in progress
        messagebox.showinfo("Processing", "The image editing process is in progress. Please wait.")

def get_image(image_url):
    # Send a GET request to the URL and store the response
    response = requests.get(image_url)
    # Check if the request was successful
    if response.status_code == 200:
        # Write the image content to a buffer
        image_buffer = BytesIO(response.content)
        return Image.open(image_buffer)
    else:
        raise ValueError(f'Image could not be retrieved from {image_url}')

def display_image(img):
    # Resize the image to fit the canvas if necessary
    if img.width > canvas.winfo_width() or img.height > canvas.winfo_height():
        img = img.resize((canvas.winfo_width(), canvas.winfo_height()), Image.ANTIALIAS)

    # Update the canvas with the edited image
    photo = ImageTk.PhotoImage(img)
    canvas.create_image(0, 0, image=photo, anchor="nw")
    canvas.image = photo

# Create the top bar
top_bar = tk.Frame(window, bg="#555555")
top_bar.pack(fill="x")

# Create the 'Open Image' button
open_button = tk.Button(top_bar, text="Open Image", command=open_image, bg="#555555", fg="white")
open_button.pack(side="left", padx=10)

# Create the 'Create Mask' button
create_mask_button = tk.Button(top_bar, text="Create Mask", command=create_mask, bg="#555555", fg="white", state="disabled")
create_mask_button.pack(side="left", padx=10)

# Create the 'Edit Image' button
edit_image_button = tk.Button(top_bar, text="Edit Image", command=edit_image, bg="#555555", fg="white", state="disabled")
edit_image_button.pack(side="left", padx=10)

# Create the canvas for displaying the image
canvas = tk.Canvas(window, bg="#333333")
canvas.pack()

# Function to handle mouse button press on the canvas
def start_drawing(event):
    global rectangle
    rectangle = (event.x, event.y, event.x, event.y)

# Function to handle mouse button release on the canvas
def end_drawing(event):
    create_mask_button.config(state="normal")

# Function to handle mouse motion on the canvas
def draw_rectangle(event):
    global rectangle
    canvas.delete("rectangle")
    rectangle = (rectangle[0], rectangle[1], event.x, event.y)
    canvas.create_rectangle(rectangle, outline="red", tags="rectangle")

# Bind the mouse events to the canvas
canvas.bind("<ButtonPress-1>", start_drawing)
canvas.bind("<ButtonRelease-1>", end_drawing)
canvas.bind("<B1-Motion>", draw_rectangle)

# Run the main event loop
window.mainloop()
