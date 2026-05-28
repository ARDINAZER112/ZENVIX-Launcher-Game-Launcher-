# Navigation
* [About](#-zenvix-launcher--game-launcher)
* [Key Features](#-key-features)
* [Prerequisites & Dependencies](#%EF%B8%8F-prerequisites-&-dependencies)
* [Project Structure](#-project-structure)
* [How to Run](#-how-to-run)
* [Color Configuration](#-color-configuration-&-style-guide)
* [License](#-license)

## Language / Bahasa
* [Indonesia](README_id.md)
* [English](README_en.md)

---

# 🚀 ZENVIX Launcher // Game Launcher

Game Launcher is a desktop application built with **Python 3** and **Tkinter**, designed to manage and launch your game collection from a single place. The application interface features a **Futuristic Cyberpunk / Tactical Tech** theme inspired by the UI style of *Arknights: Endfield*, dominated by a deep *matte charcoal* color and Neon Yellow accents (`#dfff00`).

---

## ⚡ Key Features

- **UI / UX**: A modern, clean dark interface (*matte black/panel charcoal*) with high contrast for eye comfort.
- **Dynamic Button Transition**: The main **RUN GAME** button features an animated color transition that dims to a darker shade when hovered by the mouse pointer (*hover effect*), mimicking the functionality of military HUD systems.
- **Comprehensive Game Management**: Complete features to Add, Edit, Delete, and Run games instantly.
- **Automatic Folder Scanning (Auto Scan)**: Capable of scanning entire folders to detect game executables (`.exe`, `.sh`, `.bat`, etc.) while automatically searching for matching icon files.
- **Local Icon Copying & Management System**: Automatically copies game icons into a local directory (`icons/`) and uses a caching method (via *Pillow*) to keep table loading performance smooth with a generous row height (`rowheight=42`).
- **Cross-Platform Support (Wine Integration)**: Automatically detects the operating system. On Linux systems, an integration option is available to run Windows executable files (`.exe`) using **Wine** directly from the launcher.
- **Smart Centered Windows**: Improved geometry calculations ensuring that the main window, add/edit dialog windows, and file explorer dialogs always appear precisely centered on the screen or above their parent window.

---

## 🛠️ Prerequisites & Dependencies

Ensure **Python 3** is installed on your device. For optimal visual rendering performance of game icons, it is highly recommended to install the **Pillow (PIL)** library.

### Dependency Installation (Linux / Windows)

```bash
pip install Pillow

```

*Note for Linux users:* If Tkinter is not installed by default on your system, install it via your package manager:

#### Ubuntu / Debian / Mint

```bash
sudo apt install python3-tk

```

#### Arch Linux / Manjaro

```bash
sudo pacman -S tk

```

#### Fedora

```bash
sudo dnf install python3-tkinter

```

#### CentOS / RHEL

```bash
sudo yum install python3-tkinter

```

If the system's default Python encounters conflicts or issues, it is recommended to use a Virtual Environment (venv):

### Venv Installation

#### Ubuntu / Debian / Mint

```bash
sudo apt update
sudo apt install python3-venv

```

#### Fedora

```bash
sudo dnf install python3-venv

```

#### Arch Linux

*The venv module is usually included in the main Python installation package on Arch Linux.*

### Creating a Virtual Environment

```bash
python3 -m venv .venv

```

### Activating Venv

```bash
source .venv/bin/activate

```

### Deactivating Venv

```bash
deactivate

```

---

## 📂 Project Structure

After running for the first time, the application will automatically create a local data configuration file and an icon storage folder:

```text
GameLauncher/
├── game_launcher.py  # Main application code file
├── games.json        # Local database for game data storage (JSON Format)
└── icons/            # Directory for storing and caching game icons

```

---

## 🚀 How to Run

Execute directly through the terminal or command prompt in the directory where the `game_launcher.py` file is saved:

```bash
python3 game_launcher.py

```

*If the system's default Python throws an error, use the virtual environment (venv) created earlier:*

### Activating Venv & Running the Launcher

```bash
source .venv/bin/activate
python3 game_launcher.py

```

### Exiting Venv (After Done)

```bash
deactivate

```

---

## 🔧 Color Configuration & Style Guide

If you want to modify the default color palette, here is the reference for the color codes used:

| Visual Component | Color Code (Hex) | Description |
| --- | --- | --- |
| **Main Background** | `#111214` | Deep matte black background color |
| **Panel / Input Box** | `#1b1c1f` | Background color for tables and text fields |
| **Main Accent** | `#dfff00` | Neon Yellow / Electric Lime for critical elements |
| **Primary Text** | `#f5f6f7` | Crisp white for high readability |
| **Secondary Text** | `#7e8494` | Dimmed gray for system status / labels |
| **Hover Run Button** | `#bacc00` | Dimmed yellow transition when hovered by the pointer |
| **Pressed Run Button** | `#94a300` | Tactical dark yellow when the button is clicked |

---

## 📝 License

This project is created for personal use and hobby development. Feel free to modify and develop it further to suit your game collection needs!

*If any information is missing, I apologize. If there are any bugs related to the launcher or if you would like to voluntarily contribute to its development, please feel free to do so.*

```