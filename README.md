# AI_Tool

Just a collection of AI based projects I'm working on in my free time.

## 1. Quote Wallpaper Generator

The Quote Wallpaper Generator is a Python application that allows you to create custom quote wallpapers. It provides a graphical user interface (GUI) for selecting various options such as language, category, art style, export formats, and API key. The generated wallpapers can be customized according to your preferences and can be saved in different formats.

### Features

- Select language: Choose the language for the quotes (English or Hindi).
- Choose category: Select the category of quotes you want to generate wallpapers for.
- Choose art style: Specify the art style for the wallpapers (e.g., abstract, anime, realistic).
- Custom vibe: Add an optional vibe to further personalize the wallpapers.
- Export formats: Choose the desired export formats, including square, padded, horizontal, vertical, with or without captions.
- API key: Enter your OpenAI API key to access the OpenAI language model for extracting features from quote and generating images for wallpapers.

### Prerequisites

- Python 3.x
- Dependencies: `customtkinter`, `tkinter` (built-in)

### Installation

1. Clone the repository or download the project files to your local machine.
2. Install the required dependencies by running the following command:

```bash
pip install customtkinter
```

### Usage

1. Open the terminal or command prompt and navigate to the project directory.
2. Run the following command to start the Quote Wallpaper Generator:

```bash
python WallpaperGenerator.py
```

3. The GUI application will open, allowing you to select the desired options for generating wallpapers.
4. Choose the language, category, art style, and other options according to your preferences.
5. Click the "Generate" button to generate the quote wallpapers. Be patient, it can take up to 1.5 minutes to generate all wallpapers.
6. The wallpapers will be saved in the specified export formats and can be accessed from the output folder.

### File Descriptions

- `WallpaperGenerator.py`: The main script that launches the Quote Wallpaper Generator application. It contains the GUI implementation using the `customtkinter` library and handles user interactions.
- `QuoteWallpaper.py`: A module that provides the functionality for generating quote wallpapers. It includes the `GenerateWallpaper` function, which utilizes the selected options and the OpenAI GPT-3 model to create the wallpapers.

### Contributing

Contributions to the Quote Wallpaper Generator project are welcome! If you encounter any issues, have suggestions for improvements, or would like to add new features, please feel free to open an issue or submit a pull request.

### License

The Quote Wallpaper Generator project is licensed under the [MIT License].

### Acknowledgments

- The Quote Wallpaper Generator utilizes the OpenAI GPT-3 language model for generating quotes. Special thanks to the OpenAI team for their incredible work.

### Contact

If you have any questions or need assistance with the Quote Wallpaper Generator, please contact aaryanbhardwaj97@gmail.com.
