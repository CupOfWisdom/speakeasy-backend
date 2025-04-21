import cv2
import json
from deepface import DeepFace
from collections import defaultdict
import numpy as np
from uuid import uuid4
import sys

# Function to extract frames from video
def extract_frames(video_path, frames_per_second=1, start_second=0, end_second=None):
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        raise ValueError("Could not open video file.")

    fps = cap.get(cv2.CAP_PROP_FPS)  # Get the frames per second of the video
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))  # Total frames in the video
    duration = total_frames / fps  # Total duration of the video in seconds

    # Validate start_second and end_second
    if end_second is None or end_second > duration:
        end_second = duration
    if start_second < 0 or start_second >= end_second:
        raise ValueError("Invalid start_second or end_second.")

    frame_interval = int(fps / frames_per_second)  # Calculate frame interval
    start_frame = int(start_second * fps)  # Starting frame
    end_frame = int(end_second * fps)  # Ending frame
    frame_count = 0
    frames = []

    while True:
        ret, frame = cap.read()
        if not ret or frame_count > end_frame:
            break

        # Extract frames within the specified range and interval
        if frame_count >= start_frame and frame_count % frame_interval == 0:
            frames.append(frame)
        frame_count += 1

    cap.release()
    return frames, fps

# Function to analyze emotions and face confidence in frames
def analyze_frames(frames, model='VGG-Face', detector='opencv'):
    results = []
    for frame in frames:
        try:
            analysis = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False, detector_backend=detector)
            # Extract emotion probabilities and face confidence
            emotions = analysis[0]['emotion']
            face_confidence = analysis[0]['face_confidence']
            results.append({
                "emotions": emotions,
                "face_confidence": face_confidence
            })
        except Exception as e:
            print(f"Error analyzing frame: {e}")
            results.append(None)
    return results

# Function to convert numpy float32 to Python float
def convert_float32_to_float(data):
    if isinstance(data, np.float32):
        return float(data)
    elif isinstance(data, dict):
        return {key: convert_float32_to_float(value) for key, value in data.items()}
    elif isinstance(data, list):
        return [convert_float32_to_float(item) for item in data]
    else:
        return data

# Function to aggregate results by second
def aggregate_results(results, frames_per_second):
    aggregated = defaultdict(lambda: {
        "frames_analyzed": 0,
        "face_confidence": 0.0,
        "emotions": defaultdict(float),
        "prevalent_emotion": None
    })

    for i, result in enumerate(results):
        if result:
            second = i // frames_per_second
            aggregated[second]["frames_analyzed"] += 1
            aggregated[second]["face_confidence"] += result["face_confidence"]
            for emotion, prob in result["emotions"].items():
                aggregated[second]["emotions"][emotion] += prob

    # Calculate prevalent emotion and average face confidence for each second
    for second, data in aggregated.items():
        if data["frames_analyzed"] > 0:
            # Calculate average face confidence
            data["face_confidence"] /= data["frames_analyzed"]
            # Calculate prevalent emotion
            prevalent_emotion = max(data["emotions"], key=data["emotions"].get)
            data["prevalent_emotion"] = prevalent_emotion
            # Normalize emotion probabilities
            for emotion in data["emotions"]:
                data["emotions"][emotion] /= data["frames_analyzed"]

    # Convert numpy float32 to Python float
    aggregated = convert_float32_to_float(aggregated)
    return aggregated

# Main function
def main(video_path, output_json_path, frames_per_second=1, start_second=0, end_second=None):
    # Step 1: Extract frames from the video
    frames, fps = extract_frames(video_path, frames_per_second, start_second, end_second)

    # Step 2: Analyze emotions and face confidence in each frame
    results = analyze_frames(frames, detector='yunet')

    # Step 3: Aggregate results by second
    aggregated_results = aggregate_results(results, frames_per_second)

    # Step 4: Save results to a JSON file
    with open(output_json_path, 'w') as f:
        json.dump(aggregated_results, f, indent=4)

    print(f"Analysis complete. Results saved to {output_json_path}.")

# Run the script
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 videoprocessing.py <video_path> <output_dir>")
        sys.exit(1)

    for i in range(10):
        video_path = sys.argv[1]
        output_dir = sys.argv[2]
        uuid = str(uuid4())
        output_json_path = f"{output_dir}/emotion_analysis_results_{uuid}.json"
        frames_per_second = 10  # Number of frames to analyze per second
        start_second = 10  # Start analyzing from this second
        end_second = 70 # Stop analyzing at this second

        main(video_path, output_json_path, frames_per_second, start_second, end_second)