import prodigy
import pysrt
import os


LABELS = ["label" + str(i) for i in range(1, 3)]


def load_audio_transcript_pair(audio_file, srt_file, server_url):
    subs = pysrt.open(srt_file)
    transcript_html = "<br>".join([f"{sub.index}. {sub.text} ({sub.start} - {sub.end})" for sub in subs])
    return {
        "audio": f"{server_url}/{os.path.basename(audio_file)}",
        "html": f"<div>{transcript_html}</div>",
        "spans": [
            {"start": sub.start.ordinal / 1000, "end": sub.end.ordinal / 1000, "label": "transcript"}
            for sub in subs
        ]
    }


@prodigy.recipe("audio_annotation")
def audio_annotation(directory: str):
    server_url = "http://localhost:8000"
    audio_files = [f for f in os.listdir(directory) if f.endswith(".MP3")]
    stream = []
    for audio_file in audio_files:
        audio_file_path = os.path.join(directory, audio_file)
        srt_file = audio_file_path + ".srt"
        if os.path.exists(srt_file):
            example = load_audio_transcript_pair(audio_file_path, srt_file, server_url)
            stream.append(example)

    return {
        "dataset": "audio_dataset",
        "stream": stream,
        "view_id": "blocks",
        "config": {
            "labels": LABELS,
            "blocks": [
                {"view_id": "audio_manual"},
                {"view_id": "html"}
            ]
        }
    }
