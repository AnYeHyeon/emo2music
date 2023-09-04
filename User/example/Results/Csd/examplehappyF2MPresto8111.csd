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
 
 giMidiKeys[] fillarray 71, 70, 61, 65, 68, 60, 60, 70
 giDurations[] fillarray 1, 1, 1, 1, 1, 1, 1, 1
 iIndex = 0 
 iStart = 0
 while iIndex < lenarray(giMidiKeys) do
  schedule "Play", iStart, giDurations[iIndex], giMidiKeys[iIndex]
  iStart += giDurations[iIndex]
  iIndex += 1
 od

endin


instr LetPlay1

 iMidiKeys[] fillarray 71, 70, 61, 65, 68, 60, 60, 70
 iDurations[] fillarray 1, 1, 1, 1, 1, 1, 1, 1
 iIndex = 0
 iStart = 0
 while iIndex < lenarray(iMidiKeys) do
  schedule "Play", iStart, iDurations[iIndex]*4/2, iMidiKeys[iIndex]
  iStart += iDurations[iIndex]
  iIndex += 1
 od

endin


instr LetPlay2

 iMidiKeys[] fillarray 71, 70, 61, 65, 68, 60, 60, 70
 iDurations[] fillarray 1, 1, 1, 1, 1, 1, 1, 1
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