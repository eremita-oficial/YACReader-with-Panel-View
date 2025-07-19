# YACReader-with-Panel-View 📖✨

---

## Unlock Panel-by-Panel Reading for YACReader Comics!

This project provides a simple yet powerful launcher utility that seamlessly integrates your YACReader Library with external comic readers capable of **panel-by-panel (or guided view) reading**, like [BDReader](https://sourceforge.net/projects/bdreader/). If you love YACReader for organizing your vast comic collection but miss the immersive panel-by-panel experience on desktop, this tool is tailor-made for you!

Once installed, when you click on a comic in YACReader Library, a small, unobtrusive pop-up will appear. This pop-up lets you instantly choose whether to open the comic with the original YACReader application or your preferred external panel-by-panel reader.

---

## Features

* **Seamless Integration:** Works directly with your existing YACReader Library setup.
* **Reader Selection:** Choose on the fly between YACReader's default reader and an external reader (e.g., BDReader) via a quick pop-up.
* **Panel-by-Panel Focus:** Specifically designed for users who want to leverage external readers to achieve a guided, panel-focused viewing experience.
* **User-Friendly Pop-up:** A clean, minimalist selection window with automatic focus on the "YACReader (Original)" option, allowing for quick "Enter" key activation.
* **Robust Launching:** Ensures your chosen comic reader opens correctly and remains in focus, even if the application normally minimizes when launched by another process.

---

## How It Works

This project enhances your YACReader Library experience using two small executable files that intercept and redirect the comic launch process:

1.  **`YACReader.exe` (Python Script Compiled):** This acts as the initial interceptor. When you click a comic in YACReader Library, it calls this `YACReader.exe`. This script efficiently extracts the comic's full path from your YACReader database.
2.  **`YACReader_Selector.exe` (AutoIt Script Compiled):** Once the comic path is identified, the Python script launches this AutoIt executable. This is the component responsible for displaying the small, interactive pop-up window, allowing you to select your desired reader. Based on your choice, it then precisely launches either your original `YACReader_ORIG.exe` or your external reader (`BDReader.exe`) with the correct comic file.

---

## Installation Guide (No Compilation Required)

This is the recommended method for most users.

### Prerequisites

* **YACReader Library:** Must be already installed and configured with your comic collection.
* **BDReader (or your preferred external reader):** Make sure it's installed on your system.
    * **Important:** The current setup assumes BDReader is installed at the default path: `C:\Program Files (x86)\BDReader\BDReader.exe`. If your BDReader is installed elsewhere, this "no compilation" method won't work as is. You'll need to follow the "Installation for Developers" guide to customize the AutoIt script.

### Steps to Install

1.  **Download the Latest Release:**
    * Go to the [Releases](https://github.com/eremita-oficial/YACReader-with-Panel-View/releases) section of this GitHub repository.
    * Download the `YACReader-with-Panel-View.zip` (or similar) file from the latest release.
    * Extract the contents of the `.zip` file. You should find `YACReader.exe` and `YACReader_Selector.exe` inside.

2.  **Prepare Your YACReader Installation Folder:**
    * Navigate to your YACReader installation directory (typically `C:\Program Files\YACReader`).
    * **Crucial Step:** Find the existing `YACReader.exe` file (this is the comic reader, *not* `YACReaderLibrary.exe`) and **rename it to `YACReader_ORIG.exe`**.

3.  **Copy the New Files:**
    * Copy the `YACReader.exe` and `YACReader_Selector.exe` files you downloaded in Step 1 into your YACReader installation directory (e.g., `C:\Program Files\YACReader`).

4.  **Verify BDReader Path:**
    * Ensure `BDReader.exe` is installed and accessible at `C:\Program Files (x86)\BDReader\BDReader.exe`.

5.  **Test It Out!**
    * Close YACReader Library completely (check Task Manager to be sure).
    * Open YACReader Library and click on any comic. A selection pop-up should appear!

---

## Installation Guide for Developers (Requires Compilation)

This guide is for users who want to compile the scripts themselves or customize paths.

### Prerequisites

* **YACReader Library:** Already installed.
* **BDReader (or your preferred external reader):** Installed.
* **Python:** Install [Python](https://www.python.org/downloads/).
    * Install PyInstaller: `pip install pyinstaller`
* **AutoIt v3:** Download and install [AutoIt v3](https://www.autoitscript.com/site/autoit/downloads/). This includes the SciTE4AutoIt3 editor and the Au3toExe compiler.

### Steps to Compile & Install

1.  **Clone the Repository:**
    ```bash
    git clone [https://github.com/eremita-oficial/YACReader-with-Panel-View.git](https://github.com/YOUR_GITHUB_USERNAME/YACReader-with-Panel-View.git)
    cd YACReader-with-Panel-View
    ```
2.  **Customize (Optional):**
    * If your BDReader is *not* at `C:\Program Files (x86)\BDReader\BDReader.exe`, open `YACReader_Selector.au3` in a text editor (like SciTE4AutoIt3).
    * Locate the line `Global Const $g_sBDReaderPath = "C:\Program Files (x86)\BDReader\BDReader.exe"` and update the path to your BDReader executable. Save the file.
3.  **Compile `YACReader.py`:**
    * Open your terminal (CMD or PowerShell) in the repository root.
    * Run PyInstaller:
        ```bash
        pyinstaller --onefile --windowed YACReader.py
        ```
    * The compiled `YACReader.exe` will be in the `dist` subfolder.
4.  **Compile `YACReader_Selector.au3`:**
    * Open **SciTE4AutoIt3**.
    * Go to `Tools` -> `Compile` (or `Ferramentas` -> `Compilar`).
    * Select your `YACReader_Selector.au3` file from the repository folder.
    * Ensure it compiles to an executable (e.g., `YACReader_Selector.exe`) in the desired output folder (e.g., the `dist` folder alongside `YACReader.exe`). Make sure the "Console (Hidden)" option is selected for GUI applications.
5.  **Deploy Files:**
    * **Close YACReader Library completely.**
    * Navigate to your YACReader installation directory (e.g., `C:\Program Files\YACReader`).
    * **Rename** the original `YACReader.exe` to `YACReader_ORIG.exe`.
    * Copy the newly compiled `YACReader.exe` (from your Python `dist` folder) and `YACReader_Selector.exe` (from your AutoIt compilation output) into your YACReader installation directory.
6.  **Test!** Open YACReader Library and try opening a comic.

---

## Reinstallation / Upgrading YACReader Library

When you upgrade YACReader Library itself (e.g., installing a new version), the installer might overwrite your custom `YACReader.exe`. Follow these steps to ensure your `YACReader-with-Panel-View` setup continues to work:

1.  **Before Running the YACReader Library Installer:**
    * Navigate to `C:\Program Files\YACReader\`.
    * **Delete** your custom `YACReader.exe` and `YACReader_Selector.exe`.
    * **Rename `YACReader_ORIG.exe` back to `YACReader.exe`**. This allows the YACReader installer to update its original executable cleanly.

2.  **Run the YACReader Library Upgrade Installer.**
    * Proceed with the YACReader Library upgrade as usual.

3.  **After the YACReader Library Upgrade is Complete:**
    * Navigate back to `C:\Program Files\YACReader\`.
    * **Rename the newly installed `YACReader.exe` (from the YACReader upgrade) to `YACReader_ORIG.exe`**.
    * **Copy** your `YACReader.exe` (the one you compiled from Python) and `YACReader_Selector.exe` (the one you compiled from AutoIt) back into this folder.

Your `YACReader-with-Panel-View` setup should now be fully restored and working with the upgraded YACReader Library!

---

## Contributing

Feel free to open issues or submit pull requests if you have suggestions, bug reports, or improvements!

---
