# Newsfeed

Newsfeed is a desktop news browser built with Python and Tkinter. It uses the [NewsAPI](https://newsapi.org/) Top Headlines endpoint to fetch current articles and display them in a scrollable GUI.

## What it does

- Retrieves top headlines from NewsAPI.
- Lets you filter by:
  - keyword
  - language
  - country
  - category
  - source
  - page size and page number
- Shows article details including title, short description, source, author, publish date, article URL, and image URL.
- Opens article and image links in your default browser.
- Tries to load and preview article images in the app when available.

## Project structure

- `Newsapi.py` – main application logic, API calls, and GUI.
- `Fonts.py` – helper script to preview available Tkinter font families.

## Requirements

- Python 3.10+
- A NewsAPI key
- Python packages:
  - `newsapi-python`
  - `requests`
  - `Pillow`
- Tkinter (usually included with standard Python installs)

## Installation

1. Clone the repository.
2. Install dependencies:

```bash
pip install newsapi-python requests Pillow
```

## Configuration

Use your own NewsAPI key and avoid committing credentials to source control.
For safer local setup, prefer environment-based configuration (for example, storing your key in an environment variable and reading it at runtime) instead of hardcoding secrets.

## Run

From the repository root:

```bash
python Newsapi.py
```

The app starts with default English headlines, then you can adjust filters and search again using the GUI controls.

## Notes

- NewsAPI applies request limits depending on your account plan.
- Some returned fields may be missing (`None`) depending on the source.
- Image preview availability depends on whether the source provides a valid image URL.
