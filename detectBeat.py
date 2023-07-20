import essentia.standard as es
from tempfile import TemporaryDirectory
import IPython
from pylab import plot, show, figure, imshow
import matplotlib.pyplot as plt

# Loading an audio file.
audio = es.MonoLoader(filename='../../../test/audio/recorded/dubstep.flac')()

# Compute beat positions and BPM.
rhythm_extractor = es.RhythmExtractor2013(method="multifeature")
bpm, beats, beats_confidence, _, beats_intervals = rhythm_extractor(audio)

print("BPM:", bpm)
print("Beat positions (sec.):", beats)
print("Beat estimation confidence:", beats_confidence)

# Mark beat positions in the audio and write it to a file.
# Use beeps instead of white noise to mark them, as it is more distinctive.
marker = es.AudioOnsetsMarker(onsets=beats, type='beep')
marked_audio = marker(audio)

# Write to an audio file in a temporary directory.
temp_dir = TemporaryDirectory()
es.MonoWriter(filename=temp_dir.name + '/dubstep_beats.flac')(marked_audio)

IPython.display.Audio(temp_dir.name + '/dubstep_beats.flac')
plt.rcParams['figure.figsize'] = (15, 6)

plot(audio)
for beat in beats:
    plt.axvline(x=beat*44100, color='red')
plt.xlabel('Time (samples)')
plt.title("Audio waveform and the estimated beat positions")
show()