# generate_dataframe.py

import json
import pandas as pd
import sys
import os

def generate_dataframe(json_path, output_csv_path=None):
    with open(json_path, 'r') as f:
        aggregated_results = json.load(f)

    df_rows = []
    for second, data in aggregated_results.items():
        row = {
            "second": int(second),
            "frames_analyzed": data["frames_analyzed"],
            "face_confidence": data["face_confidence"],
            "prevalent_emotion": data["prevalent_emotion"]
        }
        for emotion, prob in data["emotions"].items():
            row[f"emotion_{emotion}"] = prob
        df_rows.append(row)

    df = pd.DataFrame(df_rows)

    if output_csv_path:
        df.to_csv(output_csv_path, index=False)
        print(f"Dataframe saved to {output_csv_path}")
    return df


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_dataframe.py <json_path> [<output_csv_path>]")
        sys.exit(1)

    json_path = sys.argv[1]
    output_csv_path = sys.argv[2] if len(sys.argv) > 2 else None

    generate_dataframe(json_path, output_csv_path)
