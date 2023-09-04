<CsoundSynthesizer>
<CsOptions>
-o dac -m128 -+rtaudio=mme -B512 
;-o sample00.wav -W -f 
</CsOptions>
<CsInstruments>

sr = 44100
ksmps = 32
nchnls = 2
0dbfs = 3
A4 = 457

;massign 0, 1; assigns all midi channels to instr 1


instr LetPlay
 
 giMidiKeys[] fillarray 70, 71, 71, 70, 70, 70, 70, 70, 69, 71, 70, 70, 71, 71, 71, 70, 70, 71, 69, 69, 70, 70, 70, 70, 69, 69, 69, 69, 68, 67, 66, 65, 65, 63, 63, 64, 70, 71, 70, 71, 70, 68, 65, 64, 66, 66, 66, 66, 66, 65, 65, 66, 65, 65, 65, 64, 63, 70, 69, 67, 66, 64, 62, 61, 60, 60, 60, 61, 61, 62, 62, 62, 61, 60, 60, 60, 60, 60, 60, 60, 60, 60, 61, 60, 60, 60, 62, 64, 65, 68, 70, 70, 70, 69
 giDurations[] fillarray 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3, 2, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1
 iIndex = 0 
 iStart = 0
 while iIndex < lenarray(giMidiKeys) do
  schedule "Play", iStart, giDurations[iIndex], giMidiKeys[iIndex]
  iStart += giDurations[iIndex]
  iIndex += 1
 od

endin


instr LetPlay1

 iMidiKeys[] fillarray 70, 71, 71, 70, 70, 70, 70, 70, 69, 71, 70, 70, 71, 71, 71, 70, 70, 71, 69, 69, 70, 70, 70, 70, 69, 69, 69, 69, 68, 67, 66, 65, 65, 63, 63, 64, 70, 71, 70, 71, 70, 68, 65, 64, 66, 66, 66, 66, 66, 65, 65, 66, 65, 65, 65, 64, 63, 70, 69, 67, 66, 64, 62, 61, 60, 60, 60, 61, 61, 62, 62, 62, 61, 60, 60, 60, 60, 60, 60, 60, 60, 60, 61, 60, 60, 60, 62, 64, 65, 68, 70, 70, 70, 69
 iDurations[] fillarray 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3, 2, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1
 iIndex = 0
 iStart = 0
 while iIndex < lenarray(iMidiKeys) do
  schedule "Play", iStart, iDurations[iIndex]*4/2, iMidiKeys[iIndex]
  iStart += iDurations[iIndex]
  iIndex += 1
 od

endin


instr LetPlay2

 iMidiKeys[] fillarray 70, 71, 71, 70, 70, 70, 70, 70, 69, 71, 70, 70, 71, 71, 71, 70, 70, 71, 69, 69, 70, 70, 70, 70, 69, 69, 69, 69, 68, 67, 66, 65, 65, 63, 63, 64, 70, 71, 70, 71, 70, 68, 65, 64, 66, 66, 66, 66, 66, 65, 65, 66, 65, 65, 65, 64, 63, 70, 69, 67, 66, 64, 62, 61, 60, 60, 60, 61, 61, 62, 62, 62, 61, 60, 60, 60, 60, 60, 60, 60, 60, 60, 61, 60, 60, 60, 62, 64, 65, 68, 70, 70, 70, 69
 iDurations[] fillarray 1, 1, 1, 1, 1, 1, 2, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3, 2, 1, 3, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 3, 1, 3, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 2, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 4, 1, 1
 iIndex = 0
 iStart = 0
 while iIndex < lenarray(iMidiKeys) do
  schedule "Play", iStart, iDurations[iIndex]*4/2, iMidiKeys[iIndex]
  iStart += iDurations[iIndex]
  iIndex += 1
 od

endin






instr Play

 iMidiKey = p4
 ;iFreq mtof iMidiKey
 iFreq mtof iMidiKey
 S_name mton iMidiKey
 printf_i "Midi Note = %d, Frequency = %f, Note name = %s\n",
          3, iMidiKey, iFreq, S_name
 aPluck pluck .2, iFreq, iFreq, 0, 1
 aout linen aPluck, 0, p3, p3/2
 ;arnd randomi 400, 1000, 50
 ;asig poscil .7, arnd, 1
 
 a1, a2 pan2 aout, (iMidiKey-61)/10
      out a1, a2
	 ; fout "kyutest1.wav", 18, a1, a2 

endin

</CsInstruments>
<CsScore>
i "LetPlay" 0 1
i "LetPlay1" 0 1
i "LetPlay2" 0 1
;i "Letplay2" 1 2
</CsScore>
</CsoundSynthesizer>
;example by joachim heintz