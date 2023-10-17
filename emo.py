import re
import copy
from music21 import *

def emotion_to_music(emotion, num_note, diff_divided, scale):

    print('______________melody_______________')
    x_four_time = num_note + '/4'

    # diff_divided 데이터 정제
    diff_to_note = []
    diff_value = { 0.2:16 , 0.5:8 , 1:4 , 2:2 , 4:1 }
    for i in list(diff_divided):
        if i in diff_value.keys():
            diff_to_note.append(diff_value[i])
    # print(diff_to_note)

    # # scale 데이터 정제
    scale_to_note = []
    for byone in scale:
        note_box = []

        # scale to musesound4
        scale_only = re.findall('[a-zA-Z]', byone)
        if scale_only[0].isupper():
            scale_only = scale_only[0].lower()
            note_box.extend(scale_only)
        
        else:
            scale_only += '#'
            note_box.extend(scale_only)

        # octave to musesound4
        octave = re.findall('\d', byone)
        
        if octave[0] == '4':
            note_box.insert(1, '')
        if octave[0] == '5':
            note_box.insert(1, "'")
        if octave[0] == '6':
            note_box.insert(1, "''")

        scale_to_note.append("".join(note_box))
    # print(scale_to_note)       

    # diff + scale
    music_note = []
    for i in range(len(diff_to_note)):
        with_octave = scale_to_note[i] + str(diff_to_note[i])
        music_note.append(with_octave)

    music_note =  x_four_time + ' ' + ' '.join(music_note)
    # print(music_note)

    print(music_note)
    print('emotion: ' + emotion)

    # 1. 화성 쌓기, 2. BPM 할당
    score_with_chord = extend_melody_with_key_chord(music_note, emotion)
    # score_with_chord.show()
    
    # 3. 악기 할당
    score_with_instruments = assign_instruments_to_score(score_with_chord, emotion)
    # score_with_instruments.show()

    score_with_instruments.write('png', fp='./Score/score.png')


import random
from music21 import stream, note, chord, metadata, tempo

# 감정에 따른 음악 요소 정보
emotion_to_music_features = {
    'Happy': {
        "Key": ["D Major", "F Major"],
        "BPM": [138, 132, 150],
        "Octave": [[2], [3]],
        "Instruments": ["Piano", "Harpsichord", "Guitar"]
    },
    'Disgust': {
        "Key": ["C Major", "C Minor"],
        "BPM": [129, 125],
        "Octave": [[1]],
        "Instruments": ["Percussion (Marimba, Chimes)", "Harpsichord"]
    },
    'Fear': {
        "Key": ["C Major", "Bb Minor", "G Minor"],
        "BPM": [120, 90, 84],
        "Octave": [[2]],
        "Instruments": ["Drums", "Violin", "Piano", "Chimes", "Mezzo-soprano"]
    },
    'Angry': {
        "Key": ["F# Minor", "F Minor"],
        "BPM": [125, 120],
        "Octave": [ [2], [3]],
        "Instruments": ["Drums", "Cymbals", "Electric Piano", "Chimes", "Piano"]
    },
    'Sad': {
        "Key": ["C# Major", "Bb Minor"],
        "BPM": [125, 128],
        "Octave": [[1]],
        "Instruments": ["Cello", "Pipe Organ", "Piano", "Classical Guitar"]
    },
    'Surprise': {
        "Key": ["G Major", "F Major"],
        "BPM": [127, 196],
        "Octave": [[2, 3]],
        "Instruments": ["Electric Guitar", "Drums", "Bass Guitar"]
    },
    'Neutral': {
        "Key": ["C# Major", "E Major"],
        "BPM": [108, 75],
        "Octave": [[1, 2]],
        "Instruments": ["Flute", "Saxophone", "Harp", "Classical Guitar"]
    }
}

# 악기 이름과 music21 악기 클래스 매핑
instrument_mapping = {
    "Piano": instrument.Piano(),
    "Violin": instrument.Violin(),
    "Cello": instrument.Violoncello(),
    "Flute": instrument.Flute(),
    "Harpsichord": instrument.Harpsichord(),
    "Guitar": instrument.AcousticGuitar(),
    "Electric Guitar": instrument.ElectricGuitar(),
    "Drums": instrument.BassDrum(),
    "Cymbals": instrument.Cymbals(),
    "Saxophone": instrument.Saxophone(),
    "Percussion": instrument.Percussion(),
    "Electric Piano": instrument.ElectricPiano(),
    "Pipe Organ": instrument.PipeOrgan(),
    "Classical Guitar": instrument.AcousticGuitar(),
    "Bass Guitar": instrument.ElectricBass(),
    "Harp": instrument.Harp(),
    "Chimes": instrument.TubularBells(),
    "Mezzo-soprano": instrument.MezzoSoprano()
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

    BPM_list = emotion_to_music_features[emotion]['BPM']
    BPM = sum(BPM_list) / len(BPM_list)
    m.append(tempo.MetronomeMark(BPM))
    p.append(m)

    # 감정에 해당하는 키 목록에서 무작위로 키 선택
    chosen_key = random.choice(emotion_to_music_features[emotion]['Key'])

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

def assign_instruments_to_score(score, emotion):
    
    # 감정에 따라 선택된 악기 목록에서 두 개의 악기를 무작위로 선택
    chosen_instruments = random.sample(emotion_to_music_features[emotion]['Instruments'], 2)
    print(chosen_instruments)
    
    # 첫 번째 악기 객체를 가져온다.
    inst_obj1 = instrument_mapping[chosen_instruments[0]]
    
    # 두 번째 악기 객체를 가져온다.
    inst_obj2 = instrument_mapping[chosen_instruments[1]]

    # 첫 번째 파트에 첫 번째 악기 객체 추가
    score.parts[0].insert(0, inst_obj1)
    
    # 두 번째 파트 생성 및 두 번째 악기 객체 추가
    new_part = copy.deepcopy(score.parts[0])  # 기존 파트의 복사본을 생성
    new_part.clear()  # 새 파트의 내용을 지운다.
    new_part.insert(0, inst_obj2)  # 두 번째 악기 객체를 새 파트에 추가
    
    # 기존 파트의 노트들을 새 파트에 추가한다.
    for element in score.parts[0].elements:
        if not isinstance(element, instrument.Instrument):  # 악기 정보를 제외한 다른 요소들만 추가
            new_part.append(copy.deepcopy(element))
    
    score.append(new_part)  # 스코어에 새로운 파트를 추가

    return score
