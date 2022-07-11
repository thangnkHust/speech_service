from email.mime import audio
from pyannote.core import Segment
from pyannote.audio import Pipeline
from src.utils.waveform import audio_load

pipeline = Pipeline.from_pretrained('src/core/speaker_diarization/speaker_diarization/config.yaml')

def speaker_diarization(input_file, start_time, end_time):
    excerpt = Segment(start=start_time, end=end_time)
    waveform, sample_rate = audio_load.crop(input_file, excerpt)
    diarization = pipeline({"waveform": waveform, "sample_rate": sample_rate})
    diarization_json = diarization.for_json()['content']
    for item in diarization_json:
        item['speaker'] = item.pop('label')
        item.pop('track')
        item['segment']['start'] += start_time
        item['segment']['end'] += start_time
        item['segment']['start'] = round(item['segment']['start'], 2)
        item['segment']['end'] = round(item['segment']['end'], 2)
    return diarization_json

def speaker_identification(input_file, start_time, end_time, speaker_name_fake):
    excerpt = Segment(start=start_time, end=end_time)
    waveform, sample_rate = audio_load.crop(input_file, excerpt)
    switcher = {
        'SPEAKER_00': {
            'name': 'A',
            'reliability_speaker': 0.8
        },
        'SPEAKER_01': {
            'name': 'B',
            'reliability_speaker': 0.7
        },
        'SPEAKER_02': {
            'name': 'C',
            'reliability_speaker': 0.85
        },
        'SPEAKER_03': {
            'name': 'D',
            'reliability_speaker': 0.8
        },
        'SPEAKER_04': {
            'name': 'E',
            'reliability_speaker': 0.8
        },
        'SPEAKER_05': {
            'name': 'F',
            'reliability_speaker': 0.8
        }
    }
    return switcher.get(speaker_name_fake, {'name': 'unknown', 'reliability_speaker': None})


if __name__ == "__main__":
    input_file = "./audio.wav"
    result = speaker_diarization(input_file, 0, 5)
    print(result)
