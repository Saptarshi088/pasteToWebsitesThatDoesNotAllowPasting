import tkinter as tk
from tkinter import scrolledtext, ttk
import pyautogui
import threading
import time
import random

class ModernTextTyperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("⚡ Ultra Fast Text Typer")
        self.root.geometry("900x800")
        self.root.minsize(850, 750)
        self.root.resizable(True, True)
        
        # Modern dark theme colors
        self.colors = {
            'bg_primary': '#1e1e1e',
            'bg_secondary': '#2d2d2d', 
            'bg_accent': '#3d3d3d',
            'text_primary': '#ffffff',
            'text_secondary': '#b3b3b3',
            'accent_blue': '#0078d4',
            'accent_green': '#16c60c',
            'accent_red': '#d13438',
            'accent_orange': '#ff8c00'
        }
        
        # Configure root
        self.root.configure(bg=self.colors['bg_primary'])
        
        # Configure modern ttk style
        self.setup_styles()
        
        # Create main container with padding
        main_container = tk.Frame(root, bg=self.colors['bg_primary'])
        main_container.pack(fill=tk.BOTH, expand=True, padx=25, pady=25)
        
        # Header section
        self.create_header(main_container)
        
        # Text input section
        self.create_text_input_section(main_container)
        
        # Controls section
        self.create_controls_section(main_container)
        
        # Action buttons section
        self.create_action_section(main_container)
        
        # Status section
        self.create_status_section(main_container)
        
        # Help section
        self.create_help_section(main_container)
        
        # Initialize control variables
        self.typing_active = False
        self.typing_thread = None
        self.countdown_thread = None
        
    def setup_styles(self):
        """Setup modern ttk styles"""
        style = ttk.Style()
        
        # Configure scale style
        style.configure('Modern.Horizontal.TScale', 
                       background=self.colors['bg_secondary'],
                       troughcolor=self.colors['bg_accent'],
                       slidercolor=self.colors['accent_blue'])
        
    def create_header(self, parent):
        """Create modern header with title and subtitle"""
        header_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        header_frame.pack(fill=tk.X, pady=(0, 30))
        
        # Main title
        title_label = tk.Label(
            header_frame,
            text="⚡ ULTRA FAST TEXT TYPER",
            font=("Segoe UI", 24, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_primary']
        )
        title_label.pack()
        
        # Subtitle
        subtitle_label = tk.Label(
            header_frame,
            text="Lightning-fast automated typing with customizable settings",
            font=("Segoe UI", 11),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_primary']
        )
        subtitle_label.pack(pady=(5, 0))
        
    def create_text_input_section(self, parent):
        """Create text input area with modern styling"""
        input_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', bd=2)
        input_frame.pack(fill=tk.BOTH, expand=False, pady=(0, 20))
        
        # Section title
        input_title = tk.Label(
            input_frame,
            text="📝 YOUR TEXT",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        input_title.pack(anchor="w", padx=20, pady=(15, 10))
        
        # Text area with custom styling
        text_container = tk.Frame(input_frame, bg=self.colors['bg_secondary'])
        text_container.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        self.input_text = scrolledtext.ScrolledText(
            text_container,
            width=70,
            height=6,
            wrap=tk.WORD,
            font=("Consolas", 11),
            bg=self.colors['bg_accent'],
            fg=self.colors['text_primary'],
            insertbackground=self.colors['text_primary'],
            selectbackground=self.colors['accent_blue'],
            relief='flat',
            bd=5
        )
        self.input_text.pack(fill=tk.X)
        
    def create_controls_section(self, parent):
        """Create controls with modern sliders and options"""
        controls_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', bd=2)
        controls_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Section title
        controls_title = tk.Label(
            controls_frame,
            text="⚙️ SETTINGS",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        controls_title.pack(anchor="w", padx=20, pady=(15, 15))
        
        # Controls grid
        controls_grid = tk.Frame(controls_frame, bg=self.colors['bg_secondary'])
        controls_grid.pack(fill=tk.X, padx=20, pady=(0, 20))
        
        # Speed control
        speed_frame = tk.Frame(controls_grid, bg=self.colors['bg_secondary'])
        speed_frame.pack(fill=tk.X, pady=(0, 15))
        
        speed_label = tk.Label(
            speed_frame,
            text="🚀 Typing Speed (WPM)",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        speed_label.pack(side=tk.LEFT)
        
        self.wpm_var = tk.IntVar(value=3000)  # Much faster default
        self.wpm_value_label = tk.Label(
            speed_frame,
            text=f"{self.wpm_var.get()} WPM",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['accent_blue'],
            bg=self.colors['bg_secondary']
        )
        self.wpm_value_label.pack(side=tk.RIGHT)
        
        self.wpm_scale = tk.Scale(
            speed_frame,
            from_=1000,
            to=10000,  # Much higher max speed
            resolution=100,
            orient=tk.HORIZONTAL,
            variable=self.wpm_var,
            length=300,
            bg=self.colors['bg_accent'],
            fg=self.colors['text_primary'],
            highlightthickness=0,
            troughcolor=self.colors['bg_accent'],
            activebackground=self.colors['accent_blue'],
            command=self.update_speed_label
        )
        self.wpm_scale.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Delay control
        delay_frame = tk.Frame(controls_grid, bg=self.colors['bg_secondary'])
        delay_frame.pack(fill=tk.X, pady=(0, 15))
        
        delay_label = tk.Label(
            delay_frame,
            text="⏱️ Start Delay (seconds)",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        delay_label.pack(side=tk.LEFT)
        
        self.delay_var = tk.IntVar(value=3)
        self.delay_value_label = tk.Label(
            delay_frame,
            text=f"{self.delay_var.get()}s",
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['accent_orange'],
            bg=self.colors['bg_secondary']
        )
        self.delay_value_label.pack(side=tk.RIGHT)
        
        self.delay_scale = tk.Scale(
            delay_frame,
            from_=1,
            to=15,
            resolution=1,
            orient=tk.HORIZONTAL,
            variable=self.delay_var,
            length=300,
            bg=self.colors['bg_accent'],
            fg=self.colors['text_primary'],
            highlightthickness=0,
            troughcolor=self.colors['bg_accent'],
            activebackground=self.colors['accent_orange'],
            command=self.update_delay_label
        )
        self.delay_scale.pack(side=tk.RIGHT, padx=(20, 0))
        
        # Options
        options_frame = tk.Frame(controls_grid, bg=self.colors['bg_secondary'])
        options_frame.pack(fill=tk.X)
        
        self.human_variance = tk.BooleanVar(value=False)  # Disabled for max speed
        self.variance_check = tk.Checkbutton(
            options_frame,
            text="🎯 Human-like variance (reduces speed)",
            variable=self.human_variance,
            font=("Segoe UI", 10),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_accent'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['text_primary']
        )
        self.variance_check.pack(side=tk.LEFT)
        
        self.instant_mode = tk.BooleanVar(value=False)
        self.instant_check = tk.Checkbutton(
            options_frame,
            text="⚡ INSTANT MODE (Maximum Speed)",
            variable=self.instant_mode,
            font=("Segoe UI", 10, "bold"),
            fg=self.colors['accent_green'],
            bg=self.colors['bg_secondary'],
            selectcolor=self.colors['bg_accent'],
            activebackground=self.colors['bg_secondary'],
            activeforeground=self.colors['accent_green']
        )
        self.instant_check.pack(side=tk.RIGHT)
        
    def create_action_section(self, parent):
        """Create action buttons with modern styling"""
        action_frame = tk.Frame(parent, bg=self.colors['bg_primary'])
        action_frame.pack(fill=tk.X, pady=(0, 25))
        
        # Start button
        self.start_button = tk.Button(
            action_frame,
            text="🚀 START TYPING",
            command=self.prepare_typing,
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['accent_green'],
            fg='white',
            activebackground='#0ea50e',
            relief='flat',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2'
        )
        self.start_button.pack(side=tk.LEFT, padx=(0, 15))
        
        # Cancel button
        self.cancel_button = tk.Button(
            action_frame,
            text="❌ CANCEL",
            command=self.cancel_typing,
            font=("Segoe UI", 14, "bold"),
            bg=self.colors['accent_red'],
            fg='white',
            activebackground='#b12226',
            relief='flat',
            bd=0,
            padx=30,
            pady=12,
            cursor='hand2',
            state=tk.DISABLED
        )
        self.cancel_button.pack(side=tk.LEFT)
        
        # Clear button
        self.clear_button = tk.Button(
            action_frame,
            text="🗑️ CLEAR TEXT",
            command=self.clear_text,
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['bg_accent'],
            fg=self.colors['text_primary'],
            activebackground=self.colors['bg_secondary'],
            relief='flat',
            bd=0,
            padx=20,
            pady=8,
            cursor='hand2'
        )
        self.clear_button.pack(side=tk.RIGHT)
        
    def create_status_section(self, parent):
        """Create status display with modern styling"""
        status_frame = tk.Frame(parent, bg=self.colors['bg_secondary'], relief='flat', bd=2)
        status_frame.pack(fill=tk.X, pady=(0, 25))
        
        status_container = tk.Frame(status_frame, bg=self.colors['bg_secondary'])
        status_container.pack(fill=tk.X, padx=20, pady=15)
        
        # Status label
        self.status_var = tk.StringVar(value="Ready to type")
        self.status_label = tk.Label(
            status_container,
            textvariable=self.status_var,
            font=("Segoe UI", 12),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_secondary']
        )
        self.status_label.pack(side=tk.LEFT)
        
        # Timer label
        self.timer_var = tk.StringVar()
        self.timer_label = tk.Label(
            status_container,
            textvariable=self.timer_var,
            font=("Segoe UI", 14, "bold"),
            fg=self.colors['accent_orange'],
            bg=self.colors['bg_secondary']
        )
        self.timer_label.pack(side=tk.RIGHT)
        
    def create_help_section(self, parent):
        """Create help section with modern styling"""
        help_frame = tk.Frame(parent, bg=self.colors['bg_accent'], relief='flat', bd=2)
        help_frame.pack(fill=tk.X)
        
        help_title = tk.Label(
            help_frame,
            text="💡 HOW TO USE",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['text_primary'],
            bg=self.colors['bg_accent']
        )
        help_title.pack(anchor="w", padx=20, pady=(15, 5))
        
        help_text = ("1. Paste or type your text in the input area above\n"
                    "2. Adjust typing speed and start delay to your preference\n" 
                    "3. Click 'START TYPING' and quickly click where you want the text\n"
                    "4. The app will type your text at lightning speed!")
        
        help_label = tk.Label(
            help_frame,
            text=help_text,
            font=("Segoe UI", 10),
            fg=self.colors['text_secondary'],
            bg=self.colors['bg_accent'],
            justify=tk.LEFT
        )
        help_label.pack(anchor="w", padx=20, pady=(0, 15))
        
    def update_speed_label(self, value):
        """Update speed display label"""
        self.wpm_value_label.config(text=f"{value} WPM")
        
    def update_delay_label(self, value):
        """Update delay display label"""
        self.delay_value_label.config(text=f"{value}s")
        
    def clear_text(self):
        """Clear the input text area"""
        self.input_text.delete("1.0", tk.END)
        self.status_var.set("Text cleared - Ready to type")
        
    def prepare_typing(self):
        """Prepare for typing with customizable countdown"""
        text_content = self.input_text.get("1.0", tk.END).strip()
        if not text_content:
            self.status_var.set("❌ Error: No text to type!")
            return
            
        self.typing_active = True
        self.start_button.config(state=tk.DISABLED, bg=self.colors['bg_accent'])
        self.cancel_button.config(state=tk.NORMAL, bg=self.colors['accent_red'])
        
        # Start countdown with custom delay
        self.countdown_thread = threading.Thread(target=self.countdown, daemon=True)
        self.countdown_thread.start()
        
    def countdown(self):
        """Countdown with customizable delay"""
        delay_seconds = self.delay_var.get()
        
        for i in range(delay_seconds, 0, -1):
            if not self.typing_active:
                return
            self.timer_var.set(f"⏰ {i}")
            self.status_var.set(f"🎯 Starting in {i} seconds - Click where you want to type!")
            self.root.update()
            time.sleep(1)
            
        self.timer_var.set("⚡ TYPING NOW!")
        self.status_var.set("🚀 Ultra-fast typing in progress...")
        
        # Start typing
        self.typing_thread = threading.Thread(target=self.start_typing, daemon=True)
        self.typing_thread.start()
        
    def start_typing(self):
        """Ultra-fast typing with minimal delays"""
        text = self.input_text.get("1.0", tk.END).rstrip('\n')
        wpm = self.wpm_var.get()
        use_variance = self.human_variance.get()
        instant_mode = self.instant_mode.get()
        
        # Give time to switch focus
        time.sleep(0.3)
        
        if instant_mode:
            # Instant mode - type everything at once
            pyautogui.write(text)
            self.typing_complete()
            return
            
        # Calculate ultra-fast delays
        chars_per_minute = wpm * 5
        base_delay = 60.0 / chars_per_minute
        
        # Make it even faster by reducing the base delay
        base_delay *= 0.5  # 50% faster than calculated
        
        chars_typed = 0
        total_chars = len(text)
        
        for char in text:
            if not self.typing_active:
                break
                
            pyautogui.write(char)
            chars_typed += 1
            
            # Update progress less frequently for better performance
            if chars_typed % 50 == 0 or chars_typed == total_chars:
                progress = int((chars_typed / total_chars) * 100)
                self.status_var.set(f"🚀 Typing: {progress}% ({chars_typed}/{total_chars})")
                self.root.update_idletasks()
            
            # Minimal delay calculation
            if use_variance and not instant_mode:
                variance = random.uniform(0.9, 1.1)  # Less variance for speed
                delay = base_delay * variance
                if char in ['.', '\n']:
                    delay *= 1.2  # Minimal pause for punctuation
            else:
                delay = base_delay
                
            # Ensure minimum speed
            delay = max(delay, 0.001)  # Minimum 1ms delay
            time.sleep(delay)
        
        if self.typing_active:
            self.typing_complete()
            
    def typing_complete(self):
        """Reset UI after typing completion"""
        self.typing_active = False
        self.status_var.set("✅ Typing completed successfully!")
        self.timer_var.set("🎉 DONE!")
        self.start_button.config(state=tk.NORMAL, bg=self.colors['accent_green'])
        self.cancel_button.config(state=tk.DISABLED, bg=self.colors['bg_accent'])
        
    def cancel_typing(self):
        """Cancel typing process"""
        self.typing_active = False
        self.status_var.set("❌ Typing cancelled")
        self.timer_var.set("")
        self.start_button.config(state=tk.NORMAL, bg=self.colors['accent_green'])
        self.cancel_button.config(state=tk.DISABLED, bg=self.colors['bg_accent'])

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = ModernTextTyperApp(root)
        root.mainloop()
    except Exception as e:
        import tkinter.messagebox as messagebox
        messagebox.showerror("Error", f"Application error: {str(e)}\n\nEnsure pyautogui is installed: pip install pyautogui")
