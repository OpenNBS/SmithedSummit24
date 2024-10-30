import csv
import os

import pynbs

data = []

total_length = 0
total_notes = 0

for file in os.listdir("."):
    if file.endswith(".nbs"):

        print(f"Processing {file}...")

        # Load the NBS file
        song = pynbs.read(file)

        note_count = len(song.notes)

        length_total = song.header.song_length / song.header.tempo
        length_minutes = int(length_total // 60)
        length_seconds = int(length_total % 60)
        length = f"{length_minutes}:{length_seconds:02}"

        total_length += length_total
        total_notes += note_count

        # Add the data to the list
        data.append(
            {
                "name": file,
                "length": length,
                "notes": note_count,
                "title": song.header.song_name,
                "author": song.header.song_author,
                "original_author": song.header.original_author,
            }
        )

        for instrument in song.instruments:
            if not instrument.file.startswith("minecraft/"):
                print(f"Warning: {instrument.file} is not a Minecraft sound file")

# Calculate totals
print(total_length)
data.append(
    {
        "name": "[TOTAL]",
        "length": f"{int(total_length // 60)}:{int(total_length % 60)}",
        "notes": total_notes,
        "title": "",
        "author": "",
        "original_author": "",
    }
)

# Write the data to a CSV file
with open("songs.csv", "w", newline="") as f:
    writer = csv.DictWriter(
        f, fieldnames=["name", "length", "notes", "title", "author", "original_author"]
    )
    writer.writeheader()
    writer.writerows(data)
