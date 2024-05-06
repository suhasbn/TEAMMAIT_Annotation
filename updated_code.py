import prodigy
import pysrt
import os

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


def load_audio_transcript_pair(audio_file, srt_file, server_url):
    subs = pysrt.open(srt_file)
    # Build HTML for transcript, enclosed in a scrollable div
    transcript_html = "<br>".join([f"{sub.index}. {sub.text} ({sub.start} - {sub.end})" for sub in subs])
    scrollable_html = f"<div style='max-height: 200px; overflow-y: auto; '>{transcript_html}</div>"
    return {
        "audio": f"{server_url}/{os.path.basename(audio_file)}",
        "html": scrollable_html,
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
            ],
            "global_css": """
                .prodigy-labels { font-size: 12px; } // I've even reduced the font size to make it fit.
                .prodigy-label { white-space: nowrap; }
                .prodigy-labels { overflow-x: auto; display: flex; flex-wrap: wrap; align-content: flex-start; }
                .prodigy-content { display: flex; flex-direction: column; }
            """
        }
    }