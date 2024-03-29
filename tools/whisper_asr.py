"""
Used to transcribe all audio files in one folder into another folder.
e.g.
Directory structure:
--pre_data_root
----SP_1
------01.wav
------02.wav
------......
----SP_2
------01.wav
------02.wav
------......
Use 
python tools/whisper_asr.py --audio_dir pre_data_root/SP_1 --save_dir data/SP_1 
to transcribe the first speaker.

Use 
python tools/whisper_asr.py --audio_dir pre_data_root/SP_2 --save_dir data/SP_2 
to transcribe the second speaker.

Note: Be aware of your audio sample rate, which defaults to 44.1kHz.
"""
from pathlib import Path

import click
import librosa
import soundfile as sf
import whisper
from loguru import logger
from tqdm import tqdm

from fish_speech.utils.file import AUDIO_EXTENSIONS, list_files
from fish_speech.utils.logger_settings import api_logger

@click.command()
@click.option("--model-size", default="large", help="Size of the Whisper model")
@click.option("--audio-dir", required=True, help="Directory containing audio files")
@click.option(
    "--save-dir", required=True, help="Directory to save processed audio files"
)
@click.option(
    "--sample-rate",
    default=None,
    type=int,
    help="Output sample rate, default to input sample rate",
)
@click.option("--language", default="ZH", help="Language of the transcription")
def main(model_size, audio_dir, save_dir, sample_rate, language):
    api_logger.info("Loading / Downloading OpenAI Whisper model...")
    model = whisper.load_model(model_size)
    api_logger.info("Model loaded.")

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    audio_files = list_files(
        path=audio_dir, extensions=AUDIO_EXTENSIONS, recursive=True
    )
    for file_path in tqdm(audio_files, desc="Processing audio file"):
        file_stem = file_path.stem
        file_suffix = file_path.suffix

        rel_path = Path(file_path).relative_to(audio_dir)
        (save_path / rel_path.parent).mkdir(parents=True, exist_ok=True)

        audio, sr = librosa.load(file_path, sr=sample_rate, mono=False)
        transcription = model.transcribe(str(file_path), language=language)

        for segment in transcription.get("segments", []):
            id, text, start, end = (
                segment["id"],
                segment["text"],
                segment["start"],
                segment["end"],
            )

            extract = audio[..., int(start * sr) : int(end * sr)]
            sf.write(
                save_path / rel_path.parent / f"{file_stem}_{id}{file_suffix}",
                extract,
                samplerate=sr,
            )

            with open(
                save_path / rel_path.parent / f"{file_stem}_{id}.lab",
                "w",
                encoding="utf-8",
            ) as f:
                f.write(text)


if __name__ == "__main__":
    main()
