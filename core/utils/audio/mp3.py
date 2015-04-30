from mutagen.easyid3 import EasyID3, mutagen
from mutagen.id3 import ID3, TPE1, TIT2, TALB, TCON, COMM, TDRC
from mutagen.mp3 import MP3
from core.utils.audio import Mp3FileNotFoundException


def mp3_length(source_file):
    try:
        audio = MP3(source_file)
        return audio.info.length
    except IOError:
        raise Mp3FileNotFoundException("Audio file not found: %s" % source_file)


def tag_mp3(source_file, artist, title, url="", album="", year="", comment="", genres=""):
    try:
        audio = EasyID3(source_file)
    except mutagen.id3.ID3NoHeaderError:
        audio = mutagen.File(source_file, easy=True)
        audio.add_tags()

    audio["artist"] = artist
    audio["title"] = title
    audio["genre"] = genres
    audio["website"] = url
    audio["copyright"] = "Deep South Sounds"
    audio["album"] = album

    audio.save(v1=2)
