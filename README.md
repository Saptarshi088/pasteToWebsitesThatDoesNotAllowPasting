# Human-like Text Typer - Installation Instructions

## Prerequisites

Before running the application, you need to install:

1. **Python** (3.7 or newer): [Download Python](https://www.python.org/downloads/)
2. **Required Python packages**:
   - tkinter (usually comes with Python)
   - pyautogui

## Installation Steps

1. **Install PyAutoGUI**:
   Open Command Prompt or PowerShell and run:
   ```
   pip install pyautogui
   ```

2. **Save the code** to a file named `text_typer.py`

3. **Run the application**:
   ```
   python text_typer.py
   ```

## How to Use

1. **Paste your text** into the top text area
2. **Adjust typing speed** if needed (default is 200 WPM)
3. **Click "Start Typing"** button
4. **Within 5 seconds**, click where you want the text to appear (for example, a browser search bar, text editor, or form field)
5. The application will automatically type out your text at the specified speed

## Features

- **Adjustable typing speed** (200-1500 WPM)
- **Human-like variance** adds slight randomness to typing rhythm
- **Longer pauses** after punctuation for more natural typing 
- **Progress tracking** shows completion percentage
- **Cancel button** to stop typing at any time

## Troubleshooting

- **Text typing doesn't work**: Make sure you clicked in the destination field during the 5-second countdown
- **Application crashes**: Verify that PyAutoGUI is properly installed
- **Typing is too fast/slow**: Adjust the WPM slider to find a comfortable speed

## Important Notes

- This application uses PyAutoGUI to simulate keyboard input, so it works with any application that accepts text input
- The application needs to be running and visible while typing occurs
- Some secure applications may block simulated keyboard input
