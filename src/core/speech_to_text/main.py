import torch
from dataclasses import dataclass
from pyannote.core import Segment
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2FeatureExtractor, Wav2Vec2CTCTokenizer
from src.utils.waveform import audio_load

class SpeechToTextModel:
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu").type
    folder_model = 'src/core/speech_to_text/pretrain915_finetune2'
    __tokenizer = Wav2Vec2CTCTokenizer(folder_model + "/vocab.json", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
    __feature_extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=16000, padding_value=0.0, do_normalize=True, return_attention_mask=True)
    __processor = Wav2Vec2Processor(feature_extractor=__feature_extractor, tokenizer=__tokenizer)
    __model = Wav2Vec2ForCTC.from_pretrained(
                    folder_model,
                    attention_dropout=0.1,
                    hidden_dropout=0.1,
                    feat_proj_dropout=0.1,
                    final_dropout=0.1,
                    mask_time_prob=0.05,
                    layerdrop=0.1,
                    # gradient_checkpointing=True,
                    ctc_loss_reduction="mean",
                    ctc_zero_infinity=True,
                    pad_token_id=__processor.tokenizer.pad_token_id,
                    vocab_size=len(__processor.tokenizer)
                ).to(device)

    @staticmethod
    def __get_trellis(emission, tokens, blank_id=0):
        num_frame = emission.size(0)
        num_tokens = len(tokens)

        # Trellis has extra diemsions for both time axis and tokens.
        # The extra dim for tokens represents <SoS> (start-of-sentence)
        # The extra dim for time axis is for simplification of the code.
        trellis = torch.full((num_frame+1, num_tokens+1), -float('inf'))
        trellis[:, 0] = 0
        for t in range(num_frame):
            trellis[t+1, 1:] = torch.maximum(
                # Score for staying at the same token
                trellis[t, 1:] + emission[t, blank_id],
                # Score for changing to the next token
                trellis[t, :-1] + emission[t, tokens],
            )
        return trellis

    @dataclass
    class Point:
        token_index: int
        time_index: int
        score: float

    @staticmethod
    def __backtrack(trellis, emission, tokens, blank_id=0):
        # Note:
        # j and t are indices for trellis, which has extra dimensions
        # for time and tokens at the beginning.
        # When refering to time frame index `T` in trellis,
        # the corresponding index in emission is `T-1`.
        # Similarly, when refering to token index `J` in trellis,
        # the corresponding index in transcript is `J-1`.
        j = trellis.size(1) - 1
        t_start = torch.argmax(trellis[:, j]).item()

        path = []
        for t in range(t_start, 0, -1):
            # 1. Figure out if the current position was stay or change
            # Note (again):
            # `emission[J-1]` is the emission at time frame `J` of trellis dimension.
            # Score for token staying the same from time frame J-1 to T.
            stayed = trellis[t-1, j] + emission[t-1, blank_id]
            # Score for token changing from C-1 at T-1 to J at T.
            changed = trellis[t-1, j-1] + emission[t-1, tokens[j-1]]

            # 2. Store the path with frame-wise probability.
            prob = emission[t-1, tokens[j-1]
                            if changed > stayed else 0].exp().item()
            # Return token index and time index in non-trellis coordinate.
            path.append(SpeechToTextModel.Point(j-1, t-1, prob))

            # 3. Update the token
            if changed > stayed:
                j -= 1
                if j == 0:
                    break
        else:
            raise ValueError('Failed to align')
        return path[::-1]


    @dataclass
    class SegmentTest:
        label: str
        start: int
        end: int
        score: float
        start_time: float = None
        end_time: float = None

        def __repr__(self):
            return f"{self.label}\t({self.score:4.4f}): [{self.start:5d}, {self.end:5d})\t[{self.start_time:4.4f}, {self.end_time:4.4f})"

        def serialize(self):
            return {
                'start_time': round(self.start_time, 2),
                'end_time': round(self.end_time, 2),
                'text': self.label,
                'reliability_text': round(self.score, 4)
            }

        @property
        def length(self):
            return self.end - self.start

    @staticmethod
    def __merge_repeats(path, output):
        segments = []
        for item in output.char_offsets[0]:
            i1 = item['start_offset']
            i2 = item['end_offset']
            score = sum(point.score for point in path[i1:i2]) / (i2 - i1)
            segments.append(SpeechToTextModel.SegmentTest(
                item['char'], path[i1].time_index, path[i2-1].time_index + 1, score))
        return segments

    @staticmethod
    def __merge_words(segments, time_per_offset, start_time, separator=' '):
        words = []
        words_default = []
        i1, i2 = 0, 0
        while i1 < len(segments):
            if i2 >= len(segments) or segments[i2].label == separator:
                if i1 != i2:
                    segs = segments[i1:i2]
                    word = ''.join([seg.label for seg in segs])
                    score = sum(seg.score * seg.length for seg in segs) / sum(seg.length for seg in segs)
                    words.append(SpeechToTextModel.SegmentTest(word, segments[i1].start, segments[i2-1].end, score, segments[i1].start * time_per_offset + start_time, segments[i2-1].end*time_per_offset + start_time).serialize())
                    words_default.append(SpeechToTextModel.SegmentTest(word, segments[i1].start, segments[i2-1].end, score, segments[i1].start*time_per_offset + start_time, segments[i2-1].end*time_per_offset + start_time))
                i1 = i2 + 1
                i2 = i1
            else:
                i2 += 1
        if sum(seg.length for seg in words_default) != 0:
            score_segment = round(sum(seg.score * seg.length for seg in words_default) / sum(seg.length for seg in words_default), 4)
        else:
            score_segment = 0
        return words, score_segment

    @staticmethod
    def speech_to_text(input_file, start_time, end_time):
        excerpt = Segment(start=start_time, end=end_time)
        waveform, sample_rate = audio_load.crop(input_file, excerpt)
        inputs = SpeechToTextModel.__processor(waveform.squeeze().numpy(), sampling_rate=sample_rate, return_tensors="pt", padding=True)
        with torch.no_grad():
            logits = SpeechToTextModel.__model(inputs.input_values.to(SpeechToTextModel.device)).logits
        pred_ids = torch.argmax(logits, dim=-1)
        scores = torch.nn.functional.log_softmax(logits, dim=-1)

        output = SpeechToTextModel.__processor.batch_decode(
            pred_ids, output_word_offsets=True, output_char_offsets=True)
        transcript = output.text[0]

        emission = scores[0].cpu().detach()
        tokens = pred_ids.cpu().detach().squeeze().numpy()

        trellis = SpeechToTextModel.__get_trellis(emission, tokens)
        path = SpeechToTextModel.__backtrack(trellis, emission, tokens)

        segments = SpeechToTextModel.__merge_repeats(path, output)
        time_per_offset = (end_time - start_time)/len(pred_ids[0])
        word_segments, reliability_transcript = SpeechToTextModel.__merge_words(segments, time_per_offset, start_time)

        return transcript, reliability_transcript, word_segments


if __name__ == "__main__":
    input_file = ".docker/data/audio_sample/5/Fof5G4u6EmiJRI-xwWSoK.wav"
    transcript, reliability_transcript, word_segments = SpeechToTextModel.speech_to_text(input_file, 0, 1)
    print(transcript)
    for item in word_segments:
        print(item)
    # print(transcript, reliability_transcript, word_segments)
