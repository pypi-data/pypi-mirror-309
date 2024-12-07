# xnxx-dl-tagger

A Python script that recursively updates metadata tags of .mp4 files based on their file names and the directories they reside in. The script sets the Title, Genre, and Release Date tags of each .mp4 file:

Title: Derived from the file name (without the extension).
Genre: Taken from the name of the folder containing the file.
Release Date: Based on the file's last modification date.

Features:
Recursive Processing: Automatically traverses all subdirectories starting from the specified root directory.
Automated Metadata Assignment: Extracts and assigns metadata without manual intervention.
Error Handling: Includes try-except blocks to handle exceptions during file processing.
Non-destructive: Updates metadata in place without moving or altering the original files.

Requirements:
Python: Version 3.6 or higher.
Mutagen Library: A Python module to handle audio metadata.

Installation:
Clone the Repository

```sh
git clone https://github.com/thisisawesome1994/xnxx-dl-tagger.git
cd xnxx-dl-tagger
```

Create a Virtual Environment (Optional but Recommended)

```sh
python -m venv venv
```

Activate the Virtual Environment

On Windows:

```sh
venv\Scripts\activate
```

On macOS/Linux:

```sh
source venv/bin/activate
```

Install Dependencies

```sh
pip install mutagen
```

Usage
Place the Script in the Desired Directory

Ensure the script update_mp4_metadata.py is located in the root directory containing your .mp4 files and subdirectories.

Run the Script

```sh
python update_mp4_metadata.py
```

Optional: Specify a different root directory

```sh
python id3tag.py /path/to/your/root_directory
```

Script Explanation
```sh
import os
import time
from mutagen.mp4 import MP4, MP4Tags

def create_metadata(root_dir='.'):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        genre = os.path.basename(dirpath)  # Folder name as 'genre'
        for filename in filenames:
            if not filename.lower().endswith('.mp4'):
                continue
            file_path = os.path.join(dirpath, filename)
            name, ext = os.path.splitext(filename)  # File name without extension as 'name'
            mod_time = os.path.getmtime(file_path)
            mod_date = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mod_time))

            # Load MP4 file
            try:
                mp4_file = MP4(file_path)
            except Exception as e:
                print(f"Error processing {file_path}: {e}")
                continue

            # Prepare metadata
            mp4_file.tags = mp4_file.tags or MP4Tags()
            mp4_file.tags['\xa9nam'] = name  # Title
            mp4_file.tags['\xa9gen'] = genre  # Genre
            mp4_file.tags['\xa9day'] = mod_date  # Release Date

            # Save tags
            try:
                mp4_file.save()
                print(f"Metadata updated for {file_path}")
            except Exception as e:
                print(f"Error saving {file_path}: {e}")

if __name__ == "__main__":
    create_metadata(root_dir='.')  # Replace '.' with your root directory if needed
```

Example Directory Structure
```markdown
/Media
    /Action
        - Die_Hard.mp4
        - Mad_Max.mp4
    /Comedy
        - Superbad.mp4
        - The_Mask.mp4
After running the script, the metadata for Die_Hard.mp4 will be:

Title: Die_Hard
Genre: Action
Release Date: File's modification date
```

Troubleshooting
ModuleNotFoundError: No module named 'mutagen.mp4'; 'mutagen' is not a package
Cause: This error occurs when Python cannot find the mutagen library or there's a naming conflict.
Solution:

Ensure mutagen is Installed

```sh
pip install mutagen
```

Check for Naming Conflicts

Make sure there's no file named mutagen.py or a directory named mutagen in your project directory.
Delete any __pycache__ directories if present.


Check Python Version

```sh
python --version
```

Check Pip Version

```sh
pip --version
```
Contributing
Contributions are welcome! Please open an issue or submit a pull request for any enhancements or bug fixes.


License
This project is licensed under the MIT License.

Acknowledgements
Mutagen Library: For handling audio metadata in Python.
Contact
Author: Joannes Wyckmans
Email: none
Feel free to reach out with questions or feedback!
