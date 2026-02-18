from moviepy import VideoFileClip, concatenate_videoclips
import os
import pandas as pd


class VideoEditor:
    """
    Klasė, atsakinga už video karpymą, intervalų sujungimą ir galutinio failo generavimą.
    """

    def __init__(self, video_path):
        self.video_path = video_path
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video failas nerastas: {video_path}")

    def create_summary(self, df, target_duration, output_path):
        """
        Atrenka geriausius momentus ir sukuria santrauką.

        Args:
            df (pd.DataFrame): Duomenys su 'final_score' ir 'time_sec'.
            target_duration (int): Norima trukmė sekundėmis.
            output_path (str): Kur išsaugoti rezultatą.
        """
        print(f"Montuojamas video į: {output_path}")

        if df.empty or 'final_score' not in df.columns:
            print("KLAIDA: Nėra duomenų montavimui.")
            return

        threshold = df['final_score'].quantile(0.85)
        important_frames = df[df['final_score'] >= threshold].copy()

        if important_frames.empty:
            print("Nepavyko rasti pakankamai svarbių momentų (visi balai per žemi).")
            return

        BUFFER = 1.5
        intervals = []

        for _, row in important_frames.iterrows():
            t = row['time_sec']
            start = max(0, t - BUFFER)
            end = t + BUFFER
            intervals.append([start, end])

        intervals.sort()
        merged_intervals = []

        if intervals:
            curr_start, curr_end = intervals[0]
            for next_start, next_end in intervals[1:]:
                if next_start <= curr_end + 1.0:
                    curr_end = max(curr_end, next_end)
                else:
                    merged_intervals.append((curr_start, curr_end))
                    curr_start, curr_end = next_start, next_end
            merged_intervals.append((curr_start, curr_end))

        print(f"Rasta {len(merged_intervals)} epizodų. Karpoma...")

        try:
            original_clip = VideoFileClip(self.video_path)
            subclips = []
            current_duration = 0

            for start, end in merged_intervals:
                if current_duration >= target_duration:
                    break

                end = min(original_clip.duration, end)

                if start < end:
                    try:
                        clip = original_clip.subclipped(start, end)
                    except AttributeError:
                        clip = original_clip.subclip(start, end)

                    subclips.append(clip)
                    current_duration += (end - start)

            if subclips:
                final_clip = concatenate_videoclips(subclips)

                if final_clip.duration > target_duration:
                    try:
                        final_clip = final_clip.subclipped(0, target_duration)
                    except AttributeError:
                        final_clip = final_clip.subclip(0, target_duration)

                final_clip.write_videofile(
                    output_path,
                    codec="libx264",
                    audio_codec="aac",
                    temp_audiofile='temp-audio.m4a',
                    remove_temp=True,
                    fps=24,
                    preset='medium'
                )
                print(f"✅ Sėkmingai sukurta: {output_path} (Trukmė: {final_clip.duration:.2f}s)")
            else:
                print("Nepavyko sugeneruoti klipų.")

            original_clip.close()

        except Exception as e:
            print(f"Klaida montavimo metu: {e}")