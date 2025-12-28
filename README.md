# Screen Context GPT Assistant

A Python application that allows you to ask GPT questions while automatically sharing a screenshot of your screen for context-aware assistance. Perfect for getting help with software installation, troubleshooting, and step-by-step guidance.

## Features

- 📸 Automatic screen capture (window hides during capture)
- 🤖 GPT-4 Vision API integration with conversation history
- 💬 Interactive CLI interface
- 🖥️ **Spotlight-like GUI** (macOS-style overlay window)
- ⌨️ Global hotkey support (Cmd+Shift+A on macOS)
- 🔄 Conversation context maintained across questions
- 🔄 Reset session button to clear history
- 🔒 Secure API key management
- 🎨 Beautiful terminal output with Rich

## Installation

### Option 1: Install from Source (Recommended)

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/screen-assistant.git
   cd screen-assistant
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   
   Or install as a package:
   ```bash
   pip install -e .
   ```

3. **Set up your OpenAI API key:**
   - Create a `.env` file in the project root:
     ```bash
     cp .env.example .env
     ```
   - Edit `.env` and add your API key:
     ```
     OPENAI_API_KEY=your_api_key_here
     ```
   - Or export it as an environment variable:
     ```bash
     export OPENAI_API_KEY=your_api_key_here
     ```

### Option 2: Install via pip (if published)

```bash
pip install screen-assistant
```

Then create a `.env` file with your OpenAI API key.

## Usage

### GUI Version (Recommended - Spotlight-like Interface)

Run the GUI version:
```bash
python screen_assistant_gui.py
```

**Features:**
- Press **Cmd+Shift+A** (or customize in code) to open the assistant window
- A Spotlight-like overlay window appears
- Type your question and press Enter
- The app automatically captures your screen and sends it to GPT
- Results appear in the window
- Press **Escape** to close the window
- The app runs in the background - keep it running for quick access

### CLI Version

Run the CLI version:
```bash
python screen_assistant.py
```

The application will:
1. Capture a screenshot of your current screen
2. Wait for your question
3. Send both the screenshot and your question to GPT-4 Vision
4. Display the response

Type `quit` or `exit` to stop the application.

## Requirements

- Python 3.8+
- OpenAI API key with access to GPT-4 Vision
- macOS, Linux, or Windows

## Conversation History

The assistant maintains conversation context across all questions. This is perfect for multi-step processes like:
- Software installation guides
- Troubleshooting sequences
- Step-by-step tutorials
- Complex workflows

Each question includes the full conversation history, so GPT can reference previous steps. Use the "Reset Session" button to start a new conversation.

## Platform-Specific Notes

### macOS
- **Accessibility Permissions**: On first run, macOS may ask for accessibility permissions to enable global hotkeys. Grant permission in **System Settings > Privacy & Security > Accessibility**
- The GUI version uses **Cmd+Shift+A** by default to avoid conflicts with macOS Spotlight (Cmd+Space)
- The window automatically hides during screenshot capture

### Linux
- May require `python3-tk` package: `sudo apt-get install python3-tk` (Ubuntu/Debian)
- Global hotkeys may require additional permissions

### Windows
- Should work out of the box
- Global hotkeys may require running as administrator

## Technical Details

- Screenshots are captured automatically when you submit a question
- The screenshot is sent as base64-encoded image to the GPT API
- The GUI window hides during capture so it doesn't appear in screenshots
- Conversation history is maintained in memory (resets on app restart)
- Make sure you have sufficient API credits for GPT-4 Vision usage

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/screen-assistant.git
cd screen-assistant

# Install in development mode
pip install -e .

# Run tests (if available)
python -m pytest
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with OpenAI GPT-4 Vision API
- Uses [mss](https://github.com/BoboTiG/python-mss) for cross-platform screen capture
- GUI built with tkinter

