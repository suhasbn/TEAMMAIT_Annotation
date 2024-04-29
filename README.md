# TEAMMAIT_Annotation

# Audio Annotation with Prodigy

This README provides instructions on how to install Prodigy, set up the directory structure, and run the audio annotation code.

## Installation

To install Prodigy, you need to have Python 3.6 or later installed on your system. You can install Prodigy using pip by running the following command:

Make sure you have the necessary permissions to install packages globally. If you encounter any issues, you can try installing Prodigy in a virtual environment.

## Directory Structure

To use the audio annotation code, ensure that your directory structure is set up as follows:

data_directory/
├── audio1.MP3
├── audio1.MP3.srt
├── audio2.MP3
├── audio2.MP3.srt

- The `data_directory` should contain the audio files (`.MP3`) and their corresponding transcript files (`.srt`).
- The transcript file should have the same name as the audio file, with the additional `.srt` extension.

## Python Code

The Python code for audio annotation is provided in the `annotation_code.py` file. This code defines a custom Prodigy recipe that allows annotators to listen to audio files, follow along with the transcript, and assign labels to specific segments of the audio.

Make sure the `annotation_code.py` file is in the same directory as your data directory.

## Running the Code

To run the audio annotation code, open a terminal or command prompt and navigate to the directory containing the `annotation_code.py` file.

Run the following command:

Sure! Here's a README file for your professor that explains how to install Prodigy, the directory structure, and how to run the code:
Copy code# Audio Annotation with Prodigy

This README provides instructions on how to install Prodigy, set up the directory structure, and run the audio annotation code.

## Installation

To install Prodigy, you need to have Python 3.6 or later installed on your system. You can install Prodigy using pip by running the following command:
pip install prodigy
Copy code
Make sure you have the necessary permissions to install packages globally. If you encounter any issues, you can try installing Prodigy in a virtual environment.

## Directory Structure

To use the audio annotation code, ensure that your directory structure is set up as follows:
data_directory/
├── audio1.MP3
├── audio1.MP3.srt
├── audio2.MP3
├── audio2.MP3.srt
...
Copy code
- The `data_directory` should contain the audio files (`.MP3`) and their corresponding transcript files (`.srt`).
- The transcript file should have the same name as the audio file, with the additional `.srt` extension.

## Python Code

The Python code for audio annotation is provided in the `annotation_code.py` file. This code defines a custom Prodigy recipe that allows annotators to listen to audio files, follow along with the transcript, and assign labels to specific segments of the audio.

Make sure the `annotation_code.py` file is in the same directory as your data directory.

## Running the Code

To run the audio annotation code, open a terminal or command prompt and navigate to the directory containing the `annotation_code.py` file.

Run the following command:
prodigy -F annotation_code.py audio-annotation TEAMMAIT /path/to/your/data/directory/

This command will start the Prodigy annotation server, and you can access the annotation interface by opening a web browser and navigating to `http://localhost:8080`.
