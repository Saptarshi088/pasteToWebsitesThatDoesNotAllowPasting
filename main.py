import tkinter as tk
from tkinter import scrolledtext
import pyautogui
import threading
import time
import random

class TextTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Human-like Text Typer")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Set app icon and styling
        self.root.configure(bg="#f0f0f0")
        
        # Create a frame for better layout
        main_frame = tk.Frame(root, bg="#f0f0f0")
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Input text area (where you paste your text)
        input_label = tk.Label(main_frame, text="Paste your text here:", bg="#f0f0f0", font=("Arial", 10, "bold"))
        input_label.pack(anchor="w", pady=(0, 5))
        
        self.input_text = scrolledtext.ScrolledText(main_frame, width=60, height=10, wrap=tk.WORD, font=("Arial", 10))
        self.input_text.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Control frame for typing speed
        control_frame = tk.Frame(main_frame, bg="#f0f0f0")
        control_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Words per minute scale
        speed_label = tk.Label(control_frame, text="Typing speed (WPM):", bg="#f0f0f0")
        speed_label.pack(side=tk.LEFT, padx=(0, 10))
        
        self.wpm_var = tk.IntVar(value=1000)  # Default 1000 WPM
        self.wpm_scale = tk.Scale(
            control_frame, 
            from_=200, 
            to=1500, 
            resolution=50, 
            orient=tk.HORIZONTAL, 
            variable=self.wpm_var,
            length=150,
            bg="#f0f0f0"
        )
        self.wpm_scale.pack(side=tk.LEFT)
        
        # Human variance checkbox (adds slight randomness to typing speed)
        self.human_variance = tk.BooleanVar(value=True)
        self.variance_check = tk.Checkbutton(
            control_frame, 
            text="Add human-like variance", 
            variable=self.human_variance,
            bg="#f0f0f0"
        )
        self.variance_check.pack(side=tk.LEFT, padx=(20, 0))
        
        # Button frame for actions
        button_frame = tk.Frame(main_frame, bg="#f0f0f0")
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Function buttons
        self.start_button = tk.Button(
            button_frame, 
            text="Start Typing (5s delay)", 
            command=self.prepare_typing,
            bg="#4CAF50", 
            fg="white", 
            font=("Arial", 10, "bold"),
            padx=10, 
            pady=5
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.cancel_button = tk.Button(
            button_frame, 
            text="Cancel", 
            command=self.cancel_typing,
            bg="#f44336", 
            fg="white", 
            font=("Arial", 10, "bold"),
            padx=10, 
            pady=5,
            state=tk.DISABLED
        )
        self.cancel_button.pack(side=tk.LEFT)
        
        # Status display
        self.status_var = tk.StringVar(value="Ready")
        self.status_label = tk.Label(
            main_frame, 
            textvariable=self.status_var, 
            bg="#f0f0f0", 
            fg="#333333", 
            font=("Arial", 10)
        )
        self.status_label.pack(anchor="w", pady=(10, 0))
        
        # Timer display for countdown
        self.timer_var = tk.StringVar()
        self.timer_label = tk.Label(
            main_frame, 
            textvariable=self.timer_var, 
            bg="#f0f0f0", 
            fg="#FF5722", 
            font=("Arial", 12, "bold")
        )
        self.timer_label.pack(anchor="w", pady=(5, 0))
        
        # Help text
        help_text = "Instructions:\n1. Paste your text above\n2. Click 'Start Typing'\n3. Click where you want the text to be typed (within 5 seconds)\n4. Wait for typing to complete"
        help_label = tk.Label(
            main_frame, 
            text=help_text, 
            bg="#e0e0e0", 
            fg="#555555", 
            font=("Arial", 9),
            justify=tk.LEFT,
            padx=10,
            pady=10
        )
        help_label.pack(fill=tk.X, pady=(10, 0))
        
        # Variables for typing control
        self.typing_active = False
        self.typing_thread = None
        
    def prepare_typing(self):
        """Prepare for typing with a countdown"""
        if not self.input_text.get("1.0", tk.END).strip():
            self.status_var.set("Error: No text to type")
            return
            
        self.typing_active = True
        self.start_button.config(state=tk.DISABLED)
        self.cancel_button.config(state=tk.NORMAL)
        
        # Start countdown
        self.countdown_thread = threading.Thread(target=self.countdown, daemon=True)
        self.countdown_thread.start()
    
    def countdown(self):
        """Countdown before starting to type"""
        for i in range(5, 0, -1):
            if not self.typing_active:
                return
            self.timer_var.set(f"Starting in {i} seconds... Click where you want to type!")
            self.root.update()
            time.sleep(1)
            
        self.timer_var.set("Typing now...")
        self.status_var.set("Typing in progress...")
        
        # Start typing in a separate thread
        self.typing_thread = threading.Thread(target=self.start_typing, daemon=True)
        self.typing_thread.start()
        
    def start_typing(self):
        """Begin typing text with human-like speed"""
        text = self.input_text.get("1.0", tk.END)
        wpm = self.wpm_var.get()
        use_variance = self.human_variance.get()
        
        # Calculate base delay between keypresses
        # Average word is ~5 characters, so chars per minute = WPM * 5
        chars_per_minute = wpm * 5
        base_delay = 60.0 / chars_per_minute  # seconds per character
        
        # Give extra time for user to switch focus
        time.sleep(0.5)
        
        # Type each character with appropriate delay
        chars_typed = 0
        total_chars = len(text)
        
        for char in text:
            if not self.typing_active:
                break
                
            # Type the character
            pyautogui.write(char)
            chars_typed += 1
            
            # Update status
            if chars_typed % 10 == 0:
                progress = int((chars_typed / total_chars) * 100)
                self.status_var.set(f"Typing: {progress}% complete ({chars_typed}/{total_chars} characters)")
                self.root.update_idletasks()
            
            # Delay between keypresses with variance if enabled
            if use_variance:
                # Add human-like variance (±20% randomness)
                variance = random.uniform(0.8, 1.2)
                delay = base_delay * variance
                
                # Slightly longer pauses at punctuation
                if char in ['.', ',', '!', '?', ';', ':', '\n']:
                    delay *= 1.5
            else:
                delay = base_delay
                
            time.sleep(delay)
        
        # Reset UI after typing completes
        if self.typing_active:
            self.typing_complete()
    
    def typing_complete(self):
        """Called when typing is complete"""
        self.typing_active = False
        self.status_var.set("Typing complete!")
        self.timer_var.set("")
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)
    
    def cancel_typing(self):
        """Cancel the typing process"""
        self.typing_active = False
        self.status_var.set("Typing cancelled")
        self.timer_var.set("")
        self.start_button.config(state=tk.NORMAL)
        self.cancel_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    try:
        # Create and run the application
        root = tk.Tk()
        app = TextTyperApp(root)
        root.mainloop()
    except Exception as e:
        # Show error in a simple message box
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"An error occurred: {str(e)}\n\nMake sure you have pyautogui installed.")
