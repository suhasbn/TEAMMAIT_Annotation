import prodigy
import pysrt
import os
import boto3
from botocore.exceptions import ClientError
import requests
import json
import re

# Set the media server URL
MEDIA_SERVER_URL = "http://localhost:8000"  # Change this if using a different port


os.environ['PRODIGY_HOST'] = '0.0.0.0'

s3 = boto3.client('s3')
bucket_name = 'teammait-annotation-trial'

#LABELS = ["label" + str(i) for i in range(1, 32)]
#I've just shortened each of the 31 labels that we had initially created to better fit in the space we have!
LABELS = [
    "Treatment_Rationale",  # 1. Therapist explained the rationale for treatment
    "Review_Homework",      # 2. Therapist reviewed homework from the previous session
    "Discuss_Avoidance",    # 3. Discussion of avoidance and confronting distressing memories
    "Imaginal_Instructions",# 4. Therapist gave instructions for carrying out Imaginal Exposure
    "Hotspots_Intro",       # 5. “Hotspots” procedure and rationale introduced
    "Identify_Hotspots",    # 6. Therapist helped patient to identify hotspots
    "Imaginal_Orientation", # 7. Orientation to the Imaginal Exposure planned for the session
    "Conduct_Imaginal",     # 8. Conduction of Imaginal Exposure
    "Monitor_SUDS",         # 9. Monitoring of SUDS ratings every 5 minutes
    "Reinforcing_Comments", # 10. Appropriate reinforcing comments used during Imaginal
    "Elicit_Thoughts",      # 11. Elicitation of thoughts and feelings as appropriate
    "Prompt_Tense_Eyes",    # 12. Prompting for present tense, closed eyes
    "Imaginal_Duration",    # 13. Imaginal lasted about 30-45 minutes (or about 15 for final imaginal)
    "Process_Imaginal",     # 14. Processing of Imaginal Exposure with client
    "Plan_In_Vivo",         # 15. Explanation and planning of In Vivo Exposure tasks
    "Review_In_Vivo_HW",    # 16. Review and discussion of In Vivo Exposure homework
    "Adjust_In_Vivo_Hier",  # 17. Adjustments made to In Vivo hierarchy as necessary
    "Discuss_Avoidance_Beh",# 18. Discussion of any avoidance behaviors observed or reported
    "Maintain_Rapport",     # 19. Maintained good rapport with the patient
    "Professional_Engage",  # 20. Engagement with the client in a professional manner
    "Structure_Therapy",    # 21. Efficient structuring of therapy time
    "Adhere_Model",         # 22. Adherence to the treatment model
    "Off_Task_Discuss",     # 23. Engagement in off-task discussion for more than 15 minutes
    "Address_Problems",     # 24. Addressing any significant problems that led to a departure from the treatment plan
    "Evaluate_Problem_Mgmt",# 25. Evaluation of adequacy in dealing with problems leading to treatment plan departure
    "Rate_Essentials",      # 26. Rating the adequacy of therapist regarding Essential Elements
    "Rate_Understanding",   # 27. Rating the degree of patient's understanding of the rationale
    "Rate_Skill",           # 28. Rating therapist's overall skill as demonstrated in the session
    "Session_Comments",     # 29. Additional comments regarding the conduct of the session
    "Discuss_Future_Goals", # 30. Discussion of future goals and relapse prevention
    "Evaluate_Progress"     # 31. Evaluation of overall treatment progress and next steps
]


def load_audio_transcript_pair(audio_key, bucket_name):
    try:
        # Generate pre-signed URL for audio file
        audio_url = s3.generate_presigned_url('get_object', Params={'Bucket': bucket_name, 'Key': audio_key}, ExpiresIn=3600)
        
        # Try to get the corresponding transcript file (.srt or .txt)
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
            # Remove any WEBVTT headers if present (common in .srt files)
            transcript_content = re.sub(r'WEBVTT\n\n', '', transcript_content)
            # Remove timestamp lines (if any)
            transcript_content = re.sub(r'\d{2}:\d{2}:\d{2}\.\d{3} --> \d{2}:\d{2}:\d{2}\.\d{3}\n', '', transcript_content)
            # Split into lines and remove empty lines
            lines = [line.strip() for line in transcript_content.split('\n') if line.strip()]
            # Join lines with newlines
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
def audio_annotation():
    stream = []
    paginator = s3.get_paginator('list_objects_v2')
    for page in paginator.paginate(Bucket=bucket_name):
        for obj in page.get('Contents', []):
            if obj['Key'].endswith(('.wav', '.MP3', '.mp3')):
                example = load_audio_transcript_pair(obj['Key'], bucket_name)
                if example:
                    stream.append(example)
    
    print(f"Total examples loaded: {len(stream)}")
    if len(stream) > 0:
        print(f"First example: {json.dumps(stream[0], indent=2)}")
    else:
        print("No examples loaded!")
    
    return {
        "dataset": "audio_dataset",
        "stream": stream,
        "view_id": "blocks",
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

# Test S3 access
def test_s3_access():
    try:
        s3.head_bucket(Bucket=bucket_name)
        print(f"Successfully accessed bucket: {bucket_name}")
        # List some objects in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name, MaxKeys=5)
        print("Sample objects in bucket:")
        for obj in response.get('Contents', []):
            print(f" - {obj['Key']}")
    except ClientError as e:
        print(f"Error accessing bucket: {str(e)}")

if __name__ == "__main__":
    test_s3_access()
