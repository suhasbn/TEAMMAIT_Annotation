# TEAMMAIT_Annotation

## Installation

To install Prodigy, you need to have Python 3.9 or later installed on your system. You can install Prodigy using pip by running the following command:
`pip install prodigy -f https://4D57-240B-BE2C-4802@download.prodi.gy`

I have created a virtual environemnt called `prodigy_env` with the following libraries that I have listed in `requirements.txt`.

## Directory Structure

To use the audio annotation code, ensure that your directory structure is set up as follows:

`data_directory/
├── audio1.MP3
├── audio1.MP3.srt
├── audio2.MP3
├── audio2.MP3.srt`

- The `data_directory` should contain the audio files (`.MP3`) and their corresponding transcript files (`.srt`).
- The transcript file should have the same name as the audio file, with the additional `.srt` extension.

## Python Code

The Python code for audio annotation is provided in the `annotation_code.py` file. This code defines a custom Prodigy recipe that allows annotators to listen to audio files, follow along with the transcript, and assign labels to specific segments of the audio.

Make sure the `annotation_code.py` file is in the same directory as the data directory.

## Running the Code

To run the audio annotation code, open a terminal or command prompt and navigate to the directory containing the `annotation_code.py` file.

Run the following command:

`prodigy -F annotation_code.py audio-annotation TEAMMAIT /path/to/your/data/directory/`

This command will start the Prodigy annotation server, and you can access the annotation interface by opening a web browser and navigating to `http://localhost:8080`.
