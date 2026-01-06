#!/usr/bin/env python3
"""
Screen Context GPT Assistant - GUI Version
A Spotlight-like interface for asking GPT questions with automatic screen capture.
"""

import os
import base64
import io
import threading
import tkinter as tk
from tkinter import ttk, scrolledtext
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image, ImageTk
import mss
import markdown
import mss
import markdown
import win32con
import httpx

# Load environment variables
load_dotenv()


class ScreenAssistantCore:
    """Core functionality for screen capture and GPT interaction."""
    
    def __init__(self):
        """Initialize the assistant with API client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY is required")
        
        # Configure SSL verification
        disable_ssl = os.getenv("DISABLE_SSL_VERIFY", "false").lower() == "true"
        http_client = httpx.Client(verify=not disable_ssl)
        
        self.client = OpenAI(api_key=api_key, http_client=http_client)
        self.model = "gpt-4o"
        # Initialize conversation history
        self.conversation_history = [
            {
                "role": "system",
                "content": "You are a helpful assistant that can see the user's screen. Analyze the screenshot and provide helpful, accurate answers to the user's questions. Be specific and actionable in your responses. Maintain context from previous interactions in the conversation."
            }
        ]
    
    def capture_screen(self) -> Optional[Image.Image]:
        """Capture a screenshot of the entire screen."""
        try:
            with mss.mss() as sct:
                monitor = sct.monitors[1]  # Primary monitor
                screenshot = sct.grab(monitor)
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                return img
        except Exception as e:
            print(f"Error capturing screen: {e}")
            return None
    
    def image_to_base64(self, image: Image.Image) -> str:
        """Convert PIL Image to base64 string."""
        buffered = io.BytesIO()
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def ask_gpt(self, question: str, screenshot: Image.Image) -> Optional[str]:
        """Send question and screenshot to GPT-4 Vision API with conversation history."""
        try:
            base64_image = self.image_to_base64(screenshot)
            
            # Add current user message with screenshot to history
            user_message = {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": question
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"data:image/jpeg;base64,{base64_image}",
                            "detail": "high"
                        }
                    }
                ]
            }
            
            # Add user message to history
            self.conversation_history.append(user_message)
            
            # Send full conversation history to GPT
            response = self.client.chat.completions.create(
                model=self.model,
                messages=self.conversation_history,
                max_tokens=1500,
                temperature=0.7
            )
            
            assistant_response = response.choices[0].message.content
            
            # Add assistant response to history
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_response
            })
            
            return assistant_response
            
        except Exception as e:
            print(f"Error communicating with GPT: {e}")
            return None
    
    def reset_conversation(self):
        """Reset the conversation history."""
        self.conversation_history = [
            {
                "role": "system",
                "content": "You are a helpful assistant that can see the user's screen. Analyze the screenshot and provide helpful, accurate answers to the user's questions. Be specific and actionable in your responses. Maintain context from previous interactions in the conversation."
            }
        ]


class SpotlightWindow:
    """Spotlight-like floating window for the assistant."""
    
    def __init__(self, assistant: ScreenAssistantCore):
        self.assistant = assistant
        self.root = None
        self.input_entry = None
        self.result_text = None
        self.status_label = None
        self.is_visible = False
        
    def create_window(self):
        """Create the Spotlight-like window."""
        self.root = tk.Tk()
        self.root.title("Screen Assistant")
        
        # Window configuration - Spotlight-like appearance
        # Note: overrideredirect can cause focus issues on macOS, so we'll keep window controls
        # self.root.overrideredirect(True)  # Commented out to fix focus issues
        self.root.attributes("-topmost", True)  # Always on top
        self.root.attributes("-alpha", 0.98)  # Slight transparency
        # Make window resizable but set min size
        self.root.resizable(False, False)
        
        # Get screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # Window size (Spotlight-like dimensions)
        window_width = 700
        window_height = 500
        
        # Center the window
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 3  # Slightly above center
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Modern color scheme (Spotlight-inspired)
        bg_color = "#2D2D2D"
        input_bg = "#3D3D3D"
        text_color = "#FFFFFF"
        accent_color = "#007AFF"
        
        self.root.configure(bg=bg_color)
        
        # Main container with padding
        main_frame = tk.Frame(self.root, bg=bg_color, padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_label = tk.Label(
            main_frame,
            text="Screen Assistant",
            font=("SF Pro Display", 16, "normal"),
            bg=bg_color,
            fg=text_color
        )
        title_label.pack(pady=(0, 15))
        
        # Input field (Spotlight-style)
        input_frame = tk.Frame(main_frame, bg=bg_color)
        input_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.input_entry = tk.Entry(
            input_frame,
            font=("SF Pro Display", 14),
            bg=input_bg,
            fg=text_color,
            insertbackground=text_color,
            relief=tk.FLAT,
            bd=0,
            highlightthickness=2,
            highlightbackground=accent_color,
            highlightcolor=accent_color
        )
        self.input_entry.pack(fill=tk.X, ipady=12, padx=2)
        self.input_entry.bind("<Return>", self.on_submit)
        self.input_entry.bind("<Escape>", self.hide_window)
        
        # Placeholder text handling
        self.placeholder = "Ask anything about your screen..."
        self.placeholder_active = True
        
        def on_entry_focus_in(event):
            if self.placeholder_active and self.input_entry.get() == self.placeholder:
                self.input_entry.delete(0, tk.END)
                self.input_entry.config(fg=text_color)
                self.placeholder_active = False
        
        def on_entry_focus_out(event):
            if not self.input_entry.get():
                self.input_entry.insert(0, self.placeholder)
                self.input_entry.config(fg="#888888")
                self.placeholder_active = True
        
        def on_key_release(event):
            # Check and clear placeholder after key is released (non-intrusive)
            if self.placeholder_active and self.input_entry.get() == self.placeholder:
                # If still showing placeholder, clear it
                current_text = self.input_entry.get()
                if current_text == self.placeholder:
                    self.input_entry.delete(0, tk.END)
                    self.input_entry.config(fg=text_color)
                    self.placeholder_active = False
        
        self.input_entry.bind("<FocusIn>", on_entry_focus_in)
        self.input_entry.bind("<FocusOut>", on_entry_focus_out)
        self.input_entry.bind("<KeyRelease>", on_key_release)  # Use KeyRelease - less intrusive
        
        # Set initial placeholder
        self.input_entry.insert(0, self.placeholder)
        self.input_entry.config(fg="#888888")
        
        # Status and reset button frame
        status_frame = tk.Frame(main_frame, bg=bg_color)
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Status label
        self.status_label = tk.Label(
            status_frame,
            text="",
            font=("SF Pro Display", 11),
            bg=bg_color,
            fg="#888888",
            anchor="w"
        )
        self.status_label.pack(side=tk.LEFT, fill=tk.X, expand=True)
        
        # Reset conversation button
        self.reset_button = tk.Button(
            status_frame,
            text="Reset Session",
            font=("SF Pro Display", 10),
            bg="#555555",
            fg=text_color,
            activebackground="#666666",
            activeforeground=text_color,
            relief=tk.FLAT,
            padx=12,
            pady=6,
            cursor="hand2",
            command=self.reset_conversation
        )
        self.reset_button.pack(side=tk.RIGHT, padx=(10, 0))
        
        # Result area (scrollable)
        result_frame = tk.Frame(main_frame, bg=bg_color)
        result_frame.pack(fill=tk.BOTH, expand=True)
        
        self.result_text = scrolledtext.ScrolledText(
            result_frame,
            font=("SF Pro Display", 12),
            bg=input_bg,
            fg=text_color,
            wrap=tk.WORD,
            relief=tk.FLAT,
            bd=0,
            padx=15,
            pady=15,
            insertbackground=text_color
        )
        self.result_text.pack(fill=tk.BOTH, expand=True)
        self.result_text.config(state=tk.DISABLED)
        
        # Bind Escape to close
        self.root.bind("<Escape>", self.hide_window)
        self.root.bind_all("<Escape>", self.hide_window)  # Also bind globally
        
        # Handle "X" button click - don't destroy, just hide
        self.root.protocol("WM_DELETE_WINDOW", lambda: self.hide_window(None))
        
        # Don't close on click outside - use Escape instead
        # self.root.bind("<Button-1>", self.check_click_outside)
        
        # Show window initially for testing (can be hidden later)
        # self.root.withdraw()
        
    def check_click_outside(self, event):
        """Check if click is outside the window and close if so."""
        if event.widget == self.root:
            self.hide_window(None)
    
    def show_window(self):
        """Show and focus the window."""
        if not self.root:
            self.create_window()
        
        self.root.deiconify()
        self.root.lift()
        self.root.focus_force()
        
        # Clear previous results
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.config(state=tk.DISABLED)
        
        # Clear input and reset placeholder
        self.input_entry.delete(0, tk.END)
        self.input_entry.insert(0, self.placeholder)
        self.input_entry.config(fg="#888888")
        self.placeholder_active = True
        
        # Focus on input field - use after() to ensure window is fully shown
        self.root.after(10, self._focus_input)
        self.status_label.config(text="")
        
        self.is_visible = True
    
    def _focus_input(self):
        """Helper method to focus input after window is shown."""
        try:
            # Force focus on the entry widget
            self.input_entry.focus_set()
            self.root.update_idletasks()
            self.input_entry.focus_force()
            
            if self.placeholder_active:
                # Select all placeholder text so typing replaces it immediately
                self.input_entry.select_range(0, tk.END)
                # Also select all on next update
                self.root.after(50, lambda: self.input_entry.select_range(0, tk.END))
            else:
                self.input_entry.icursor(tk.END)
        except Exception as e:
            print(f"Focus error: {e}")
    
    def hide_window(self, event):
        """Hide the window."""
        if self.root:
            self.root.withdraw()
            self.is_visible = False
    
    def toggle_window(self):
        """Toggle window visibility."""
        if self.is_visible:
            self.hide_window(None)
        else:
            self.show_window()
    
    def update_status(self, message: str):
        """Update status label."""
        if self.status_label:
            self.status_label.config(text=message)
            self.root.update()
    
    def display_result(self, text: str, question: str = None):
        """Display GPT response in the result area."""
        self.result_text.config(state=tk.NORMAL)
        
        # If there's existing content, add a separator
        if self.result_text.get(1.0, tk.END).strip():
            self.result_text.insert(tk.END, "\n" + "─" * 60 + "\n\n")
        
        # Show the question if provided
        if question:
            self.result_text.insert(tk.END, f"Q: {question}\n\n", "question")
            self.result_text.tag_config("question", foreground="#4A9EFF", font=("SF Pro Display", 11, "bold"))
        
        # Add the response
        self.result_text.insert(tk.END, f"A: {text}\n\n", "answer")
        self.result_text.tag_config("answer", foreground="#FFFFFF", font=("SF Pro Display", 12))
        
        self.result_text.config(state=tk.DISABLED)
        self.result_text.see(tk.END)
    
    def reset_conversation(self):
        """Reset the conversation history and clear the result area."""
        # Reset conversation history in the assistant
        self.assistant.reset_conversation()
        
        # Clear the result area
        self.result_text.config(state=tk.NORMAL)
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, "Conversation history cleared. Start a new session.\n")
        self.result_text.config(state=tk.DISABLED)
        
        # Update status
        self.status_label.config(text="✅ Session reset - conversation history cleared")
        
        # Clear status after 2 seconds
        self.root.after(2000, lambda: self.status_label.config(text=""))
    
    def on_submit(self, event):
        """Handle question submission."""
        question = self.input_entry.get().strip()
        
        # Check for placeholder or empty
        if self.placeholder_active or question == self.placeholder or not question:
            return
        
        # Disable input during processing
        self.input_entry.config(state=tk.DISABLED)
        self.update_status("📸 Capturing screen...")
        
        # Run in separate thread to avoid blocking UI
        thread = threading.Thread(target=self.process_question, args=(question,))
        thread.daemon = True
        thread.start()
    
    def process_question(self, question: str):
        """Process question in background thread."""
        import time
        
        try:
            # Hide window before capturing screenshot
            self.root.after(0, lambda: self.root.withdraw())
            self.root.after(0, lambda: self.update_status("📸 Hiding window and capturing screen..."))
            
            # Wait a moment for window to fully hide and screen to update
            time.sleep(0.3)
            
            # Capture screen (now without the GUI window)
            screenshot = self.assistant.capture_screen()
            
            # Show window again immediately after capture
            self.root.after(0, lambda: self.root.deiconify())
            self.root.after(0, lambda: self.root.lift())
            self.root.after(0, lambda: self.root.focus_force())
            
            if not screenshot:
                self.root.after(0, lambda: self.update_status("❌ Failed to capture screen"))
                self.root.after(0, lambda: self.input_entry.config(state=tk.NORMAL))
                return
            
            self.root.after(0, lambda: self.update_status("🤖 Sending to GPT (with conversation history)..."))
            
            # Ask GPT (conversation history is maintained automatically)
            response = self.assistant.ask_gpt(question, screenshot)
            
            if response:
                self.root.after(0, lambda: self.update_status("✅ Response received"))
                # Display result with question for context
                self.root.after(0, lambda: self.display_result(response, question))
            else:
                self.root.after(0, lambda: self.update_status("❌ Failed to get response"))
            
        except Exception as e:
            self.root.after(0, lambda: self.update_status(f"❌ Error: {str(e)}"))
            # Make sure window is shown even on error
            self.root.after(0, lambda: self.root.deiconify())
            self.root.after(0, lambda: self.root.lift())
        finally:
            self.root.after(0, lambda: self.input_entry.config(state=tk.NORMAL))
            self.root.after(0, lambda: self.input_entry.focus_set())
            # Ensure window is visible
            self.root.after(0, lambda: self.root.deiconify())
            self.root.after(0, lambda: self.root.lift())


class GlobalHotkeyManager:
    """Manages global hotkey using native Windows API to avoid hooks."""
    
    def __init__(self, window: SpotlightWindow):
        self.window = window
        self.running = False
        self.thread = None
        
    def start(self):
        """Start listening for hotkeys in a separate thread."""
        self.running = True
        self.thread = threading.Thread(target=self._listen)
        self.thread.daemon = True
        self.thread.start()
    
    def _listen(self):
        """Native message loop for hotkey."""
        import ctypes
        from ctypes import wintypes
        import win32con
        
        user32 = ctypes.windll.user32
        
        # Define constants
        MOD_ALT = 0x0001
        MOD_CONTROL = 0x0002
        MOD_SHIFT = 0x0004
        VK_A = 0x41
        HOTKEY_ID = 1
        
        # Register Hotkey: Ctrl + Shift + A
        if not user32.RegisterHotKey(None, HOTKEY_ID, MOD_CONTROL | MOD_SHIFT, VK_A):
            print("Failed to register native hotkey: Ctrl+Shift+A")
            return
            
        print("Native hotkey registered: Ctrl+Shift+A")
        
        try:
            msg = wintypes.MSG()
            while self.running:
                # GetMessage blocks until a message is received
                # We use PeekMessage with a small sleep to allow clean exit if needed
                if user32.PeekMessageW(ctypes.byref(msg), None, 0, 0, 1): # PM_REMOVE
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam == HOTKEY_ID:
                            self.on_activate()
                    user32.TranslateMessage(ctypes.byref(msg))
                    user32.DispatchMessageW(ctypes.byref(msg))
                else:
                    import time
                    time.sleep(0.01)
        finally:
            user32.UnregisterHotKey(None, HOTKEY_ID)
    
    def on_activate(self):
        """Handle hotkey activation."""
        if self.window.root:
            self.window.root.after(0, self.window.toggle_window)
    
    def stop(self):
        """Stop listening for hotkeys."""
        self.running = False


def main():
    """Entry point for the GUI application."""
    try:
        # Initialize core assistant
        assistant = ScreenAssistantCore()
        
        # Create GUI window
        window = SpotlightWindow(assistant)
        window.create_window()
        
        # Show window initially
        window.show_window()
        
        # Try to set up global hotkey (may fail without permissions)
        try:
            hotkey_manager = GlobalHotkeyManager(window)
            hotkey_manager.start()
            print("Screen Assistant GUI is running!")
            print("Press Ctrl+Shift+A to toggle the assistant window.")
            print("(Note: If hotkey doesn't work, grant Accessibility permissions)")
        except Exception as e:
            print(f"Hotkey setup failed: {e}")
            print("Window is visible - you can use it directly.")
            print("To enable hotkeys, grant Accessibility permissions in System Settings.")
        
        print("Press Escape to close the window.")
        
        # Run the GUI main loop
        window.root.mainloop()
        
    except ValueError as e:
        print(f"Error: {e}")
        print("Please set OPENAI_API_KEY in your .env file.")
    except Exception as e:
        print(f"Fatal error: {e}")


if __name__ == "__main__":
    main()

