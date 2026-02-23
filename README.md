# videoRecogYOLO

## AI Video Summarizer: Krepšinio Rungtynių Santrauka

## Projekto Aprašymas
Šis projektas yra automatinis vaizdo įrašų apibendrinimo įrankis (*Video Summarization Tool*), sukurtas naudojant Python ir dirbtinį intelektą.

Sistema analizuoja krepšinio rungtynių apžvalgą (pvz., 10 min. trukmės) ir automatiškai sukuria trumpą „highlights“ klipą, remdamasi **hibridine analize**: vaizdiniu veiksmu (žaidėjų ir kamuolio detekcija) ir garso intensyvumu (sirgalių reakcijos).



## Projekto Struktūra

```text
video-summarizer/
├── data/                  # Įvesties duomenys (video failai .mp4)
├── models/                # Iš anksto apmokyti YOLO modeliai (yolo11s.pt)
├── results/               # Generuojami rezultatai (video, grafikai, csv)
├── src/                   # Programinis kodas
│   ├── __init__.py
│   ├── main.py            # Pagrindinis paleidimo failas (CLI sąsaja)
│   ├── config.py          # Nustatymai ir dinaminiai failų keliai
│   ├── analyzer.py        # "Smegenys": YOLO (vaizdas) ir Audio analizės klasės
│   ├── editor.py          # "Rankos": Video karpymo ir montavimo logika
│   └── visualizer.py      # Grafikų generavimas ataskaitoms
├── requirements.txt       # Reikalingų bibliotekų sąrašas
└── README.md              # Projekto dokumentacija

```

## Veikimo Logika (Metodologija)

Sistema naudoja hibridinį „Audio-Visual“ metodą svarbiausioms akimirkoms nustatyti:

### Vaizdo Analizė (Computer Vision):
- Naudojamas YOLOv11 modelis objektų aptikimui.
- Sistema skenuoja vaizdą ir skaičiuoja „svarbumo balą“ pagal formulę: ```(Žmonių skaičius * 1) + (Kamuolys * 50)```. Tai leidžia atskirti žaidimo momentus nuo pertraukėlių.

### Garso Analizė (Audio Processing):
- Naudojama **MoviePy** biblioteka garso takeliui nuskaityti.
- Skaičiuojamas garso stiprumas (RMS - Root Mean Square). Didelis triukšmas dažniausiai indikuoja įvartį arba svarbų įvykį.

### Duomenų Suliejimas (Fusion):
- Vaizdo ir garso duomenys normalizuojami į skalę [0, 1].
- Taikomas svertinis vidurkis: ```Final Score = 0.6 * Visual + 0.4 * Audio```

### Montažas
- Atrenkami 15% geriausiai įvertintų kadrų.
- Jie sujungiami į vientisus epizodus (pridedant 1.5 sek. buferį prieš ir po įvykio).
- Sugeneruojamas galutinis ``.mp4`` failas.

## Aplinkos paruošimas
### Atsisiųskite kodą
`git clone https://github.com/QikKick/videoRecogYOLO.git`

`cd video-summarizer`
###Aplinka
`# Windows:`
`python -m venv .venv`
`.venv\Scripts\activate`

`# Mac/Linux:`
`python3 -m venv .venv`
`source .venv/bin/activate`

### Bibliotekos

`pip install -r requirements.txt`

### Duomenų paruošimas

- Pagrindinėje direktorijoje sukurkite aplanką data/ ir įkelkite ten savo video failą (pvz., video.mp4).

- Naudoto video atsisiuntimo nuoroda (nuoroda laikina, jei neišeina atsisiųsti, susiekit asmeniškai: [https://we.tl/t-flj10cO6WO](https://we.tl/t-flj10cO6WO)

## Paleidimas

- Projektas valdomas per komandinę eilutę. Įsitikinkite, kad esate pagrindiniame projekto aplanke (root).

`python src/main.py --input data/video_pavadinimas.mp4
`

## Rezultatai
Sėkmingai įvykdžius programą, aplanke results/ rasite:

- `summary.mp4`: Galutinis sumontuotas vaizdo įrašas su svarbiausiomis akimirkomis.
- `analysis_chart.png`: Grafikas, vizualiai parodantis vaizdo ir garso intensyvumo kreives bei atrinktus epizodus.
- `analysis_data.csv`: Detalūs duomenys (Excel analizei), kuriuose matomi kiekvieno kadro balai.


### Naudotos Technologijos
* **Python 3.10+**
* **Ultralytics YOLO** (Objektų atpažinimas)
* **MoviePy** (Video redagavimas ir garso analizė)
* **OpenCV** (Vaizdo nuskaitymas)
* **Matplotlib** (Duomenų vizualizacija)
* **Pandas** ir **NumPy** (Duomenų apdorojimas)

**Emilis Keras,**
**Paulius Rybakovas**
