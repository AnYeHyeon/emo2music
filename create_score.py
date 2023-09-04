import os
import re
from music21 import *
from PIL  import Image


def create_score(num_note, diff_divided, scale, score_path, output_name):
    print('악보 생성 중...')
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

    us = environment.UserSettings()
    us['musicxmlPath'] = "C:/Program Files/MuseScore4/bin/MuseScore4.exe"
    us['lilypondPath'] = "C:/Program Files/lilypond-2.24.1-mingw-x86_64/lilypond-2.24.1/bin/lilypond.exe"

    s = converter.parse(music_note, format='tinyNotation')
    s.write('lilypond.png', fp = score_path + output_name)

def resize_score(score_path, output_name):
    # print(score_path)
    index = 1
    images = []
    # print(os.listdir(score_path))
    for file in os.listdir(score_path):
        filename, extension = os.path.splitext(file)
        if extension == '.png' or 'page' in file:
            if 'page' in file:  # two or more images
                filename = file.split("-", 1)[0]
            else:
                filename = filename
            # print(filename, output_name)

            if filename == output_name:
                print('Image resizing...')
                image1 = Image.open(score_path + file)

                # cut image crop(left,up, rigth, down)
                right = 790
                down = 90
                croppedImage = image1.crop((0,0,right,down))

                # croppedImage.show()
                resize_file = filename + '_' +str(index) + '.png'
                png_path = score_path + resize_file
                croppedImage.save(png_path)
                images.append(croppedImage)
                index += 1
                
    # # Merge Imgs
    result_height = sum(img.height for img in images)
    result_width = 790
    result_score = Image.new("RGB", (result_width, result_height))
    y_offset = 0
    for img in images:
        result_score.paste(img, (0, y_offset))
        y_offset += img.size[1]

    result_score.save(score_path + output_name +'_1' + '.png')  # 결과 이미지 저장