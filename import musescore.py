from music21 import stream, note, tempo, instrument, converter

# Create a Stream (musical container)
instrument = instrument.ElectricGuitar()
song = stream.Stream()
song.append(instrument)

# Add a title
# song.metadata.title = "My Song"

# # Add a Part (e.g., for piano)
# part = stream.Part()
# part.insert(0, instrument.Piano())


# # Define notes and durations
# notes = [("C4", 4), ("D4", 4), ("E4", 4), ("F4", 4)]

note1 = note.Note("C4")
note2 = note.Note("F#4")
note3 = note.Note("B-2")

song.append(note1)
song.append(note2)
song.append(note3)

song.show()

# # Add notes to the Part
# for n, duration in notes:
#     part.append(note.Note(n, type=duration))

# # Add a tempo mark
# part.append(tempo.MetronomeMark(number=120))

# # Add the Part to the Song
# song.append(part)

# # Convert the song to MusicXML format
# musicxml = song.write('musicxml')

# # Save the MusicXML to a file
# with open('my_song.xml', 'w') as f:
#     f.write(musicxml)

# # You can also convert the MusicXML to a PDF using MuseScore or another tool
# converter.subConvert('my_song.xml', 'my_song.pdf')