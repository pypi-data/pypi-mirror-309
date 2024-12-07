__version__ = '0.0.2'

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