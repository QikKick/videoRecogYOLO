import cv2
import numpy as np
import pandas as pd
from ultralytics import YOLO
from moviepy import VideoFileClip
from tqdm import tqdm  # Progreso juostai
import os


class VideoAnalyzer:
    """
    Klasė, skirta vaizdo įrašo analizei naudojant YOLO objektų aptikimą.
    """

    def __init__(self, video_path, model_name="yolov8n.pt"):
        self.video_path = video_path
        self.model = YOLO(model_name)

        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video failas nerastas: {video_path}")

    def analyze(self, scan_interval=10):
        """
        Skenuoja video failą ir grąžina DataFrame su vaizdo įvertinimais.

        Args:
            scan_interval (int): Kas kelintą kadrą analizuoti (didesnis = greičiau).

        Returns:
            pd.DataFrame: Lentelė su stulpeliais ['frame', 'time_sec', 'visual_score']
        """
        cap = cv2.VideoCapture(self.video_path)
        if not cap.isOpened():
            raise ValueError("Nepavyko atidaryti video failo su OpenCV.")

        fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

        data = []

        print(f"Pradedama VAIZDO analizė ({os.path.basename(self.video_path)})...")

        pbar = tqdm(total=total_frames)

        frame_idx = 0
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            if frame_idx % scan_interval == 0:
                results = self.model(frame, verbose=False, classes=[0, 32])

                person_count = 0
                ball_detected = 0

                for r in results:
                    boxes = r.boxes
                    for box in boxes:
                        cls = int(box.cls[0])
                        if cls == 0:
                            person_count += 1
                        elif cls == 32:
                            ball_detected = 1

                score = (person_count * 1) + (ball_detected * 50)

                data.append({
                    'frame': frame_idx,
                    'time_sec': frame_idx / fps,
                    'visual_score': score
                })

            pbar.update(1)
            frame_idx += 1

        cap.release()
        pbar.close()

        df = pd.DataFrame(data)

        if not df.empty:
            v_min, v_max = df['visual_score'].min(), df['visual_score'].max()
            df['visual_norm'] = (df['visual_score'] - v_min) / (v_max - v_min + 1e-6)

        return df, fps


class AudioAnalyzer:
    """
    Klasė, skirta garso takelio analizei (RMS - garsumo nustatymui).
    """

    def __init__(self, video_path):
        self.video_path = video_path

    def add_audio_scores(self, df_video):
        """
        Papildo video duomenų lentelę garso duomenimis.

        Args:
            df_video (pd.DataFrame): Lentelė su 'time_sec' stulpeliu.

        Returns:
            pd.DataFrame: Papildyta lentelė su 'audio_score' ir 'audio_norm'.
        """
        print("Pradedama GARSO analizė...")

        try:
            clip = VideoFileClip(self.video_path)
            audio = clip.audio

            if audio is None:
                print("ĮSPĖJIMAS: Video neturi garso takelio. Garso balai bus 0.")
                df_video['audio_norm'] = 0
                return df_video

            audio_fps = 22050
            sound_array = audio.to_soundarray(fps=audio_fps)

            if sound_array.ndim == 2:
                sound_array = sound_array.mean(axis=1)

            total_samples = len(sound_array)
            duration = clip.duration

            audio_scores = []

            for t in tqdm(df_video['time_sec'], desc="Apdorojamas garsas"):
                start_t = max(0, t - 0.25)
                end_t = min(duration, t + 0.25)

                start_idx = int(start_t * audio_fps)
                end_idx = int(end_t * audio_fps)

                chunk = sound_array[start_idx:end_idx]

                if len(chunk) > 0:
                    rms = np.sqrt(np.mean(chunk ** 2))
                else:
                    rms = 0
                audio_scores.append(rms)

            df_video['audio_score'] = audio_scores

            a_min, a_max = df_video['audio_score'].min(), df_video['audio_score'].max()
            df_video['audio_norm'] = (df_video['audio_score'] - a_min) / (a_max - a_min + 1e-6)

            clip.close()
            del sound_array

            return df_video

        except Exception as e:
            print(f"Klaida garso analizėje: {e}")
            df_video['audio_norm'] = 0
            return df_video

