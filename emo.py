import re

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




    
    print('Hello World!')