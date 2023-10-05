import re
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

    # 1. 화성 쌓기
    score_with_chord = extend_melody_with_key_chord(music_note, emotion)
    score_with_chord.show()
    
    # 2. 악기 할당
    # instrument_musicnote = assigning_instrument(score_with_chord)
    # score = instrument_musicnote

    # 3. BPM 결정


    # 4. 








    # # Tinynotation을 사용하여 음악 부분(part) 생성
    # part = converter.parse("tinynotation: " + music_note)

    # # 스코어 생성 및 음악 부분 추가
    # score = stream.Score()
    # score.append(part)

    # 스코어 표시 (이 부분은 음악 악보로 결과를 시각화하기 위한 것입니다)
    # score.show()
    print('Hello World!')

import random
from music21 import stream, note, chord, metadata, tempo

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

# 주어진 감정에 따라 무작위로 키를 선택하고 해당 키의 화성을 멜로디에 추가하는 함수
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

        # Add melody note
        melody_note = note.Note(n)
        
        # Create chord based on the melody note and the chosen key
        if "Major" in chosen_key:
            c_notes = [melody_note.nameWithOctave, 
                       note.Note(melody_note.pitch.transpose('M3')).nameWithOctave,
                       note.Note(melody_note.pitch.transpose('P5')).nameWithOctave]
        else:  # Minor chord
            c_notes = [melody_note.nameWithOctave, 
                       note.Note(melody_note.pitch.transpose('m3')).nameWithOctave,
                       note.Note(melody_note.pitch.transpose('P5')).nameWithOctave]
        
        c = chord.Chord(c_notes)
        m.append(c)
        p.append(m)

    s.insert(0, metadata.Metadata())
    s.metadata.title = f"Extended Melody with {chosen_key} Chord Based on {emotion}"
    s.append(p)
    return s




def assigning_instrument(music_note):
    # 스코어 생성
    score = stream.Score()

    # 피아노 파트
    pianoPart = converter.parse("tinynotation: " + music_note)
    piano = instrument.Piano()
    pianoPart.insert(0, piano)
    score.append(pianoPart)

    # 기타 파트
    guitarPart = converter.parse("tinynotation: " + music_note)
    guitar = instrument.AcousticGuitar()
    guitarPart.insert(0, guitar)
    score.append(guitarPart)

    # 첼로 파트
    celloPart = converter.parse("tinynotation: " + music_note)
    cello = instrument.Violoncello()
    celloPart.insert(0, cello)
    score.append(celloPart)

    return score