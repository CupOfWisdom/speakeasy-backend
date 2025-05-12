import json
import os
import sys
from uuid import uuid4

def extract_summary(input_path, output_dir):
    with open(input_path, 'r') as f:
        data = json.load(f)

    # Summarized values to extract — adapt as needed
    total_seconds = len(data)
    total_frames = sum([sec["frames_analyzed"] for sec in data.values()])
    average_face_confidence = sum([sec["face_confidence"] for sec in data.values()]) / total_seconds

    # Count occurrences of each prevalent emotion
    emotion_counts = {}
    for sec in data.values():
        emotion = sec["prevalent_emotion"]
        if emotion not in emotion_counts:
            emotion_counts[emotion] = 0
        emotion_counts[emotion] += 1

    most_common_emotion = max(emotion_counts, key=emotion_counts.get)

    summary = {
        "total_seconds_analyzed": total_seconds,
        "total_frames_analyzed": total_frames,
        "average_face_confidence": round(average_face_confidence, 3),
        "most_common_emotion": most_common_emotion,
        "emotion_distribution": emotion_counts
    }

    summary_uuid = str(uuid4())
    output_path = os.path.join(output_dir, f"emotion_summary_{summary_uuid}.json")
    with open(output_path, 'w') as f:
        json.dump(summary, f, indent=4)

    print(f"Summary saved to {output_path}")
    return summary

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python extract_summary.py <input_json_path> <output_dir>")
        sys.exit(1)

    input_json_path = sys.argv[1]
    output_dir = sys.argv[2]
    extract_summary(input_json_path, output_dir)
