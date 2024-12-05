import eyed3
import csv
from pathlib import Path

    
def scan(args):
    mp3 = Path(args.path)
    print(mp3)
    fp = open(Path.cwd()/"songs.csv", "w", newline="", encoding="utf-8")

    songs_writer = csv.writer(fp)
    songs_writer.writerow(["Title", "New Title", "Artist(s)", "Album","Genre", "N°"])

    for song in mp3.rglob("*.mp3"):
        audiofile = eyed3.load(song)
        song_name = song.name[:-4]
        if audiofile is None:
            songs_writer.writerow([song_name])
        else:
            genre = audiofile.tag.genre.name if audiofile.tag.genre else None
            songs_writer.writerow([
                    song_name, 
                    None,  # New Title
                    audiofile.tag.artist, 
                    audiofile.tag.album, 
                    genre, 
                    audiofile.tag.track_num.count
                    ])        
    fp.close()


def edit(args):
    mp3 = Path(args.path)
    csv_file = args.csv if args.csv else Path.cwd()/"songs.csv"
    csv_is_modified = False
    with open(csv_file, encoding="utf-8") as fp:
        songs_reader = csv.reader(fp)
        rows = list(songs_reader)[1:]
        for index, row in enumerate(rows):
            filename = row[0] + ".mp3"
            try:
                audiofile = eyed3.load(mp3/filename)
            except OSError:
                continue
            if audiofile is not None:
                if row[2] != audiofile.tag.artist and audiofile.tag.artist is not None:
                    print(f"artist {row[2]} → {audiofile.tag.artist}")
                    audiofile.tag.artist = row[2]
                    audiofile.tag.save()
                if row[3] != audiofile.tag.album and audiofile.tag.album is not None:
                    print(f"album {row[3]} → {audiofile.tag.album}")
                    audiofile.tag.album = row[3]
                    audiofile.tag.save()
                
                genre = audiofile.tag.genre.name if audiofile.tag.genre else None
                if row[4] != genre and genre is not None:
                    print(f"genre {row[4]} → {genre}")
                    audiofile.tag.genre = row[4]
                    audiofile.tag.save()

            if row[1] != "" and row[1] != "Nouveau Titre":
                print(f"rename {row[0]} → {row[1]}")
                (mp3/Path(filename)).rename(mp3/(row[1]+".mp3"))
                updated_row = row
                updated_row[0] = row[1]
                updated_row[1] =  None
                rows[index] = updated_row
                csv_is_modified = True
    if csv_is_modified:
        with open(csv_file, "w", newline="", encoding="utf-8") as fp:
            songs_writer = csv.writer(fp)
            songs_writer.writerow(["Titre", "Nouveau Titre", "Artiste(s)", "Album","Genre", "N°"])
            songs_writer.writerows(rows)
                    