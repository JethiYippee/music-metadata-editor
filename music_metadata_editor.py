import tkinter as tk
from tkinter import filedialog, messagebox
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from mutagen.oggvorbis import OggVorbis
from mutagen.mp3 import MP3
import os

class MusicMetadataEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Music Metadata Editor")
        self.root.configure(bg="#333333")  # Set the background color to dark gray

        self.file_paths = []

        # Upload file button
        self.upload_button = tk.Button(root, text="Upload Files", command=self.upload_files, bg="#555555", fg="white")
        self.upload_button.pack(pady=10)

        # File name field
        self.file_name_var = tk.StringVar()
        self.file_name_check_var = tk.BooleanVar(value=True)
        file_name_frame = tk.Frame(root, bg="#333333")
        file_name_frame.pack()
        file_name_check_button = tk.Checkbutton(file_name_frame, variable=self.file_name_check_var, bg="#333333", fg="white", selectcolor="black")
        file_name_check_button.pack(side=tk.LEFT)
        file_name_label = tk.Label(file_name_frame, text="File Name", bg="#333333", fg="white")
        file_name_label.pack(side=tk.LEFT)
        self.file_name_entry = tk.Entry(file_name_frame, textvariable=self.file_name_var, width=50, bg="#555555", fg="white", insertbackground="white")
        self.file_name_entry.pack(side=tk.LEFT)

        # Metadata fields
        self.fields = {
            "Title": (tk.StringVar(), tk.BooleanVar(value=True)),
            "Artist": (tk.StringVar(), tk.BooleanVar(value=True)),
            "Album": (tk.StringVar(), tk.BooleanVar(value=True)),
            "Tracknumber": (tk.StringVar(), tk.BooleanVar(value=True)),  # Corrected key for track number
            "Genre": (tk.StringVar(), tk.BooleanVar(value=True)),
            "Year": (tk.StringVar(), tk.BooleanVar(value=True))
        }

        for field, (var, check_var) in self.fields.items():
            frame = tk.Frame(root, bg="#333333")
            frame.pack()
            check_button = tk.Checkbutton(frame, variable=check_var, bg="#333333", fg="white", selectcolor="black")
            check_button.pack(side=tk.LEFT)
            label = tk.Label(frame, text=field, bg="#333333", fg="white")
            label.pack(side=tk.LEFT)
            entry = tk.Entry(frame, textvariable=var, width=50, bg="#555555", fg="white", insertbackground="white")
            entry.pack(side=tk.LEFT)

        # Save button
        self.save_button = tk.Button(root, text="Save", command=self.save_metadata, bg="#555555", fg="white")
        self.save_button.pack(pady=10)

    def upload_files(self):
        self.file_paths = filedialog.askopenfilenames(filetypes=[("Audio files", "*.mp3 *.flac *.ogg")])
        if self.file_paths:
            self.load_metadata()

    def load_metadata(self):
        if self.file_paths:
            file_path = self.file_paths[0]
            ext = os.path.splitext(file_path)[1].lower()
            self.file_name_var.set(os.path.basename(file_path))
            if ext == ".mp3":
                audio = MP3(file_path, ID3=EasyID3)
            elif ext == ".flac":
                audio = FLAC(file_path)
            elif ext == ".ogg":
                audio = OggVorbis(file_path)
            else:
                return
            for field, (var, _) in self.fields.items():
                if field.lower() in audio:
                    var.set(audio[field.lower()][0])

    def save_metadata(self):
        if self.file_paths:
            for file_path in self.file_paths:
                ext = os.path.splitext(file_path)[1].lower()
                if ext == ".mp3":
                    audio = MP3(file_path, ID3=EasyID3)
                elif ext == ".flac":
                    audio = FLAC(file_path)
                elif ext == ".ogg":
                    audio = OggVorbis(file_path)
                else:
                    continue
                for field, (var, check_var) in self.fields.items():
                    if check_var.get():
                        key = field.lower()
                        if key == "tracknumber":
                            key = "tracknumber"
                        audio[key] = var.get()
                audio.save()

                if self.file_name_check_var.get():
                    new_file_name = self.file_name_var.get()
                    new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

                    if new_file_name != os.path.basename(file_path):
                        base_name, ext = os.path.splitext(new_file_name)
                        counter = 1
                        while os.path.exists(new_file_path):
                            new_file_name = f"{base_name} ({counter}){ext}"
                            new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)
                            counter += 1
                        os.rename(file_path, new_file_path)

            messagebox.showinfo("Success", "File(s) have been saved successfully!")

if __name__ == "__main__":
    root = tk.Tk()
    editor = MusicMetadataEditor(root)
    root.mainloop()
