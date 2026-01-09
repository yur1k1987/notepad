# PySide6 Notepad

A feature-rich, lightweight tabbed text editor written in Python using PySide6. Designed for developers and power users who need a versatile text editing solution with advanced encoding support, text manipulation tools, and extensive customization options.

---

- [PySide6 Notepad](#pyside6-notepad)
  - [Overview](#overview)
    - [Key Highlights](#key-highlights)
  - [Features](#features)
    - [File Management](#file-management)
    - [Search \& Navigation](#search--navigation)
    - [Encoding \& Line Endings](#encoding--line-endings)
    - [Text Manipulation Tools](#text-manipulation-tools)
    - [Display \& View Options](#display--view-options)
    - [Customization](#customization)
    - [Printing](#printing)
    - [Additional Features](#additional-features)
  - [Installation](#installation)
    - [Prerequisites](#prerequisites)
    - [Step 1: Clone or Download](#step-1-clone-or-download)
    - [Step 2: Install Dependencies](#step-2-install-dependencies)
    - [Step 3: Run the Application](#step-3-run-the-application)
  - [Usage](#usage)
    - [Basic Operations](#basic-operations)
    - [Finding Text](#finding-text)
    - [Changing Encoding](#changing-encoding)
    - [Customizing Appearance](#customizing-appearance)
    - [Keyboard Shortcuts](#keyboard-shortcuts)
  - [Configuration](#configuration)
  - [Technical Details](#technical-details)
    - [Architecture](#architecture)
    - [Supported File Types](#supported-file-types)
    - [Encoding Detection](#encoding-detection)
    - [Performance](#performance)
  - [Requirements](#requirements)
    - [Platform Support](#platform-support)
  - [Contributing](#contributing)
    - [Areas for Contribution](#areas-for-contribution)
  - [License](#license)
  - [Version](#version)
  - [Developer](#developer)


---

## Overview

PySide6 Notepad is a cross-platform text editor that combines the simplicity of a basic notepad with powerful features typically found in more advanced editors. It provides an intuitive interface for editing multiple files simultaneously, with robust encoding detection, comprehensive text manipulation tools, and extensive customization capabilities.

### Key Highlights

- **Multi-tab Interface**: Work with multiple files simultaneously in a clean, organized tabbed interface
- **Advanced Encoding Support**: Automatic encoding detection and support for various text encodings
- **Rich Text Manipulation**: Comprehensive set of text transformation and editing tools
- **Highly Customizable**: Extensive theming, color, and UI customization options
- **Developer-Friendly**: Line numbers, syntax highlighting for search matches, and various productivity features

---

## Features

### File Management

* **Multiple Tabs**: Open and edit multiple files simultaneously with an intuitive tabbed interface
* **Recent Files**: Quick access to recently opened files (up to 5 files by default)
* **Drag & Drop**: Open files by dragging them into the application window
* **File Operations**: New, open, save, save as, close, and close all operations
* **File Reloading**: Reload files from disk to discard unsaved changes
* **Rename Files**: Rename files directly from the tab context menu
* **Open Containing Folder**: Quickly navigate to the folder containing the current file

### Search & Navigation

* **Find & Replace**: Advanced find and replace dialog with multiple options
  - Case-sensitive search
  - Whole word matching
  - Wrap around search
  - Replace single occurrence or replace all
* **Go to Line**: Jump to any specific line number quickly
* **Search Highlighting**: Automatically highlights all search matches in the document
* **Current Line Highlighting**: Visual indicator for the current cursor line

### Encoding & Line Endings

* **Encoding Support**:
  - UTF-8 (default)
  - UTF-8 with BOM
  - UTF-16 Big Endian with BOM
  - UTF-16 Little Endian with BOM
  - Windows-1251 (Cyrillic)
  - OEM-866 (Cyrillic DOS)
* **Automatic Encoding Detection**: Uses `chardet` library to automatically detect file encoding
* **Line Ending Support**:
  - Windows (CRLF - `\r\n`)
  - Unix/Linux (LF - `\n`)
* **Encoding Switching**: Change encoding on-the-fly for each document
* **Line Ending Conversion**: Convert between Windows and Unix line endings

### Text Manipulation Tools

* **Case Conversion**:
  - Convert to UPPERCASE
  - Convert to lowercase
  - Convert to Title Case (Proper Case)
* **Space Management**:
  - Trim trailing spaces
  - Trim leading spaces
  - Remove all spaces
  - Convert tabs to spaces
* **Line Operations**:
  - Join lines (remove line breaks)
  - Remove empty lines
  - Remove duplicate lines
  - Sort lines (ascending/descending order)
* **Date/Time Insertion**: Insert current date and time at cursor position

### Display & View Options

* **Line Numbers**: Display line numbers in a dedicated gutter area
* **Zoom Controls**: Zoom in, zoom out, and restore zoom level
  - Mouse wheel zoom with Ctrl modifier
  - Keyboard shortcuts for zoom operations
* **Text Wrapping**: Toggle word wrap on/off
* **Show Whitespace**: Visualize spaces and tabs in the document
* **Status Bar**: Comprehensive status bar showing:
  - Current encoding
  - Line ending type
  - Cursor position (line and column)
  - Document length
  - Zoom level
  - Text format indicator

### Customization

* **Themes**: Choose from multiple application styles (Windows Vista, Windows, Fusion)
* **Color Customization**:
  - Text color
  - Background color
  - Current line highlight color
  - Line number area text color
  - Line number area background color
* **Font Settings**:
  - Font family selection
  - Font size
  - Bold and italic styles
* **UI Visibility**:
  - Show/hide menu bar
  - Show/hide status bar
  - Show/hide toolbar
  - Show/hide tab bar
* **Tab Bar Options**:
  - Vertical or horizontal tab bar
  - Show/hide tab close buttons
  - Movable tabs
* **Toolbar Icon Size**: Small (16px), Medium (24px), or Large (32px)
* **Window Options**: Keep window always on top

### Printing

* **Print Support**: Print documents with full printer dialog
* **Print Preview**: Preview documents before printing
* **High Resolution Printing**: Support for high-resolution printing

### Additional Features

* **Document Statistics**: View detailed information about the current document:
  - Character count (with/without line endings)
  - Word count
  - Line count
  - File path and metadata
  - Selection statistics
* **Undo/Redo**: Full undo/redo support with unlimited history
* **Context Menus**: Right-click context menus for tabs and document area
* **Settings Persistence**: All settings are saved to `config.ini` and restored on startup
* **Internationalization**: Support for English and Russian languages

---

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

### Step 1: Clone or Download

Clone the repository or download the source code:

```bash
git clone <repository-url>
cd notepad
```

### Step 2: Install Dependencies

Install the required Python packages:

```bash
pip install -r requirements.txt
```

This will install:
- **PySide6**: Qt for Python framework (provides GUI components)
- **chardet**: Character encoding detection library

### Step 3: Run the Application

Start the application:

```bash
python main.py
```

---

## Usage

### Basic Operations

1. **Creating a New File**: Click `File → New` or use the toolbar button
2. **Opening a File**: Click `File → Open` or drag and drop a file into the window
3. **Saving a File**: Click `File → Save` (Ctrl+S) or `File → Save As` for a new file
4. **Closing a Tab**: Click the X button on the tab or use `File → Close`

### Finding Text

1. Press `Ctrl+F` or go to `Edit → Find/Replace`
2. Enter your search term
3. Use options for case sensitivity, whole words, and wrap around
4. Click "Find" to search, or "Replace" to replace the current match

### Changing Encoding

1. Open a file (encoding is auto-detected)
2. Go to the encoding menu in the menu bar
3. Select the desired encoding
4. The encoding will be applied when you save the file

### Customizing Appearance

1. Go to `File → Options`
2. Adjust colors, fonts, and UI visibility settings
3. Changes are applied immediately and saved automatically

### Keyboard Shortcuts

- `Ctrl+N`: New file
- `Ctrl+O`: Open file
- `Ctrl+S`: Save file
- `Ctrl+Shift+S`: Save as
- `Ctrl+F`: Find/Replace
- `Ctrl+G`: Go to line
- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo
- `Ctrl+C`: Copy
- `Ctrl+X`: Cut
- `Ctrl+V`: Paste
- `Ctrl+A`: Select all
- `Ctrl+P`: Print
- `Ctrl+Wheel`: Zoom in/out

---

## Configuration

The application stores all settings in `config.ini` in the application directory. Settings include:

- Application style and language
- UI element visibility
- Color scheme
- Font preferences
- Window geometry
- Recent files list

Settings are automatically saved when you close the application and restored on the next launch.

---

## Technical Details

### Architecture

- **Framework**: PySide6 (Qt for Python)
- **UI Design**: Qt Designer (.ui files)
- **Encoding Detection**: chardet library
- **Settings Storage**: QSettings with INI format
- **Internationalization**: Qt translation system (.qm files)

### Supported File Types

The editor can open any text file. By default, it recognizes `.txt` files as text files, but you can open files with any extension.

### Encoding Detection

The application uses the `chardet` library to automatically detect file encoding when opening files. If detection fails, it defaults to UTF-8.

### Performance

- Efficient handling of large text files
- Optimized line number rendering
- Smooth scrolling and text editing

---

## Requirements

- **Python**: 3.7+
- **PySide6**: Latest version (installed via requirements.txt)
- **chardet**: Latest version (installed via requirements.txt)

### Platform Support

- Windows
- Linux
- macOS

---

## Contributing

Contributions are welcome! If you'd like to contribute:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

### Areas for Contribution

- Additional language translations
- New text manipulation tools
- Additional encoding support
- Bug fixes and performance improvements
- Documentation improvements

---

## License

MIT License — see [LICENSE](LICENSE.md) for details.

---

## Version

Current version: **0.1.2** (2026/01/09)

---

## Developer

**Yuri Pavlov**

---

<p align="center">
  <img src="https://komarev.com/ghpvc/?username=yur1k87-notepad&label=Project+Views&color=blue" alt="Project Views" />
</p>
