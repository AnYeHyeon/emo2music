import numpy as np
from pprint import pprint
from scipy.io.wavfile import write
import json
import cv2

def get_json_f2m_param():
    with open('./User/example/test.json', 'r') as f:

        json_data = json.load(f)
        option_data = json_data['User']['Option']

        # face_to_music parameter
        num_bpm = option_data['Bpm']
        num_bar = option_data['Bar']
        num_note = option_data['Note']
        num_octave = option_data['Octave']
        harmony_on = option_data['Harmony']
        #tune_on = option_data['Tuned']

    return num_bpm, int(num_bar), int(num_note), int(num_octave), int(harmony_on) #, int(tune_on)

def get_note_length(val_note, num_bar, num_note):
    diff = np.zeros([num_note * num_bar], dtype='int64')

    for i in range(0, num_note * num_bar):
        diff[i] = abs(val_note[i+1] - val_note[i])

    sum_bar = np.zeros([num_bar], dtype='int64')
    avg_bar = np.zeros([num_bar], dtype='int64')

    for i in range(0, num_note * num_bar):
        sum_bar[int(i / num_note)] += diff[i]

    for i in range(0, num_bar):  ## 평균 픽셀 차이값
        avg_bar[i] = sum_bar[i] / num_note

    diff_divided = np.zeros([num_note * num_bar], dtype='float64')

    for i in range(0, num_bar * num_note):
        diff_divided[i] = np.around(diff[i] / avg_bar[int(i / num_note)])
    
    return diff_divided

def get_scale(num_octave, strandardized_val_Y, num_bar, num_note):
    octave1_scale={0.: 'C4', 1.: 'c4', 2.: 'D4', 3.: 'd4', 4.: 'E4', 5.: 'F4', 6.: 'f4', 7.: 'G4', 8.: 'g4', 9.: 'A4', 10.: 'a4', 11.: 'B4', 12.: 'B4'}

    octave2_scale={0.: 'C4', 1.: 'c4', 2.: 'D4', 3.: 'd4', 4.: 'E4', 5.: 'F4', 6.: 'f4', 7.: 'G4', 8.: 'g4', 9.: 'A4', 10.: 'a4', 11.: 'B4', 12.: 'C5', 
                13.: 'c5', 14.: 'D5', 15.: 'd5', 16.: 'E5', 17.: 'F5', 18.: 'f5', 19.: 'G5', 20.: 'g5', 21.: 'A5', 22.: 'a5', 23.: 'B5', 24.: 'B5'}

    octave3_scale={0.: 'C4', 1.: 'c4', 2.: 'D4', 3.: 'd4', 4.: 'E4', 5.: 'F4', 6.: 'f4', 7.: 'G4', 8.: 'g4', 9.: 'A4', 10.: 'a4', 11.: 'B4', 12.: 'C5', 
                13.: 'c5', 14.: 'D5', 15.: 'd5', 16.: 'E5', 17.: 'F5', 18.: 'f5', 19.: 'G5', 20.: 'g5', 21.: 'A5', 22.: 'a5', 23.: 'B5', 24.: 'C6',
                25.: 'c6', 26.: 'D6', 27.: 'd6', 28.: 'E6', 29.: 'F6', 30.: 'f6', 31.: 'G6', 32.: 'g6', 33.: 'A6', 34.: 'a6', 35.: 'B6', 36.: 'B6'}

    scale=[]
    if num_octave==1:
        for i in range(0, num_bar * num_note):
            scale.append(octave1_scale[strandardized_val_Y[i]])
    elif num_octave==2:
        for i in range(0, num_bar * num_note):
            scale.append(octave2_scale[strandardized_val_Y[i]])
    elif num_octave==3:
        for i in range(0, num_bar * num_note):
            scale.append(octave3_scale[strandardized_val_Y[i]])
    return scale

def get_piano_notes():
    octave = ['C4', 'c4', 'D4', 'd4', 'E4', 'F4', 'f4', 'G4', 'g4', 'A4', 'a4', 'B4',
              'C5', 'c5', 'D5', 'd5', 'E5', 'F5', 'f5', 'G5', 'g5', 'A5', 'a5', 'B5',
              'C6', 'c6', 'D6', 'd6', 'E6', 'F6', 'f6', 'G6', 'g6', 'A6', 'a6','B6',
              'C7', 'c7', 'D7', 'd7', 'E7', 'F7', 'f7', 'G7', 'g7', 'A7', 'a7','B7']  # Upper-White, lower-black keys

    base_freq = 261.63  # Frequency of Note C4

    note_freqs = {octave[i] : base_freq * pow(2, (i / 12)) for i in range(len(octave))}  # 각 음계에 (주파수)값을 할당
    #print('note_freqs', note_freqs)

    note_freqs[''] = 0.0  # silent note

    return note_freqs

def get_wave(freq, sample_rate=44100, duration = float):

    amplitude = 4096
    t = np.linspace(0, duration, int(sample_rate * duration))  # 0부터 duration까지 균일간격으로 sample_rate*duration 개 생성
    wave = amplitude * np.sin(2 * np.pi * freq * t)

    return wave

def get_song_data(music_notes, num_bpm):
    note_freqs = get_piano_notes()
    music_notes = music_notes.replace('-------', '-')
    # print(music_notes)
    song = [get_wave(note_freqs[note], duration=num_bpm) for note in music_notes.split('-')]
    song = np.concatenate(song)
    return song

def face_to_music(input_image_path, output_wave_path):    
    # 마디 수와 한 마디 안의 음표 수
    num_bpm, num_bar, num_note, num_octave, harmony_on = get_json_f2m_param()
    
    bpm_dic = {'Grave': 1.5, 'Largo': 1.2, 'Adagio': 1,
            'Andante': 0.857, 'Andantino': 0.75, 'Moderato': 0.667, 
            'Allegretto': 0.545, 'Allegro': 0.462, 'Vivace': 0.4,
            'Presto': 0.353}
    num_bpm = bpm_dic[num_bpm]

    # sample_rate 설정
    sample_rate = 44100

    img = cv2.imread(input_image_path)
    height, width, channel = img.shape
    
    # 한 음표 안에 들어있는 픽셀 컬럼 수
    # 각 컬럼의 모든 픽셀 RGB값의 곱의 합 도출
    one_step_size = int(width / (num_bar * num_note+1))
    
    # 음표 픽셀값의 합 배열
    val_note=[]
    val_note = [0 for i in range(0, num_bar * num_note+1)]

    # Y값 도출 및 할당
    val_Y = np.zeros([num_note * num_bar+1], dtype='float64')
    
    for i in range(0, num_bar * num_note+1):
        for x in range(one_step_size * i, one_step_size * (i + 1)):
            for y in range(0, height):
                b = str(img[y, x, 0])
                g = str(img[y, x, 1])
                r = str(img[y, x, 2])

                b = int(b)
                g = int(g)
                r = int(r)

                val_note[i] += b * g * r
                val_Y[i] = 0.2125 * r + 0.7154 * g + 0.0721 * b

    # 음표 별 박자 배열
    diff_divided = get_note_length(val_note, num_bar, num_note)

    # YUV를 활용한 음계 설정
    max_Y = max(val_Y)
    min_Y = min(val_Y)

    # 음계 할당 기준 도출
    unit_val_Y = (max_Y - min_Y) / (12 * num_octave)

    #val_Y 표준화
    strandardized_val_Y = (val_Y-min_Y)//unit_val_Y
    
    # 각 음표의 Y값에 따라 음계 기준에 기반하여 음계 설정
    scale = get_scale(num_octave, strandardized_val_Y, num_bar, num_note)
    
    # 음표 별 음계 할당
    bar_sum = 0
    num_real_bar = 0
    music_notes = ''
    
    for i in range(0, num_bar * num_note):
        if diff_divided[i] != 0:
            if (i < num_note * num_bar) and (bar_sum + diff_divided[i] <= num_note):
                # print('박자:', diff_divided[i], '음계:', scale[i])

                for k in range(int(diff_divided[i])):
                    music_notes += scale[i]
                    music_notes += '-'

                bar_sum += diff_divided[i]

                for j in range(i + 1, num_bar * num_note):
                    if diff_divided[j] != 0:
                        next_nonzero_index = j
                        break

                if bar_sum == num_note or (
                        (i < num_note * num_bar - 1) and (bar_sum + diff_divided[next_nonzero_index] > num_note)):
                    num_real_bar += 1
                    # print('bar_sum:', bar_sum, ',', num_real_bar, '번째 마디 완료')
                    # print('=======================================================')

                    bar_sum = 0

    # 박자 고려한 음계 출력 (원음)
    only_code_name =[scale[i] for i in range(0, num_bar * num_note) if diff_divided[i] != 0 ]

    data = get_song_data(music_notes, num_bpm)
    # print(music_notes)
    data = data * (16300 / np.max(data))  # optional
    write(output_wave_path, sample_rate, data.astype(np.int16))

    return diff_divided, scale