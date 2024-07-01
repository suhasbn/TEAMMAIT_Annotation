import prodigy
from prodigy.components.db import connect
import os
import json
import boto3
from botocore.exceptions import ClientError
import requests
import re
from datetime import datetime, date, timedelta

os.environ['PRODIGY_HOST'] = '0.0.0.0'

s3 = boto3.client('s3')
bucket_name = 'teammait-annotation-trial'

LABELS = [
    "Treatment_Rationale", "Review_Homework", "Discuss_Avoidance",
    "Imaginal_Instructions", "Hotspots_Intro", "Identify_Hotspots",
    "Imaginal_Orientation", "Conduct_Imaginal", "Monitor_SUDS",
    "Reinforcing_Comments", "Elicit_Thoughts", "Prompt_Tense_Eyes",
    "Imaginal_Duration", "Process_Imaginal", "Plan_In_Vivo",
    "Review_In_Vivo_HW", "Adjust_In_Vivo_Hier", "Discuss_Avoidance_Beh",
    "Maintain_Rapport", "Professional_Engage", "Structure_Therapy",
    "Adhere_Model", "Off_Task_Discuss", "Address_Problems",
    "Evaluate_Problem_Mgmt", "Rate_Essentials", "Rate_Understanding",
    "Rate_Skill", "Session_Comments", "Discuss_Future_Goals",
    "Evaluate_Progress"
]


# Use the home directory to store the annotated_files.txt
HOME_DIR = os.path.expanduser("~")
STATS_FILE = os.path.join(os.path.expanduser("~"), 'annotation_stats.json')
ANNOTATED_FILES_PATH = os.path.join(os.path.expanduser("~"), 'annotated_files.txt')

def load_stats():
    if os.path.exists(STATS_FILE):
        with open(STATS_FILE, 'r') as f:
            return json.load(f)
    return {"total_annotated": 0, "daily_stats": {}}

def save_stats(stats):
    with open(STATS_FILE, 'w') as f:
        json.dump(stats, f)

def update_stats(newly_annotated):
    stats = load_stats()
    today = str(date.today())
    stats["total_annotated"] += len(newly_annotated)
    stats["daily_stats"][today] = stats["daily_stats"].get(today, 0) + len(newly_annotated)
    save_stats(stats)

def print_stats():
    stats = load_stats()
    today = str(date.today())
    print("\nAnnotation Statistics:")
    print(f"Total files annotated so far: {stats['total_annotated']}")
    print(f"Files annotated today: {stats['daily_stats'].get(today, 0)}")
    print(f"Files annotated this week: {sum(stats['daily_stats'].get(str(date.today() - timedelta(days=i)), 0) for i in range(7))}")

def get_annotated_files():
    try:
        with open(ANNOTATED_FILES_PATH, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

def mark_file_as_annotated(filename):
    annotated_files = get_annotated_files()
    if filename not in annotated_files:
        with open(ANNOTATED_FILES_PATH, 'a') as f:
            f.write(f"{filename}\n")

def load_audio_transcript_pair(audio_key, bucket_name):
    try:
        audio_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': audio_key}, ExpiresIn=3600)
        
        transcript_key = os.path.splitext(audio_key)[0]
        transcript_content = None
        
        for ext in ['.srt', '.txt']:
            try:
                file_key = transcript_key + ext
                file_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': file_key}, ExpiresIn=3600)
                response = requests.get(file_url)
                if response.status_code == 200:
                    transcript_content = response.text
                    break
            except Exception as e:
                print(f"Error loading {ext} file for {audio_key}: {str(e)}")
        
        if transcript_content:
            transcript_content = re.sub(r'WEBVTT\n\n', '', transcript_content)
            transcript_content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n', '', transcript_content)
            lines = [line.strip() for line in transcript_content.split('\n') if line.strip()]
            transcript_text = "\n".join(lines)
        else:
            transcript_text = "No transcript available."

        scrollable_html = f"<div style='max-height: 200px; overflow-y: auto;'>{transcript_text}</div>"
        
        example = {
            "audio": audio_url,
            "transcription": transcript_text,
            "html": scrollable_html,
            "meta": {"filename": os.path.basename(audio_key)}
        }
        print(f"Loaded example: {json.dumps(example, indent=2)}")
        return example
    except Exception as e:
        print(f"Error processing {audio_key}: {str(e)}")
        return None


@prodigy.recipe("audio_annotation")
def audio_annotation(dataset):
    stream = []
    annotated_files = get_annotated_files()

    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith(('.wav', '.MP3', '.mp3')) and obj['Key'] not in annotated_files:
                example = load_audio_transcript_pair(obj['Key'], bucket_name)
                if example:
                    stream.append(example)

    print(f"Files loaded for annotation: {len(stream)}")
    print_stats()

    def on_exit(ctrl):
        try:
            DB = connect()
            examples = list(DB.get_dataset_examples(dataset))
            newly_annotated = set()
            for example in examples:
                if example.get('answer') == 'accept':
                    filename = example.get('meta', {}).get('filename')
                    if filename:
                        newly_annotated.add(filename)

            if newly_annotated:
                for filename in newly_annotated:
                    mark_file_as_annotated(filename)
                update_stats(newly_annotated)
                print(f"\nNewly annotated files in this session: {len(newly_annotated)}")
                print_stats()
            else:
                print("\nNo new annotations in this session.")
        except Exception as e:
            print(f"Error in on_exit function: {str(e)}")

    return {
        "dataset": dataset,
        "stream": stream,
        "view_id": "blocks",
        "on_exit": on_exit,
        "config": {
            "labels": LABELS,
            "blocks": [
                {"view_id": "audio_manual"},
                {"view_id": "text_input", "field": "transcription"},
                {"view_id": "html", "field": "html"}
            ],
            "global_css": """
                .prodigy-labels { font-size: 12px; }
                .prodigy-label { white-space: nowrap; }
                .prodigy-labels { overflow-x: auto; display: flex; flex-wrap: wrap; align-content: flex-start; }
                .prodigy-content { display: flex; flex-direction: column; }
            """
        }
    }
