from music21 import instrument

def assign_instruments_to_score(score, emotion):
    # 감정에 따라 선택된 악기 목록에서 무작위로 악기 선택
    chosen_instruments = random.choice(emotion_to_music_features[emotion]['Instruments'])
    
    # 각 악기에 대한 파트 생성 및 추가
    for inst_name in chosen_instruments:
        # music21의 instrument 모듈에서 악기 이름을 찾아 객체를 생성
        inst_obj = getattr(instrument, inst_name)() 
        # 파트에 악기 객체 추가
        score.parts[0].insert(0, inst_obj)
    
    return score

# 감정에 따른 음악 요소 정보
emotion_to_music_features = {
    'Happy': {
        "Key": ["F# Minor", "D Major", "F Major"],
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
        "Instruments": ["Drums", "Piano", "Electric Guitar", "Chimes", "Mezzo-soprano"]
    },
    'Angry': {
        "Key": ["F# Minor", "F Minor"],
        "BPM": [125, 120],
        "Octave": [ [2], [3]],
        "Instruments": ["Drums", "Electric Piano", "Chimes", "Piano"]
    },
    'Sad': {
        "Key": ["C# Major", "Bb Major"],
        "BPM": [125, 128],
        "Octave": [[1]],
        "Instruments": ["Male Vocal", "Pipe Organ", "Piano", "Classical Guitar"]
    },
    'Surprise': {
        "Key": ["G Major", "F Major"],
        "BPM": [127, 196],
        "Octave": [[2, 3]],
        "Instruments": ["Electric Guitar", "Exciting Drums", "Bass Guitar", "Female Vocal"]
    },
    'Neutral': {
        "Key": ["C# Major", "E Major"],
        "BPM": [108, 75],
        "Octave": [[1, 2]],
        "Instruments": ["Bass Guitar", "Harp", "Female Vocal", "Classical Guitar"]
    }
}

# 악기 이름과 music21 악기 클래스 매핑
instrument_mapping = {
    "Piano": instrument.Piano(),
    "Harpsichord": instrument.Harpsichord(),
    "Guitar": instrument.AcousticGuitar(),
    "Electric Guitar": instrument.ElectricGuitar(),
    "Drums": instrument.SnareDrum(),
    "Percussion": instrument.Percussion(),
    "Electric Piano": instrument.ElectricPiano(),
    "Pipe Organ": instrument.PipeOrgan(),
    "Classical Guitar": instrument.AcousticGuitar(),
    "Bass Guitar": instrument.ElectricBass(),
    "Harp": instrument.Harp(),
    "Male Vocal": instrument.Vocalist(),
    "Female Vocal": instrument.Vocalist(),
    "Chimes": instrument.TubularBells(),
    "Mezzo-soprano": instrument.MezzoSoprano()
}
# 사용 예시:
s = extend_melody_with_key_chord("2/4 b4 b4 b2 a#2 g#2 d#2 a#4 f#4 f#2 a4 c4", "Happy")
score_with_instruments = assign_instruments_to_score(s, "Happy")
score_with_instruments.show()

