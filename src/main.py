# src/main.py
import argparse
import os
import pandas as pd
from config import *
from analyzer import VideoAnalyzer, AudioAnalyzer
from editor import VideoEditor
from visualizer import plot_excitement_curve


def main():
    parser = argparse.ArgumentParser(description="AI Video Summarizer")
    parser.add_argument("--input", type=str, required=True, help="Kelias iki video failo")
    parser.add_argument("--output", type=str, default="summary.mp4", help="Rezultato failo pavadinimas")
    parser.add_argument("--duration", type=int, default=TARGET_DURATION, help="Norima santraukos trukmė (sekundėmis)")
    args = parser.parse_args()

    if not os.path.exists(args.input):
        print(f"Klaida: Failas {args.input} nerastas.")
        return

    os.makedirs(RESULTS_DIR, exist_ok=True)

    print("--- 1 ETAPAS: Vaizdo analizė (YOLO) ---")
    video_analyzer = VideoAnalyzer(args.input, YOLO_MODEL)
    df, fps = video_analyzer.analyze(scan_interval=SCAN_INTERVAL)

    print("--- 2 ETAPAS: Garso analizė ---")
    audio_analyzer = AudioAnalyzer(args.input)
    df = audio_analyzer.add_audio_scores(df)

    df['final_score'] = (df['visual_norm'] * WEIGHT_VISUAL) + (df['audio_norm'] * WEIGHT_AUDIO)

    csv_path = os.path.join(RESULTS_DIR, "analysis_data.csv")
    df.to_csv(csv_path, index=False)

    print("--- 3 ETAPAS: Grafikų generavimas ---")
    plot_excitement_curve(df, RESULTS_DIR)

    print("--- 4 ETAPAS: Video montavimas ---")
    editor = VideoEditor(args.input)
    editor.create_summary(df, args.duration, os.path.join(RESULTS_DIR, args.output))


if __name__ == "__main__":
    main()