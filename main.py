import json
from pathlib import Path
from f2m import face_to_music
from emo import emotion_to_music
from create_csd import create_csd
from create_score import create_score, resize_score

#import emo

# 1. get json data
with open('./User/example/test.json', 'r') as f:
    json_data = json.load(f)

    user_data = json_data['User']
    option_data = json_data['User']['Option']
    path_data = json_data['User']['Result']

# 2. set input_path & output_path
img_path = './User/' + user_data['ID'] + '/Image/' + user_data['Selected_Image']
score_path = './User/' + user_data['ID'] + path_data['Score_path']
wave_path = './User/' + user_data['ID'] + path_data['Wave_path']
csd_path = './User/' + user_data['ID'] + path_data['Csd_path']

# 3. program & option check
music_program = option_data['Program']


# parameter
num_bpm = option_data['Bpm']
num_bar = option_data['Bar']
num_note = option_data['Note']
num_octave = option_data['Octave']
harmony_on = option_data['Harmony']
detected_emo = option_data['Predicted_Emotion']

# 4-1. set output name
output_name = user_data["ID"] + Path(user_data["Selected_Image"]).stem + music_program + num_bpm + num_bar + num_note + num_octave + harmony_on
org_wav = wave_path + output_name + '.wav'
csd_wav = wave_path + output_name + 'csd.wav'
#score_png = score_path + output_name + '.png'

# 5-1. Run program
diff_divided, scale_org = face_to_music(img_path, org_wav)

# 6-1. f2m Create Score   ## error발생 시, lilypond 경로 확인 (Img 미생성시 resize error)
if music_program == 'F2M':

    # 6-2. Create Csd
    create_csd('./fin.csd', scale_org, diff_divided, csd_path + output_name + '.csd', csd_wav)

    try: 
        create_score(num_note, diff_divided, scale_org, score_path, output_name)
    except:
        pass
    resize_score(score_path, output_name)

    print("!!COMPLETE!!")   

# 7-1. emo Create Score
elif music_program == 'EMO':

    emotion_to_music(detected_emo, num_note, diff_divided, scale_org)



# 8. set json output
#with open('./User/example/test.json', 'r') as f:
#    json_update = json.load(f)
#    json_update['User']['Result']['Output_name'] = output_name
