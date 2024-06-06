from flask import Flask, render_template, jsonify, request
import subprocess
import boto3

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')  # A simple HTML page that loads Prodigy UI in an iframe or through JS

@app.route('/get_audio_data', methods=['GET'])
def get_audio_data():
    # The audio data needs to be fetched from S3 and passed to Prodigy
    bucket = 'teammait-s3-bucket-name'
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=bucket, Prefix='audio/')
    audio_files = [content['Key'] for content in response.get('Contents', []) if content['Key'].endswith('.MP3')]
    data = []
    for key in audio_files:
        # We have corresponding .srt files
        srt_key = key + '.srt'
        data.append({
            'audio_url': f'https://{bucket}.s3.amazonaws.com/{key}',
            'transcript_url': f'https://{bucket}.s3.amazonaws.com/{srt_key}'
        })
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)
