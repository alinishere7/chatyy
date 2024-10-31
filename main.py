from groq import Groq  # type: ignore
import subprocess
import tkinter as tk
from tkinter import scrolledtext
from tkinter import PhotoImage

# Initialize the Groq client with the API key
api_key = "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"
client = Groq(api_key=api_key)

# Initialize the conversation history (message history)
messages = [
    {"role": "system", "content": "Sən köməkçi chatbot rolundasan."}
]

# Theme colors
dark_theme = {
    "bg": "#2b2b2b",
    "text_bg": "#1e1e1e",
    "input_bg": "#3c3836",
    "fg": "#dcdcdc",
    "text_fg": "white",  # Text color for dark mode
    "user_text": "white",  # White text for user messages in dark mode
    "chatty_text": "white",  # White text for Chatty's messages in dark mode
    "button_bg": "#458588",
    "button_active": "#83a598",
    "icon_bg": "black"
}

light_theme = {
    "bg": "#f5f5f5",
    "text_bg": "#ffffff",
    "input_bg": "#e8e8e8",
    "fg": "#333333",
    "text_fg": "black",  # Text color for light mode
    "user_text": "black",  # Black text for user messages in light mode
    "chatty_text": "black",  # Black text for Chatty's messages in light mode
    "button_bg": "#0a9396",
    "button_active": "#94d2bd",
    "icon_bg": "white"
}

# Start with dark theme
current_theme = dark_theme

# Function to apply the current theme
def apply_theme():
    root.configure(bg=current_theme["bg"])
    # Set background and text color for response area
    response_area.configure(bg=current_theme["text_bg"], fg=current_theme["text_fg"])
    # Set background and text color for input box
    input_box.configure(bg=current_theme["input_bg"], fg=current_theme["text_fg"], insertbackground=current_theme["text_fg"])
    # Set background and text color for submit button
    submit_button.configure(bg=current_theme["button_bg"], fg=current_theme["text_fg"], activebackground=current_theme["button_active"])
    # Set icon background color
    icon_bg_label.configure(bg=current_theme["icon_bg"])

    # Update tagged text colors in response area
    response_area.tag_config("user", foreground=current_theme["user_text"])
    response_area.tag_config("chatty", foreground=current_theme["chatty_text"])

# Toggle between light and dark themes
def toggle_theme():
    global current_theme, current_icon
    if current_theme == dark_theme:
        current_theme = light_theme
        current_icon = light_icon
    else:
        current_theme = dark_theme
        current_icon = dark_icon
    toggle_button.config(image=current_icon)  # Update button icon
    apply_theme()

# Function to get a response from the Groq API
def get_gpt_response(command):
    messages.append({"role": "user", "content": command})
    chat_completion = client.chat.completions.create(
        messages=messages,
        model="llama3-8b-8192"
    )
    response_content = chat_completion.choices[0].message.content
    messages.append({"role": "assistant", "content": response_content})
    return response_content

# Function to handle system-level tasks (open apps, perform actions)
def handle_system_commands(command):
    if "open notepad" in command:
        subprocess.run(["notepad.exe"])
        return "Opening Notepad."
    elif "open calculator" in command:
        subprocess.run(["calc.exe"])
        return "Opening Calculator."
    elif "shutdown" in command:
        subprocess.run(["shutdown", "/s", "/t", "1"])
        return "Shutting down the system."
    elif "restart" in command:
        subprocess.run(["shutdown", "/r", "/t", "1"])
        return "Restarting the system."
    else:
        return None

# Function to process the user's command
def process_command(event=None):
    if event and event.state == 1 and event.keysym == "Return":
        input_box.insert(tk.END, "\n")  # Insert newline
        return

    command = input_box.get("1.0", tk.END).strip()  # Get all text from input box
    input_box.delete("1.0", tk.END)  # Clear the input box

    # First, check if it's a system command
    system_response = handle_system_commands(command)
    if system_response:
        response_area.insert(tk.END, f"Chatty: {system_response}\n", "chatty")
    else:
        # Otherwise, treat it as a general query and get a response from Groq API
        response = get_gpt_response(command)
        response_area.insert(tk.END, f"You: {command}\n", "user")
        response_area.insert(tk.END, f"Chatty: {response}\n", "chatty")
    response_area.see(tk.END)

# Initialize the Tkinter window
root = tk.Tk()
root.title("Chatty AI Assistant")
root.geometry("700x500")  # Set initial size
root.state("zoomed")  # Start in maximized mode
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
root.rowconfigure(1, weight=0)
root.rowconfigure(2, weight=0)

# Load icons after root initialization and resize
light_icon = PhotoImage(file="assets/sun.png").subsample(30, 30)  # Icon for light mode (half size)
dark_icon = PhotoImage(file="assets/moon.png").subsample(30, 30)  # Icon for dark mode (half size)
current_icon = dark_icon  # Start with dark mode icon

# Create a display area for Chatty's responses
response_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, font=("Arial", 12))
response_area.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
response_area.tag_config("user", foreground=current_theme["user_text"])  # Greenish color for user text
response_area.tag_config("chatty", foreground=current_theme["chatty_text"])  # Pinkish color for Chatty's responses
response_area.insert(tk.END, "Chatty: Hello! I am your Chatty AI assistant. How can I assist you today?\n", "chatty")

# Create an input box for user commands
input_box = tk.Text(root, height=3, font=("Arial", 12))
input_box.grid(row=1, column=0, sticky="ew", padx=10, pady=(0, 10))
input_box.bind("<Return>", process_command)  # Bind Enter key to process_command
input_box.bind("<Shift-Return>", lambda event: input_box.insert(tk.END, "\n"))  # Bind Shift+Enter to insert newline

# Icon background label for white/black toggle background
icon_bg_label = tk.Label(root, bg=current_theme["icon_bg"])
icon_bg_label.grid(row=2, column=0, pady=(0, 10), sticky="w", padx=10)

# Create a theme toggle button with an icon inside the label
toggle_button = tk.Button(icon_bg_label, image=current_icon, command=toggle_theme, font=("Arial", 10), bd=0)
toggle_button.pack()

# Create a submit button
submit_button = tk.Button(root, text="Send", command=process_command, font=("Arial", 12))
submit_button.grid(row=2, column=0, pady=(0, 10), sticky="e", padx=10)

# Apply the initial theme
apply_theme()

# Start the Tkinter main loop
root.mainloop()
