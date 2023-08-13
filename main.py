import pathlib
import re
import sys

import mutagen
from mutagen.id3 import ID3, TRCK, TIT2

trim_artist_re = re.compile(r"^(?:(?:(?! - ).)* - )?(.+)$")

def number_album(dir, number_tracks, trim_artist):
    dir = pathlib.Path(dir).resolve()
    if not dir.is_dir():
        raise ValueError(f"{dir} is not a directory")
    paths = filter(lambda p: p.is_file(), dir.iterdir())
    if number_tracks:
        paths = sorted(paths, key=lambda p: p.stat().st_ctime)
    i = 1
    for path in paths:
        try:
            save = False
            audio = mutagen.File(path)
            if audio is None or audio.tags is None:
                print(f"skipping {path}")
                continue
            if number_tracks:
                audio.tags['TRCK'] = TRCK(encoding=3, text=str(i))
                save = True
            if trim_artist:
                match = trim_artist_re.match(str(audio.tags["TIT2"]))
                audio.tags["TIT2"] = TIT2(encoding=3, text=match.group(1))
                save = True
            if save:
                audio.save()
            i += 1
            
        except mutagen.MutagenError as e:
            print(e)

def main():
    number_album(sys.argv[1], "-t" in sys.argv, "-a" in sys.argv)

if __name__ == '__main__':
    main()
