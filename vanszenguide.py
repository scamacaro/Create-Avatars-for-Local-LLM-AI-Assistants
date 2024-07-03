# Create a local LLM GUI to run a local LLM model

# Import necessary libraries
# Import the OS library to interact with the operating system
import os
# Import the library to create the GUI using tkinter
import tkinter as tk
# Import the library to create 
from tkinter import scrolledtext
# Import the library to loadour language model and generate responses from it.
# Do not forget to install the library using the command: pip install llama-cpp-python
from llama_cpp import Llama
# Import a random library to generate random numbers
import random
# import a library to get the current date
import datetime

# ******************************** Change the model path here *****************************************
# If you use a different model, change the path to the model here.
model_path ="tinyllama-1.1b-chat-v1.0.Q8_0.gguf"

# Create a variable to store the version of your application
version = 1.0

# Get today's date and stuff the date into a variable
todays_date = datetime.datetime.now().strftime("%Y-%m-%d")

# Create a function to load our model
def load_model():
    # Chech if the models exists by checking the model_path
    if not os.path.isfile(model_path):
        # If the model does not exist, print an error message
        print("Error: Using the model path " + model_path + " I could not find a Model with that filename at that location.")
        # Exit app since no valid model was found
        exit()

    # Otherwise if the model exists and can be found then load the model
    global model
    # Note there are many more parameters you can set when loading the model
    # Make sure to explore them
    model = Llama(
        model_path=model_path,
        verbose=True,
        seed=random.randint(1,2**31),
        n_ctx=0
    )

# Create a function to generate a response from the model
def generate_response(model, input_tokens, prompt_input_text):
    # Display the input text in the area response which is above the input prompt area in the GUI
    text_area_display.insert(tk.INSERT, '\n\nUser: ' + prompt_input_text + '\n')
    # Generate a response from the model
    output_response_text = b""
    count = 0
    output_response_text = b"\n\nVansZenGuideAI: "
    # Put the above variables together
    text_area_display.insert(tk.INSERT, output_response_text)
    # Generate a response  Once this is working okay, you can add parameters to the generate function an change values
    for token in model.generate(input_tokens, top_k=40,top_p=0.95, temp=.72, repeat_penalty=1.1):
        # Extract the response text from the output of the model which is in tokens and convert it to a string
        response_text = model.detokenize([token])
        output_response_text = response_text.decode()
        # Display the response text in the text area response which is above the input prompt area in theGUI
        text_area_display.insert(tk.INSERT, output_response_text)
        root.update_idletasks()
        count += 1
        # Now that we hace a response, we can break out of the for loop we are in
        # We can go beyond 2000 tokens but is not recommended until we add more logic to handle it
        if count > 2000 or (token == model.token_eos()):
            break
        # Let the user know that the response from the model is complete
        # We can clear the input prompt area and allow the user to enter another prompt and let them know the response is complete
        text_area_main_user_input.delete('1.0', tk.END)

# Create a function to send a message to the model and display the response
def send_message():
    # Get the input prompt from the user from the lower text area
    user_prompt_input_text = text_area_main_user_input.get('1.0', 'end-1c')
    # Delete any leading or trailing spaces from user input.
    user_prompt_input_text = user_prompt_input_text.strip()
    # encode the message with uft-8
    byte_message = user_prompt_input_text.encode('utf-8')

    # Here is where we can change the prompt format for the LLM.
    # This is something you will need to experiment with to get the best results.
    # input_tokens = model.tokenize(b"### Human: " + byte_message + b"\n### Assistant: ")
    # use a zen guide personality
    input_tokens = model.tokenize(b"### Human: " + byte_message + b"\n### Zen Guide: Hello there, I am your Zen Guide! I am calm and serene, offering tranquil responses and guiding users to find peace of mind. ")

    # print out the input tokens to the console for debugging, this is for our eyes only/
    # the user will not see this in the GUI. This will be in the console where we run the app.
    print("Input Tokens: ", input_tokens)

    # Call the generate_response functtion to generate a reponse from the model
    generate_response(model, input_tokens, user_prompt_input_text)

# Create our main function that will build our GUI and run it
def main():
    # Load the model when our app starts
    load_model()

    # Create the main window of our GUI
    global root
    root = tk.Tk()
    # Set the title of the GUI - change the title to the name of your application to make it unique and yours!
    root.title("VansZenGuideAI -v" + str(version) + " - " + todays_date)
    # Create a frame to add a scrollbar to the text area
    frame_display = tk.Frame(root)
    scrollbar_frame_display = tk.Scrollbar(frame_display)
    # Create the text area where the model responses will be displayed and add the user prompt in between each reponse so
    # it flows like a conversation history.
    global text_area_display
    text_area_display = scrolledtext.ScrolledText(frame_display, width=150, height=35, yscrollcommand=scrollbar_frame_display.set)
    # Create colors for our GUI - Change the colors to match your application's color scheme
    my_light_purple = "#a616ab"
    my_light_grey = "#bcb5bd"
    #Set the background color and the foreground color of the text area
    text_area_display.config(background=my_light_grey, foreground=my_light_purple, font=("Courier", 12))
    # Set the scrollbar properties
    scrollbar_frame_display.config(command=text_area_display.yview)
    text_area_display.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar_frame_display.pack(side=tk.RIGHT, fill=tk.Y)
    # fill the frame display of the root window 
    frame_display.pack()

    frame_Controls = tk.Frame(root)
    # Create a label to let our users know what LLM model they are using, and also the path to that model.
    model_path_label = tk.Label(frame_Controls, text="Model Path: " + model_path, font=("Courier", 12))
    # Place the label that we created in the frame controls
    model_path_label.pack(side=tk.LEFT, padx=10)
    frame_Controls.pack(fill=tk.BOTH, padx=5,pady=5)

    # Create a frame for the user to input text as a prompt for the model
    # This will be below the output text area.
    frame_user_input = tk.Frame(root)
    frame_user_input.pack(fill=tk.BOTH)

    # Create a text area where the user can input text as a prompt for the model
    frame_main_user_input = tk.Frame(root)
    scrollbar_main_user_input = tk.Scrollbar(frame_main_user_input)

    global text_area_main_user_input
    text_area_main_user_input = scrolledtext.ScrolledText(frame_main_user_input, width=128, height=5, yscrollcommand=scrollbar_main_user_input.set)
    # Set the background color and the foreground color of the text area, and the font.
    # Change the colors to match your application's color scheme
    text_area_main_user_input.config(background=my_light_grey, foreground=my_light_purple, font=("Courier", 12))
    scrollbar_main_user_input.config(command=text_area_main_user_input.yview)
    # Fill out root window with the frame 
    text_area_main_user_input.pack(side=tk.LEFT, fill=tk.BOTH)
    scrollbar_main_user_input.pack(side=tk.RIGHT, fill=tk.Y)
    frame_main_user_input.pack()

    # Create a button to send the user input to the model
    # Remember the enter key will NOT sent the user input to the model, you must click the button
    # This is a design choice to prevent the user from accidentally sending the inout to the nodel
    # before they are ready. And so they can send multiple lines of input to the model at once.
    send_button = tk.Button(root, text="Send", command=send_message, font=("Courier", 12))
    # Fill out the root window with the button
    send_button.pack()
    # Run the main loop of the GUI
    # This is very important,this is what makes the GUI run, this often gets forgotten for some reason!
    root.mainloop()

# Create the starting point of our app!
if __name__ == "__main__":
    main()
