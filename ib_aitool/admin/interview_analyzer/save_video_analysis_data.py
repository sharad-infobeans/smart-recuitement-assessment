import requests
from flask import request, jsonify, render_template
from flask_restful import Resource, Api
from ib_aitool.database import db
import re
import os
from datetime import datetime
from ib_aitool.database.models.CandidateModel import Candidate
from ib_aitool.database.models.VideoProcessModel import VideoProcess,VideoReport
import retrying
import json
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import numpy as np
# Load the pre-trained model and tokenizer
model_name = "michellejieli/emotion_text_classifier"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForSequenceClassification.from_pretrained(model_name)

API_URL = "https://api-inference.huggingface.co/models/michellejieli/emotion_text_classifier"
headers = {"Authorization": "Bearer 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","Content-Type": "application/json"}
  
# Define the API request function
@retrying.retry(
    stop_max_attempt_number=3,  # Maximum number of retry attempts
    wait_fixed=1000,  # Wait 1000 milliseconds (1 second) between retries
    retry_on_exception=lambda e: isinstance(e, requests.exceptions.Timeout),  # Retry on timeout exception
)
def get_text_sentiments(input_text):
        # Define the text you want to classify
    # Tokenize the input text
    inputs = tokenizer(input_text, return_tensors="pt", padding=True, truncation=True)

    # Get the logits (raw scores) for each label
    with torch.no_grad():
        logits = model(**inputs).logits

    # Convert logits to probabilities
    probs = torch.softmax(logits, dim=1)

    # Get the labels and their corresponding probabilities
    label_ids = np.arange(probs.shape[1])
    labels = [model.config.id2label[label_id] for label_id in label_ids]
    probabilities = probs[0].tolist()  # Assuming you have a single input text

    # Create a list of dictionaries with labels and scores
    result = [
        {
            "label": label,
            "score": score,
        }
        for label, score in zip(labels, probabilities)
    ]

    if result: 
        result_dict = {item['label']: item['score'] for item in result}
        # Replace specific keys
        replacement_mapping = {
            'joy': 'happy',
            'sadness': 'sad',
            'anger': 'angry'
        }
        # Create the updated dictionary with replaced keys
        updated_result_dict = {replacement_mapping.get(key, key): value for key, value in result_dict.items()}
        return updated_result_dict
    else:
        updated_result_dict={}
        return updated_result_dict

def convert_dict(input_dict):
    order = [
        'angry',
        'disgust',
        'fear',
        'happy',
        'neutral',
        'sad',
        'surprise'
    ]

    output_dict = {key: input_dict[key] for key in order if key in input_dict}
    return output_dict

def save_videots_report(data_by_timestamps,audio_emotions):
    if data_by_timestamps:
        for item in data_by_timestamps:
            key = list(item.keys())[0]  # Get the key from the dictionary
            #print(key)
        # print(item[key])
            trans_data= VideoProcess.get_transcripts_by_videoprocessid(key)
            interview_transcript=trans_data.interview_transcript
            vid=trans_data.vid
            added_by=trans_data.added_by
            speaker=trans_data.speaker
            #print(interview_transcript)
            if audio_emotions:
                filtered_dicts = [item for item in audio_emotions if key in item]
                if filtered_dicts:
                    emotion_dict_data = convert_dict(filtered_dicts[0][key])
                else:
                    emotion_dict_data={'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0}
            else:
                emotion_dict_data={'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0}   
            transcript_emotions=get_text_sentiments(interview_transcript)
            #print(transcript_emotions)
            if item[key]:
                frame_report=item[key]
            else:
                frame_report={'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0}

            if transcript_emotions:
                transcript_emotions_data=transcript_emotions
            else:
                transcript_emotions_data={'angry': 0.0, 'disgust': 0.0, 'fear': 0.0, 'happy': 0.0, 'sad': 0.0, 'surprise': 0.0, 'neutral': 0.0}
                
            video_report = VideoReport(
                video_process_id=key,
                frame_dur_report=frame_report,
                text_dur_report=transcript_emotions_data,
                audio_report=emotion_dict_data,
                speaker=speaker,
                added_by=added_by,
                video_id=vid,
                created_at=datetime.utcnow(),
            )
            db.session.add(video_report)
            db.session.commit()

        return True
    else:
        return False

def generate_and_save_overall_video_report(videoid, speaker):
    interviewer_data = VideoReport.get_video_timestamp_report(speaker, videoid)
    timestamps_data_report_count = len(interviewer_data)
    timestamps_interviewer_frame_report = {
        "angry": 0,
        "disgust": 0,
        "fear": 0,
        "happy": 0,
        "sad": 0,
        "surprise": 0,
        "neutral": 0
    }
    timestamps_text_report = {
        "angry": 0,
        "disgust": 0,
        "fear": 0,
        "happy": 0,
        "sad": 0,
        "surprise": 0,
        "neutral": 0
    }

    timestamps_audio_report = {
        "angry": 0,
        "disgust": 0,
        "fear": 0,
        "happy": 0,
        "sad": 0,
        "surprise": 0,
        "neutral": 0
    }
    

    for report in interviewer_data:
        
        timestamps_frame_report_json = report.frame_dur_report  # Already a dictionary, no need to load it.
        # Replace single quotes with double quotes
        timestamps_frame_report_json = timestamps_frame_report_json.replace("'", "\"")
        timestamps_frame_report = json.loads(timestamps_frame_report_json)

        text_sentiment_report_json = report.text_dur_report  # Already a dictionary, no need to load it.
        # Replace single quotes with double quotes
        text_sentiment_report_json = text_sentiment_report_json.replace("'", "\"")
        text_sentiment_report = json.loads(text_sentiment_report_json)
        
        audio_report_sentiment_report={}
        audio_report_sentiment_report_json = report.audio_report
        if audio_report_sentiment_report_json:
            audio_report_sentiment_report_json = audio_report_sentiment_report_json.replace("'", "\"")
            audio_report_sentiment_report = json.loads(audio_report_sentiment_report_json)

        timestamps_interviewer_frame_report["angry"] += timestamps_frame_report['angry'] 
        timestamps_interviewer_frame_report["disgust"] += timestamps_frame_report['disgust'] 
        timestamps_interviewer_frame_report["fear"] += timestamps_frame_report['fear'] 
        timestamps_interviewer_frame_report["happy"] += timestamps_frame_report['happy'] 
        timestamps_interviewer_frame_report["sad"] += timestamps_frame_report['sad'] 
        timestamps_interviewer_frame_report["surprise"] += timestamps_frame_report['surprise'] 
        timestamps_interviewer_frame_report["neutral"] += timestamps_frame_report['neutral'] 

        timestamps_text_report["angry"] += text_sentiment_report['angry'] 
        timestamps_text_report["disgust"] += text_sentiment_report['disgust'] 
        timestamps_text_report["fear"] += text_sentiment_report['fear'] 
        timestamps_text_report["happy"] += text_sentiment_report['happy'] 
        timestamps_text_report["sad"] += text_sentiment_report['sad'] 
        timestamps_text_report["surprise"] += text_sentiment_report['surprise'] 
        timestamps_text_report["neutral"] += text_sentiment_report['neutral']
        
        if audio_report_sentiment_report:
            if 'angry' in audio_report_sentiment_report:
                timestamps_audio_report["angry"] += audio_report_sentiment_report['angry']

            if 'disgust' in audio_report_sentiment_report:
                timestamps_audio_report["disgust"] += audio_report_sentiment_report['disgust']

            if 'fear' in audio_report_sentiment_report:
                timestamps_audio_report["fear"] += audio_report_sentiment_report['fear']

            if 'happy' in audio_report_sentiment_report:
                timestamps_audio_report["happy"] += audio_report_sentiment_report['happy']

            if 'sad' in audio_report_sentiment_report:
                timestamps_audio_report["sad"] += audio_report_sentiment_report['sad']

            if 'surprise' in audio_report_sentiment_report:
                timestamps_audio_report["surprise"] += audio_report_sentiment_report['surprise']

            if 'neutral' in audio_report_sentiment_report:
                timestamps_audio_report["neutral"] += audio_report_sentiment_report['neutral']

    timestamp_frame_result = {key: round(value / timestamps_data_report_count, 2) for key, value in timestamps_interviewer_frame_report.items()}
    text_sentiments_result = {key: round(value / timestamps_data_report_count, 2) for key, value in timestamps_text_report.items()}
    audio_sentiments_result = {key: round(value / timestamps_data_report_count, 2) for key, value in timestamps_audio_report.items()}

   # print(timestamp_frame_result)
   # print(text_sentiments_result)
    all_zeros_audio_sentiments = all(value == 0.0 for value in audio_sentiments_result.values())
    if all_zeros_audio_sentiments:
        audio_sentiments_result=''

    candidate_data = Candidate.query.filter_by(id=videoid).first()
    if candidate_data:
        if speaker =="Interviewer":
            candidate_data.overall_interviewer_video_report = timestamp_frame_result
            candidate_data.overall_interviewer_text_report = text_sentiments_result
            candidate_data.overall_interviewer_audio_report = audio_sentiments_result
            db.session.commit()
        elif speaker =="candidate":
            candidate_data.overall_candidate_video_report = timestamp_frame_result
            candidate_data.overall_candidate_text_report = text_sentiments_result
            candidate_data.overall_candidate_audio_report = audio_sentiments_result
            db.session.commit()


    
    return True


