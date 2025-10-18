# Alias Manager Desktop App

A simple and intuitive desktop application for viewing, adding, editing, and deleting shell aliases for both bash and zsh. This app provides a clean graphical user interface (GUI) to manage your command-line shortcuts without needing to manually edit configuration files.

---

## Features

- **Unified View**: Displays all aliases from both `~/.bashrc` and `~/.zshrc` in a single, sortable list.
- **Add & Edit**: Easily create new aliases or modify existing ones through a simple form.
- **Delete with Confidence**: Remove unwanted aliases with the click of a button.
- **Automatic File Handling**: The app reads from and writes to your `.bashrc` and `.zshrc` files automatically.
- **Cross-Shell Compatibility**: Any alias you add, edit, or delete is updated in both shell configuration files simultaneously.
- **User-Friendly Interface**: A clean, two-panel layout makes managing aliases straightforward.

---

## Setup and Running

Follow these instructions to run the application on your local machine.

### Prerequisites

- Python 3.8+
- `pip` (Python's package installer)
- `venv` (for creating virtual environments)

---

### Steps

#### 1. Set Up Your Project Directory

Make sure your Python script (`alias.py`) and the icon (`alias_icon.png`) are in the same folder. Open your terminal and navigate into this folder.

#### 2. Create and Activate a Virtual Environment

It is highly recommended to use a virtual environment to keep project dependencies isolated.

```bash
# Create the virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

#### 3. Install Dependencies

With your virtual environment activated, install all the required packages from the `requirements.txt` file.

> **Note:** For this specific Tkinter app, the file may be empty, but this step is crucial for other projects.

```bash
pip install -r requirements.txt
```

#### 4. Run the Application

You're all set! Run the main script to launch the app.

```bash
python3 alias.py
```

---

## Building the Standalone Desktop App

Follow these instructions to package the script into a single, standalone executable that can be run on any Linux system, complete with an application icon.

### On Ubuntu / Linux

#### 1. Install PyInstaller

Make sure you are in your activated virtual environment.

```bash
pip install pyinstaller
```

#### 2. Build the Executable

Run the `pyinstaller` command from your project's root directory. This command bundles your script into a single file.

```bash
pyinstaller --onefile --windowed alias.py
```

#### 3. Make it Globally Executable (Optional)

Move the generated app from the `dist/` folder to a system-wide location so you can run it from anywhere.

```bash
# Make sure the file is executable
chmod +x dist/alias

# Move it to a directory in your PATH
sudo mv dist/alias /usr/local/bin/
```

---

## Create a Desktop Entry for App Launcher (Optional)

To make the app appear in your applications menu with its icon, create a `.desktop` file.

#### 1. Copy the Icon

```bash
sudo cp alias_icon.png /usr/share/pixmaps/alias.png
```

#### 2. Create and Edit the Desktop File

```bash
sudo nano /usr/share/applications/alias.desktop
```

Paste the following content into the file, then save and exit (`Ctrl+X`, `Y`, `Enter`):

```ini
[Desktop Entry]
Version=1.0
Name=Alias Manager
Comment=Manage shell aliases for bash and zsh
Exec=/usr/local/bin/alias
Icon=/usr/share/pixmaps/alias.png
Terminal=false
Type=Application
Categories=Utility;Application;
```

Your **Alias Manager** should now be available from your system's application launcher.

---
