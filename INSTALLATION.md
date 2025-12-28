# Installation Guide

## Quick Start

### macOS / Linux

```bash
# Clone the repository
git clone https://github.com/yourusername/screen-assistant.git
cd screen-assistant

# Run the installation script
./install.sh

# Or manually install dependencies
pip3 install -r requirements.txt

# Set up your API key
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### Windows

```powershell
# Clone the repository
git clone https://github.com/yourusername/screen-assistant.git
cd screen-assistant

# Install dependencies
pip install -r requirements.txt

# Set up your API key
# Copy .env.example to .env and edit it
# Add your OPENAI_API_KEY
```

## Detailed Installation

### Prerequisites

- Python 3.8 or higher
- pip (Python package manager)
- OpenAI API key with GPT-4 Vision access

### Step 1: Install Python Dependencies

```bash
pip install -r requirements.txt
```

Or if you prefer a virtual environment (recommended):

```bash
# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# On macOS/Linux:
source venv/bin/activate
# On Windows:
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Step 2: Get OpenAI API Key

1. Go to [OpenAI Platform](https://platform.openai.com/api-keys)
2. Sign in or create an account
3. Create a new API key
4. Make sure your account has access to GPT-4 Vision

### Step 3: Configure API Key

Create a `.env` file in the project root:

```bash
OPENAI_API_KEY=sk-your-actual-api-key-here
```

**Important**: Never commit your `.env` file to git! It's already in `.gitignore`.

### Step 4: Run the Application

**GUI Version (Recommended):**
```bash
python3 screen_assistant_gui.py
```

**CLI Version:**
```bash
python3 screen_assistant.py
```

## Platform-Specific Setup

### macOS

1. Install dependencies (see above)
2. On first run, grant Accessibility permissions:
   - System Settings → Privacy & Security → Accessibility
   - Add Terminal or Python to allowed apps
3. The hotkey `Cmd+Shift+A` will work after granting permissions

### Linux

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install python3-tk python3-pip
pip3 install -r requirements.txt
```

**Fedora/RHEL:**
```bash
sudo dnf install python3-tkinter python3-pip
pip3 install -r requirements.txt
```

### Windows

1. Install Python from [python.org](https://www.python.org/downloads/)
2. Make sure to check "Add Python to PATH" during installation
3. Open Command Prompt or PowerShell
4. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

## Troubleshooting

### "Module not found" errors

Make sure you're using the correct Python version and have installed all dependencies:
```bash
python3 --version  # Should be 3.8 or higher
pip3 install -r requirements.txt
```

### Hotkey not working (macOS)

1. Grant Accessibility permissions (see macOS setup above)
2. Restart the application
3. Try the hotkey again

### Screenshot capture fails

- On Linux, you may need additional permissions
- On Windows, make sure you're not running in a restricted environment
- Try running as administrator if needed

### API Key errors

- Make sure your `.env` file is in the project root
- Check that the API key is correct (starts with `sk-`)
- Verify your OpenAI account has GPT-4 Vision access
- Check your API usage limits on OpenAI dashboard

## Uninstallation

Simply delete the project directory:

```bash
rm -rf screen-assistant
```

If you installed globally with `pip install -e .`:
```bash
pip uninstall screen-assistant
```

