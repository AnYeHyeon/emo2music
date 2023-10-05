import random
from music21 import *

# 감정에 따른 키 정보
emotion_to_keys = {
    'Happy': ["F# Minor", "D Major", "F Major"],
    'Disgust': ["C Major", "C Minor"],
    'Fear': ["C Major", "Bb Minor", "G Minor"],
    'Angry': ["F# Minor", "F Minor"],
    'Sad': ["C# Major", "Bb Major"],
    'Surprise': ["G Major", "F Major"],
    'Neutral': ["C# Major", "E Major"]
}

def get_chord_for_note_and_key(note_name, key_name):
    major_chords = {
        'C': ['C', 'E', 'G'],
        'D': ['D', 'F#', 'A'],
        'E': ['E', 'G#', 'B'],
        'F': ['F', 'A', 'C'],
        'G': ['G', 'B', 'D'],
        'A': ['A', 'C#', 'E'],
        'B': ['B', 'D#', 'F#']
    }

    minor_chords = {
        'C': ['C', 'Eb', 'G'],
        'D': ['D', 'F', 'A'],
        'E': ['E', 'G', 'B'],
        'F': ['F', 'Ab', 'C'],
        'G': ['G', 'Bb', 'D'],
        'A': ['A', 'C', 'E'],
        'B': ['B', 'D', 'F#']
    }

    root = note_name[0].upper()  # get the root of the note
    if "Major" in key_name:
        return major_chords[root]
    else:
        return minor_chords[root]

def extend_melody_with_key_chord(tinynotation_str, emotion):
    s = stream.Score()
    p = stream.Part()
    m = stream.Measure()
    m.append(tempo.MetronomeMark(number=60))  # 60 BPM
    p.append(m)

    # 감정에 해당하는 키 목록에서 무작위로 키 선택
    chosen_key = random.choice(emotion_to_keys[emotion])

    # "2/4" (박자 표시)를 제외하고 음표만 분할
    notes_only = tinynotation_str.split()[1:]

    for n in notes_only:
        m = stream.Measure()
        
        # Create chord based on the melody note and the chosen key
        c_notes = get_chord_for_note_and_key(n, chosen_key)
        
        c = chord.Chord(c_notes)
        m.append(c)
        p.append(m)

    s.insert(0, metadata.Metadata())
    s.metadata.title = f"Extended Melody with {chosen_key} Chord Based on {emotion}"
    s.append(p)
    return s

# 주어진 멜로디
tinynotation_string = "2/4 b4 b4 b2 a#2 g#2 d#2 a#4 f#4 f#2 a4 c4"

# 'Happy' 감정에 대해 확장된 멜로디 생성
extended_score = extend_melody_with_key_chord(tinynotation_string, 'Happy')

# 악보 표시
extended_score.show()

