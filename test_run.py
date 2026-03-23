from src.database import SongDatabase
from src.recognize import recognize
from src.utils import load_audio

db = SongDatabase()
db.index_directory("songs/")

audio, sr = load_audio("songs/Al Compás De Mi Caballo.wav")

clip = audio[int(3 * sr):int(8 * sr)]

name, score, scores = recognize(clip, sr, db)

print("Resultado:", name, score)