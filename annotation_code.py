# Install boto for S3 integration

'''
import boto3
from io import BytesIO

def get_s3_audio_stream(bucket_name, prefix):
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket_name, Prefix=prefix)
    for obj in response.get('Contents', []):
        audio_key = obj['Key']
        audio_stream = BytesIO()
        s3.download_fileobj(bucket_name, audio_key, audio_stream)
        audio_stream.seek(0)
        yield audio_stream, audio_key
'''
###
## Previous version
'''
import prodigy
#from prodigy.components.loaders import Audio
#from prodigy.util import set_hashes
import srt
import os



def parse_srt_file(srt_file_path):
    with open(srt_file_path, 'r', encoding='utf-8') as file:
        subtitle_generator = srt.parse(file.read())
        subtitles = list(subtitle_generator)
    return [
        {
            'start': sub.start.total_seconds(),  # Convert timedelta to total seconds
            'end': sub.end.total_seconds(),      # Convert timedelta to total seconds
            'text': sub.content                  # The actual subtitle text
        }
        for sub in subtitles
    ]


@prodigy.recipe("audio_segment_labeling", 
    dataset=("The dataset to use", "positional", None, str)
)
def audio_segment_labeling(dataset):
    def get_stream():
        audio_dir = "/Users/suhas/Docs/WHI_Lab/Amanda_Speech_Transcript_Data/Interview1"
        for audio_file in os.listdir(audio_dir):
            if audio_file.lower().endswith(".mp3"):
                audio_id = os.path.splitext(audio_file)[0]
                audio_path = os.path.join(audio_dir, audio_file)
                print("Requested audio" + audio_path)
                srt_path = audio_path + ".srt"
                
                if os.path.isfile(srt_path):
                    subtitles = parse_srt_file(srt_path)
                    task = {
                        "audio": f"1.MP3",
                        "subtitles": subtitles,
                        "meta": {"audio_id":"1.MP3"}
                    }
                    yield task

                else:
                    print(f"SRT file not found for: {audio_id}")


    blocks = [
        {"view_id": "audio"},
        {
            "view_id": "html", 
            "html_template": """
                <h3>Transcript</h3>
                <p id="transcript"></p>
                <script>
                 document.addEventListener('prodigyupdate', () => {
                    const audio = document.querySelector('audio');
                    const transcript = document.getElementById('transcript');
                    // Subtitles are an array of {start, end, text}.
                    const subtitles = window.prodigy.content.task.subtitles || [];

                    function updateTranscript() {
                        const currentTime = audio.currentTime;
                        const currentSubtitle = subtitles.find(sub => currentTime >= sub.start && currentTime <= sub.end);
                        transcript.textContent = currentSubtitle ? currentSubtitle.content : '';
                    }

                    audio.addEventListener('timeupdate', updateTranscript);
                    updateTranscript();  // Call it once to set an initial value for the transcript
                });


                </script>
                """
        },
        {
            "view_id": "spans_manual",  # For labeling spans of audio
            "options": ["TherapistExplainedTheRationale", "OtherOptionsHere"],  # Adjust later
            "label": "Select Segment Labels" 
        }
    ]

    return {
        "dataset": dataset,
        "view_id": "blocks",
        "stream": get_stream(),
        "config": {
            "blocks": blocks,
            "audio_autoplay": True,
            "spans_manual_highlight_color": "#faa"  # Adjust highlight color later
        }
    }
'''
import os
import json
import hashlib
import prodigy
from prodigy.components.loaders import Audio

# Define the labels for annotation
LABELS = [
    "Label1", "Label2", "Label3", "Label4", "Label5",
    "Label6", "Label7", "Label8", "Label9", "Label10",
    "Label11", "Label12", "Label13", "Label14", "Label15",
    "Label16", "Label17", "Label18", "Label19", "Label20",
    "Label21", "Label22", "Label23", "Label24", "Label25",
    "Label26", "Label27", "Label28", "Label29", "Label30",
    "Label31"
]

# Custom recipe for audio annotation with transcripts
@prodigy.recipe('audio-annotation')
def audio_annotation(dataset, data_dir):
    stream = []
    for file_name in os.listdir(data_dir):
        if file_name.endswith(".MP3"):
            audio_path = os.path.join(data_dir, file_name)
            transcript_path = os.path.join(data_dir, file_name + ".srt")
            task = {
                "audio": audio_path,
                "transcript": transcript_path,
                "meta": {"file": file_name}
            }
            
            # Set the input/task hash explicitly
            input_hash = hashlib.md5(audio_path.encode('utf-8')).hexdigest()
            task_hash = hashlib.md5((input_hash + json.dumps(task, sort_keys=True)).encode('utf-8')).hexdigest()
            task['_input_hash'] = int(input_hash, 16)  # Convert input_hash to integer
            task['_task_hash'] = int(task_hash, 16)  # Convert task_hash to integer
            
            stream.append(task)

    def audio_with_transcript(stream):
        for task in stream:
            audio_path = task['audio']
            transcript_path = task['transcript']
            
            # Check if the transcript file exists
            if not os.path.exists(transcript_path):
                print(f"Transcript file not found: {transcript_path}")
                continue
            
            # Read the transcript file and handle any errors
            try:
                with open(transcript_path, 'r') as file:
                    transcript_text = file.read()
            except IOError as e:
                print(f"Error reading transcript file: {transcript_path}")
                print(f"Error: {str(e)}")
                continue
            
            html = [
                '<audio controls src="%s"></audio>' % os.path.basename(audio_path),
                '<div class="transcript">%s</div>' % transcript_text,
                '<script>',
                '  const audio = document.querySelector("audio");',
                '  const transcript = document.querySelector(".transcript");',
                '  audio.addEventListener("timeupdate", () => {',
                '    const currentTime = audio.currentTime;',
                '    const subtitles = transcript.querySelectorAll("p");',
                '    subtitles.forEach(subtitle => {',
                '      const startTime = parseFloat(subtitle.getAttribute("data-start"));',
                '      const endTime = parseFloat(subtitle.getAttribute("data-end"));',
                '      if (currentTime >= startTime && currentTime <= endTime) {',
                '        subtitle.classList.add("active");',
                '      } else {',
                '        subtitle.classList.remove("active");',
                '      }',
                '    });',
                '  });',
                '</script>',
                '<style>',
                '  .transcript p { display: none; }',
                '  .transcript p.active { display: block; }',
                '</style>',
            ]
            task['html'] = ''.join(html)
            yield task

    return {
        "dataset": dataset,
        "stream": audio_with_transcript(stream),
        "view_id": "blocks",
        "config": {
            "labels": LABELS,
            "auto_count_stream": True,
            "audio_autoplay": False,
            "blocks": [
                {"view_id": "audio"},
                {"view_id": "html"},
                {"view_id": "choice", "text": "Select a label"}
            ]
        }
    }