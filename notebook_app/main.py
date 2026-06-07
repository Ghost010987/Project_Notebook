"""This is going to be the single point of entry that boots
    the entire application. Nothing else should start the app."""

import customtkinter as ctk
from ui.app_window import AppWindow

# This main.py should do 4 things:
# Set the appearence mode
# Set the color theme using
# Instantiate AppWindow and store it as app
# Call app.mainloop() to start the UI event loop

def main():
    # Set appearence and theme
    ctk.set_appearance_mode("dark")     #"Dark", "Light", "system"
    ctk.set_default_color_theme("blue") #"blue", "green", "dark-blue"

    # Create and run the app
    app = AppWindow()
    app.mainloop()

if __name__ == "__main__":
    main()
