import torch
import torchaudio
from transformers import Wav2Vec2Processor, Wav2Vec2ForCTC, Wav2Vec2FeatureExtractor, Wav2Vec2CTCTokenizer
import librosa

def speech_to_text():
    tokenizer = Wav2Vec2CTCTokenizer("src/utils/speech_to_text/pretrain915_finetune2/vocab.json", unk_token="[UNK]", pad_token="[PAD]", word_delimiter_token="|")
    feature_extractor = Wav2Vec2FeatureExtractor(feature_size=1, sampling_rate=16000, padding_value=0.0, do_normalize=True, return_attention_mask=True)
    processor = Wav2Vec2Processor(feature_extractor=feature_extractor, tokenizer=tokenizer)
    model = Wav2Vec2ForCTC.from_pretrained(
        "src/utils/speech_to_text/pretrain915_finetune2",
        attention_dropout=0.1,
        hidden_dropout=0.1,
        feat_proj_dropout=0.1,
        final_dropout=0.1,
        mask_time_prob=0.05,
        layerdrop=0.1,
        # gradient_checkpointing=True,
        ctc_loss_reduction="mean",
        ctc_zero_infinity=True,
        pad_token_id=processor.tokenizer.pad_token_id,
        vocab_size=len(processor.tokenizer)
    )

    # audio_waveform, sample_rate = torchaudio.load('.docker/data/record/J3C1WESvQKwP5nnicB-Mk.wav')
    audio_waveform, sample_rate = librosa.load('.docker/data/record/_5K9_3Wi6i_0.wav')

    inputs = processor(audio_waveform, sampling_rate=sample_rate, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(inputs.input_values).logits
    pred_ids = torch.argmax(logits, dim=-1)

    output = processor.batch_decode(pred_ids, output_word_offsets=False, output_char_offsets=False)
    print(output)
    return output[0]
if __name__ == '__main__':
    speech_to_text()
