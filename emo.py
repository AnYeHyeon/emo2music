import re
from music21 import *

def emotion_to_music(num_note, diff_divided, scale):

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

    
    # 2. 악기 할당
    instrument_musicnote = assigning_instrument(music_note)
    score = instrument_musicnote

    # 3. BPM 결정


    # 4. 








    # # Tinynotation을 사용하여 음악 부분(part) 생성
    # part = converter.parse("tinynotation: " + music_note)

    # # 스코어 생성 및 음악 부분 추가
    # score = stream.Score()
    # score.append(part)

    # 스코어 표시 (이 부분은 음악 악보로 결과를 시각화하기 위한 것입니다)
    score.show()
    print('Hello World!')


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