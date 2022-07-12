from pyannote.core import Segment
from pyannote.audio import Pipeline
from src.utils.waveform import audio_load

class SpeakerDiarizationModel:
    __model = None
    @staticmethod
    def getModel():
        if SpeakerDiarizationModel.__model == None:
            SpeakerDiarizationModel()
        return SpeakerDiarizationModel.__model
    
    def __init__(self) -> None:
        if SpeakerDiarizationModel.__model == None:
            SpeakerDiarizationModel.__model = Pipeline.from_pretrained('src/core/speaker_diarization/speaker_diarization/config.yaml')
        else:
            SpeakerDiarizationModel.__model = self.__model


    @staticmethod
    def speaker_diarization(input_file, start_time, end_time):
        excerpt = Segment(start=start_time, end=end_time)
        waveform, sample_rate = audio_load.crop(input_file, excerpt)
        diarization = SpeakerDiarizationModel.__model({"waveform": waveform, "sample_rate": sample_rate})
        diarization_json = diarization.for_json()['content']

        for item in diarization_json:
            item['speaker'] = item.pop('label')
            item.pop('track')
            item['segment']['start'] += start_time
            item['segment']['end'] += start_time
            item['segment']['start'] = round(item['segment']['start'], 2)
            item['segment']['end'] = round(item['segment']['end'], 2)

        return diarization_json


if __name__ == "__main__":
    input_file = "./audio.wav"
    result = SpeakerDiarizationModel.speaker_diarization(input_file, 0, 3)
    print(result)
