# TEAMMAIT_Annotation

## Installation

Python 3.9 or later is needed. You can install Prodigy using pip:
`pip install prodigy -f https://4D57-240B-BE2C-4802@download.prodi.gy`

I have created a virtual environemnt called `prodigy_env` with the following libraries that I have listed in `requirements.txt`.

## Directory Structure

To use the audio annotation code, the directory structure is set up as follows:
<pre>
<code>
data_directory/
├── audio1.MP3
├── audio1.MP3.srt
├── audio2.MP3
└── audio2.MP3.srt
    .
    .
    .
</code>
</pre>

- The `data_directory` has the audio files (`.MP3`) and their corresponding transcript files (`.srt`).
- The transcript file should have the same name as the audio file, with the additional `.srt` extension.

## Python Code

The Python code is `annotation_code.py` file. I have defined a custom Prodigy recipe that allows annotators to listen to audio files, follow along with the transcript, and assign labels to specific segments of the audio.

Make sure the `annotation_code.py` file is in the same directory as the data directory.

## Data
I have not included the audio because it contains PII data.

## Running the Code

To run the code, open a terminal and navigate to the directory containing the `annotation_code.py` file.

Run the following command:

`prodigy -F annotation_code.py audio-annotation TEAMMAIT /path/to/your/data/directory/`

This command will start the Prodigy annotation server, and you can access the annotation interface by opening a web browser and navigating to `http://localhost:8080`.
