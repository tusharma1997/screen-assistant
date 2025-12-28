#!/usr/bin/env python3
"""
Screen Context GPT Assistant
A tool that allows you to ask GPT questions with automatic screen capture for context.
"""

import os
import base64
import io
from typing import Optional
from dotenv import load_dotenv
from openai import OpenAI
from PIL import Image
import mss
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.markdown import Markdown

# Load environment variables
load_dotenv()

console = Console()


class ScreenAssistant:
    """Main class for the screen context GPT assistant."""
    
    def __init__(self):
        """Initialize the assistant with API client."""
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            console.print("[red]Error: OPENAI_API_KEY not found in environment variables.[/red]")
            console.print("[yellow]Please set it in a .env file or export it as an environment variable.[/yellow]")
            raise ValueError("OPENAI_API_KEY is required")
        
        self.client = OpenAI(api_key=api_key)
        self.model = "gpt-4o"  # Using GPT-4o which has vision capabilities
    
    def capture_screen(self) -> Optional[Image.Image]:
        """
        Capture a screenshot of the entire screen.
        
        Returns:
            PIL Image object or None if capture fails
        """
        try:
            with mss.mss() as sct:
                # Get the primary monitor
                monitor = sct.monitors[1]  # 0 is all monitors, 1 is primary
                
                # Capture the screen
                screenshot = sct.grab(monitor)
                
                # Convert to PIL Image
                img = Image.frombytes("RGB", screenshot.size, screenshot.bgra, "raw", "BGRX")
                
                return img
        except Exception as e:
            console.print(f"[red]Error capturing screen: {e}[/red]")
            return None
    
    def image_to_base64(self, image: Image.Image) -> str:
        """
        Convert PIL Image to base64 string.
        
        Args:
            image: PIL Image object
            
        Returns:
            Base64 encoded string
        """
        buffered = io.BytesIO()
        # Convert to RGB if necessary (for PNG with transparency)
        if image.mode != "RGB":
            image = image.convert("RGB")
        image.save(buffered, format="JPEG", quality=85)
        img_str = base64.b64encode(buffered.getvalue()).decode()
        return img_str
    
    def ask_gpt(self, question: str, screenshot: Image.Image) -> Optional[str]:
        """
        Send question and screenshot to GPT-4 Vision API.
        
        Args:
            question: User's question
            screenshot: PIL Image of the screen
            
        Returns:
            GPT response text or None if error
        """
        try:
            # Convert screenshot to base64
            base64_image = self.image_to_base64(screenshot)
            
            console.print("[cyan]📸 Screenshot captured![/cyan]")
            console.print("[cyan]🤖 Sending to GPT...[/cyan]\n")
            
            # Prepare the message with image
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that can see the user's screen. Analyze the screenshot and provide helpful, accurate answers to the user's questions. Be specific and actionable in your responses."
                    },
                    {
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
                ],
                max_tokens=1000,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            console.print(f"[red]Error communicating with GPT: {e}[/red]")
            return None
    
    def run(self):
        """Main interactive loop."""
        console.print(Panel.fit(
            "[bold cyan]Screen Context GPT Assistant[/bold cyan]\n"
            "Ask questions about your screen and get AI-powered guidance!",
            border_style="cyan"
        ))
        console.print()
        
        while True:
            try:
                # Get user question
                question = Prompt.ask("[bold green]What would you like to know?[/bold green]")
                
                # Check for exit commands
                if question.lower() in ['quit', 'exit', 'q']:
                    console.print("[yellow]Goodbye![/yellow]")
                    break
                
                if not question.strip():
                    console.print("[yellow]Please enter a question.[/yellow]")
                    continue
                
                # Capture screen
                console.print("[cyan]📸 Capturing screen...[/cyan]")
                screenshot = self.capture_screen()
                
                if not screenshot:
                    console.print("[red]Failed to capture screen. Please try again.[/red]")
                    continue
                
                # Ask GPT
                response = self.ask_gpt(question, screenshot)
                
                if response:
                    # Display response in a nice format
                    console.print()
                    console.print(Panel(
                        Markdown(response),
                        title="[bold]GPT Response[/bold]",
                        border_style="green"
                    ))
                    console.print()
                else:
                    console.print("[red]Failed to get response from GPT.[/red]")
                
            except KeyboardInterrupt:
                console.print("\n[yellow]Interrupted. Goodbye![/yellow]")
                break
            except Exception as e:
                console.print(f"[red]Unexpected error: {e}[/red]")


def main():
    """Entry point for the application."""
    try:
        assistant = ScreenAssistant()
        assistant.run()
    except ValueError:
        # API key error already handled
        pass
    except Exception as e:
        console.print(f"[red]Fatal error: {e}[/red]")


if __name__ == "__main__":
    main()

