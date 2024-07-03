# Import necessary libraries
import os  # Module to interact with the operating system
import tkinter as tk  # GUI framework for Python
from tkinter import scrolledtext, filedialog  # ScrolledText widget and file dialog box
from PIL import Image, ImageTk  # Image processing with PIL (Pillow)
from llama_cpp import Llama  # Import the Llama class for handling the model
import random  # For random number generation
import datetime  # For handling dates and times

# Set the path to the AI model
model_path = "dolphin-2.6-mistral-7b-dpo.Q5_K_M.gguf"  # Model file path
version = 1.0  # Version of your application
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")  # Current date in YYYY-MM-DD format

# Function to load the AI model
def load_model():
    # Check if the model file exists at the specified path
    if not os.path.isfile(model_path):
        print("Error: Could not find the model at the specified path.")  # Error message if not found
        exit()  # Exit the program if the model is not found
    
    # Initialize the model with a random seed
    global model  # Declare the model as a global variable
    model = Llama(
        model_path=model_path,
        seed=random.randint(1, 2**31),  # Random seed
    )

# Function to generate a response from the model based on user input
def generate_response(model, input_tokens, prompt_input_text):
    # Display the user's message in the chat area
    text_area_display.insert(tk.END, f'\n\nUser: {prompt_input_text}\n')
    text_area_display.insert(tk.END, "\nAI Engineer:")  # Indicate the start of AI's response

    # Loop to generate the AI response
    for token in model.generate(input_tokens, top_k=40, top_p=0.95, temp=0.72, repeat_penalty=1.1):
        response_text = model.detokenize([token]).decode()  # Convert token to text
        text_area_display.insert(tk.END, response_text)  # Display the generated text
        root.update_idletasks()  # Refresh the GUI

        # Break if the end-of-sequence token is detected
        if token == model.token_eos():
            break

    # Clear the user input field after generating a response
    text_area_main_user_input.delete("1.0", tk.END)

# Function to send a message to the model and display the response
def send_message():
    # Get the user's input from the text area
    user_prompt_input_text = text_area_main_user_input.get("1.0", "end-1c").strip()
    byte_message = user_prompt_input_text.encode("utf-8")  # Encode input as bytes

    # Tokenize the user message for the model
    input_tokens = model.tokenize(b"### Human: " + byte_message + b"\n### AI Engineer: ")
    generate_response(model, input_tokens, user_prompt_input_text)  # Generate the AI response

# Function to save the current conversation to a file
def save_conversation():
    # Generate a unique filename using a timestamp
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    filename = f"conversation_{timestamp}.txt"
    
    # Get the full conversation text from the display area
    conversation = text_area_display.get("1.0", tk.END)

    # Try to save the conversation to a file
    try:
        with open(filename, "w") as file:  # Open the file for writing
            file.write(conversation)  # Write the conversation to the file
        print(f"Conversation saved to {filename}")  # Confirmation message
    except Exception as e:  # Handle any errors during file operations
        print(f"Error saving conversation: {e}")  # Print error message

# Function to clear the current conversation from the display area
def clear_conversation():
    text_area_display.delete("1.0", tk.END)  # Clear the entire text area

# Function to start a new conversation by clearing the current one
def new_conversation():
    clear_conversation()  # Clear the existing conversation
    text_area_display.insert(tk.END, "New conversation started.\n")  # Indicate a new conversation has started

# Function to load a saved conversation from a file
def load_conversation():
    # Open a file dialog to select the conversation file
    filename = filedialog.askopenfilename(
        title="Open Conversation",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    
    # If a filename was selected, load the content into the display area
    if filename:
        try:
            with open(filename, "r") as file:  # Open the file for reading
                conversation = file.read()  # Read the content
            text_area_display.delete("1.0", tk.END)  # Clear the current content
            text_area_display.insert(tk.END, conversation)  # Insert the loaded content
            print(f"Loaded conversation from {filename}")  # Confirmation message
        except Exception as e:  # Handle file-related errors
            print(f"Error loading conversation: {e}")  # Print error message

# Main function to build and run the GUI
def main():
    load_model()  # Load the AI model

    global root  # Global variable for the main tkinter window
    root = tk.Tk()  # Initialize the main tkinter window
    root.title(f"AI Engineer - v{version} - {todays_date}")  # Set the title with version and date

    # Display the avatar image if available
    image_path = "avatar.png"  # Path to the avatar image
    if os.path.exists(image_path):  # Check if the image file exists
        img = Image.open(image_path)  # Open the image file
        img = img.resize((158, 186), Image.LANCZOS)  # Resize the image
        photo = ImageTk.PhotoImage(img)  # Convert to tkinter-compatible image
        label = tk.Label(root, image=photo)  # Create a label with the image
        label.image = photo  # Keep a reference to prevent garbage collection
        label.pack(side=tk.TOP, fill=tk.BOTH, expand=True)  # Pack into the tkinter window
    else:
        print(f"Error: Avatar image not found at {image_path}.")  # Error message if not found
        exit()  # Exit if the image is not found

    # Display area for model responses with a scrollbar
    frame_display = tk.Frame(root)  # Frame to contain the text area
    scrollbar_frame_display = tk.Scrollbar(frame_display)  # Scrollbar for scrolling
    global text_area_display  # Global variable for the text area
    text_area_display = scrolledtext.ScrolledText(frame_display, width=128, height=15, yscrollcommand=scrollbar_frame_display.set)  # Create a scrollable text area
    text_area_display.config(background="#202020", foreground="#a72ab8", font=("Courier", 12))  # Set the style of the text area
    scrollbar_frame_display.config(command=text_area_display.yview)  # Connect the scrollbar to the text area
    text_area_display.pack(side=tk.LEFT, fill=tk.BOTH)  # Pack the text area into the frame
    scrollbar_frame_display.pack(side=tk.RIGHT, fill=tk.Y)  # Pack the scrollbar into the frame
    frame_display.pack()  # Pack the frame into the main window

    # Frame to display the model path and other controls
    frame_controls = tk.Frame(root)  # Create a frame for controls
    model_path_label = tk.Label(frame_controls, text=f"Model Path: {model_path}", font=("Courier", 12))  # Label to show the model path
    model_path_label.pack(side=tk.LEFT, padx=10)  # Pack the label into the frame
    frame_controls.pack(fill=tk.BOTH, padx=5, pady=5)  # Pack the frame with padding

    # Frame for user input with a scrollbar
    frame_main_user_input = tk.Frame(root)  # Create a frame for user input
    scrollbar_main_user_input = tk.Scrollbar(frame_main_user_input)  # Scrollbar for the input area
    global text_area_main_user_input  # Global variable for the user input text area
    text_area_main_user_input = scrolledtext.ScrolledText(frame_main_user_input, width=128, height=5, yscrollcommand=scrollbar_main_user_input.set)  # Scrollable user input
    text_area_main_user_input.config(background="#202020", foreground="#a72ab8", font=("Courier", 12))  # Set the style for user input
    scrollbar_main_user_input.config(command=text_area_main_user_input.yview)  # Connect the scrollbar to the input area
    text_area_main_user_input.pack(side=tk.LEFT, fill=tk.BOTH)  # Pack the input area into the frame
    scrollbar_main_user_input.pack(side=tk.RIGHT, fill=tk.Y)  # Pack the scrollbar into the frame
    frame_main_user_input.pack()  # Pack the frame into the main window

    # Button to send a message to the AI
    send_button = tk.Button(root, text="Send", command=send_message, font=("Courier", 12))  # Create the Send button
    send_button.pack(pady=10)  # Pack the Send button into the main window

    # Menu bar for additional actions
    menu_bar = tk.Menu(root)  # Create the main menu bar
    root.config(menu=menu_bar)  # Set the menu bar for the main window

    # Create the File menu
    file_menu = tk.Menu(menu_bar, tearoff=0)  # Create the File menu
    file_menu.add_command(label="Save Conversation", command=save_conversation)  # Option to save the current conversation
    file_menu.add_command(label="Load Conversation", command=load_conversation)  # Option to load a saved conversation
    file_menu.add_command(label="Clear Conversation", command=clear_conversation)  # Option to clear the current conversation
    file_menu.add_command(label="New Conversation", command=new_conversation)  # Start a new conversation
    file_menu.add_separator()  # Separator in the menu
    file_menu.add_command(label="Exit", command=root.quit)  # Option to exit the application
    menu_bar.add_cascade(label="File", menu=file_menu)  # Add the File menu to the menu bar

    # Section for drawing pixel art
    def draw_pixel(event):
        # Get the coordinates where the mouse is moved
        x, y = event.x, event.y
        pixel_size = 10  # Set the size of each pixel
        x1, y1 = (x - pixel_size), (y - pixel_size)  # Coordinates for the top-left corner
        x2, y2 = (x + pixel_size), (y + pixel_size)  # Coordinates for the bottom-right corner
        canvas.create_oval(x1, y1, x2, y2, fill="black")  # Draw a black oval (pixel)

    # Create a frame for the pixel art pad
    pixel_pad_frame = tk.Frame(root)  # Frame to contain the canvas
    pixel_pad_frame.pack(fill=tk.BOTH, expand=True)  # Pack the frame into the main window

    # Create a canvas for drawing pixel art
    canvas = tk.Canvas(pixel_pad_frame, bg="white", width=400, height=400)  # White background canvas
    canvas.pack(fill=tk.BOTH, expand=True)  # Pack the canvas into the frame

    # Bind the mouse motion event to the draw_pixel function
    canvas.bind("<B1-Motion>", draw_pixel)  # When the mouse is moved with button 1 pressed, draw pixels

    # Start the main event loop
    root.mainloop()  # Start the tkinter main loop to run the GUI

# Start the application
if __name__ == "__main__":
    main()  # Call the main function to start the GUI