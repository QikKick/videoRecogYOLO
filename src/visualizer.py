# src/visualizer.py
import matplotlib.pyplot as plt
import os


def plot_excitement_curve(df, output_folder):
    """
    Nubraižo grafiką, parodantį vaizdo ir garso intensyvumą per laiką.
    """
    plt.figure(figsize=(12, 6))

    plt.plot(df['time_sec'], df['visual_norm'], label='Vaizdo intensyvumas (YOLO)', alpha=0.6)
    plt.plot(df['time_sec'], df['audio_norm'], label='Garso intensyvumas (RMS)', alpha=0.6)

    plt.plot(df['time_sec'], df['final_score'], label='BENDRAS SVARBUMAS', color='red', linewidth=2)

    threshold = df['final_score'].quantile(0.85)
    plt.axhline(y=threshold, color='green', linestyle='--', label=f'Atrankos riba (Top 15%)')

    plt.title('Krepšinio rungtynių intensyvumo analizė')
    plt.xlabel('Laikas (sekundės)')
    plt.ylabel('Svarbumo balas (0-1)')
    plt.legend()
    plt.grid(True, alpha=0.3)

    save_path = os.path.join(output_folder, 'analysis_chart.png')
    plt.savefig(save_path)
    plt.close()
    print(f"Grafikas išsaugotas: {save_path}")