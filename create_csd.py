import subprocess
import numpy as np

def create_csd(src_file, scale, diff_divided, csd_output, wav_output):
    def get_csound(scale, diff_divided):
        music = [ "C4", "c4", "D4", "d4", "E4", "F4", "f4", "G4", "g4", "A4", "a4", "B4", 
                "C5", "c5", "D5", "d5", "E5", "F5", "f5", "G5", "g5", "A5", "a5", "B5", 
                "C6", "c6", "D6", "d6", "E6", "F6", "f6", "G6", "g6", "A6", "a6", "B6", ""]
        replace_music = [ "60", "61", "62", "63", "64", "65", "66", "67", "68", "69", "70", "71", 
                        "72", "73", "74", "75", "76", "77", "78", "79", "80", "81", "82", "83", 
                        "84", "85", "86", "87", "88", "89", "90", "91", "92", "93", "94", "95", "0"]

        py2csd = {}
        for i in range(len(music)):
            py2csd[music[i]] = replace_music[i]

        # csound scale value
        csound_scale = [int(py2csd[scale[i]]) for i in range(len(scale))]

        midiKey=''
        duration=''

        for i in range(len(csound_scale)):
            if diff_divided[i] == 0:
                continue
            else:
                if i == int(len(csound_scale)) - 1:
                    midiKey = midiKey + str(csound_scale[i])
                    duration = duration + str(int(diff_divided[i]))
                else:
                    midiKey = midiKey + str(csound_scale[i]) + ', '
                    duration = duration + str(int(diff_divided[i])) + ', '
        
        if midiKey[-2] == ',':
            midiKey = midiKey[:-2]
            duration = duration[:-2]

        return midiKey, duration

    midiKey, duration = get_csound(scale, diff_divided)

    strOrc = ""
    isMidiMode = False
    isDurationMode = False

    f = open(src_file, 'r')
    while True:
        line=f.readline()
        if not line: break

        if (isMidiMode == True):
            if (line.endswith(",")):
                continue
            else:
                isMidiMode = False
                continue

        if (line.find("iMidiKeys[]") >= 0):
            isMidiMode = True
            tokens=line.split()
            line = " " + tokens[0] + " " + tokens[1] + " " + midiKey + "\n"

        if (isDurationMode == True):
            if (line.endswith(",")):
                continue
            else:
                isDurationMode = False
                continue

        if (line.find("iDurations[]") >= 0):
            isDurationMode = True
            tokens=line.split()
            line = " " + tokens[0] + " " + tokens[1] + " " + duration + "\n"
        
        strOrc += line
    f.close()

    f = open(csd_output, 'w')
    f.write(strOrc)
    f.close()

    # Csound Compiler Run, (csd line 77, 87 error)
    subprocess.run(["csound", "-o", wav_output, csd_output])

    #return strOrc