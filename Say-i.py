import os
import tkinter as tk
from PIL import ImageTk, Image
import requests
from io import BytesIO
import openai
import speech_recognition as sr
import pyttsx3

# Set up the OpenAI API key
openai.api_key = "Your OpenAI API here"

# Set up the speech recognizer
r = sr.Recognizer()

# Initialize Pyttsx3
engine = pyttsx3.init()

# Define the function to speak text
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Define the function to show the image
def show_image(image_url):
    response = requests.get(image_url)
    img_data = response.content
    img = Image.open(BytesIO(img_data))
    img = img.resize((500, 500))
    photo = ImageTk.PhotoImage(img)

    # Create a new window to display the image
    window = tk.Toplevel()
    window.title("Image")

    # Create a canvas to display the image
    canvas = tk.Canvas(window, width=img.width, height=img.height)
    canvas.pack()

    # Create a label with the image and add it to the canvas
    label = tk.Label(canvas, image=photo)
    label.photo = photo
    label.pack()

    window.mainloop()


def get_image_from_user():
    # Use the microphone as the source for audio
    with sr.Microphone() as source:
        speak("What would you like to see?")
        audio = r.listen(source)

    # Transcribe the audio using Google's speech recognition service
    try:
        text = r.recognize_google(audio)
        # Generate the edited image using OpenAI API
        response_image = openai.Image.create(
            prompt=text,
            n=1,
            size="1024x1024"
        )
        image_url = response_image.data[0].url
        show_image(image_url)

    except sr.UnknownValueError:
        speak("Sorry, I could not understand what you said.")

    except sr.RequestError as e:
        speak("Sorry, my speech service is currently down. Please try again later.")

    except Exception as e:
        speak(f"Sorry, an error occurred: {e}")


# Set up the GUI
root = tk.Tk()
root.title("Speech Recognition")

# Set the GUI to fill the entire window
root.pack_propagate(False)
root.geometry("500x500")
root.configure(bg='#E4FDE1')

# Create a new frame for the buttons
buttons_frame = tk.Frame(root, bg='#E4FDE1')
buttons_frame.pack(pady=50, fill=tk.BOTH, expand=True)

# Create the "Go " button widget and place it in the frame
start_button = tk.Button(buttons_frame, text="Go", command=get_image_from_user, bg='#F25F5C', fg='#E4FDE1', font=('Helvetica', 14), padx=20, pady=10, borderwidth=0)
start_button.pack(side=tk.LEFT, padx=10)

# Create a new frame for the credits and add it to the bottom of the window
credits_frame = tk.Frame(root, bg='#E4FDE1')
credits_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=10)

credits_label = tk.Label(credits_frame, text="Powered by OpenAI GPT-3 and Google Speech Recognition", bg='#E4FDE1', fg='#5B5B5B', font=('Helvetica', 10), pady=5)
credits_label.pack()

# Start the main event loop
root.mainloop()
