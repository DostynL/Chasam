import numpy as np

from src.fingerprint import SAMPLE_RATE, fingerprint_audio
from src.utils import highpass_filter


def recognize(audio, sample_rate, database):

    fingerprints = fingerprint_audio(audio, sample_rate)

    if not fingerprints:
        return None, 0, {}

    matches = {}

    for hash_val, t_clip in fingerprints:
        hits = database.table.lookup(hash_val)

        for song_id, t_song in hits:
            delta = t_song - t_clip
            matches.setdefault(song_id, []).append(delta)

    if not matches:
        return None, 0, {}

    best_song_id = None
    best_count = 0
    all_scores = {}

    for song_id, deltas in matches.items():
        histogram = {}

        for d in deltas:
            histogram[d] = histogram.get(d, 0) + 1

        peak_count = max(histogram.values())

        song_name = database.get_song_name(song_id)
        all_scores[song_name] = peak_count

        if peak_count > best_count:
            best_count = peak_count
            best_song_id = song_id

    best_name = database.get_song_name(best_song_id) if best_song_id is not None else None

    return best_name, best_count, all_scores


def record_and_recognize(database, duration=5, sample_rate=SAMPLE_RATE):
    import sounddevice as sd

    print(f"Recording {duration} seconds...")
    audio = sd.rec(
        int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype="float64"
    )
    sd.wait()

    audio = audio.flatten()
    audio = highpass_filter(audio, cutoff=200, sample_rate=sample_rate)

    print("Recording complete. Matching...")

    best_name, best_score, all_scores = recognize(audio, sample_rate, database)

    if best_name:
        print(f"Match: {best_name} (score: {best_score})")
    else:
        print("No match found.")

    if all_scores:
        print("All scores:")
        for name, score in sorted(all_scores.items(), key=lambda x: -x[1]):
            print(f"  {name}: {score}")

    return best_name, best_score, all_scores