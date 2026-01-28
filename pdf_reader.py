
# pdf_reader.py

import pdfplumber
import re
from datetime import datetime

MOIS_FR = {
    "janv": "01",
    "févr": "02",
    "fevr": "02",
    "mars": "03",
}

def convertir_date_fr(date_str):
    """
    '23-janv.' -> '2026-01-23'
    """
    m = re.match(r"(\d{1,2})-([a-zéû]+)", date_str.lower())
    if not m:
        return None
    jour = m.group(1).zfill(2)
    mois_txt = m.group(2)
    mois = MOIS_FR.get(mois_txt)
    if not mois:
        return None
    return f"2026-{mois}-{jour}"

def extraire_mon_planning(chemin_pdf, mes_initiales):
    print("OUVERTURE DU PDF")
    planning = {}

    with pdfplumber.open(chemin_pdf) as pdf:
        for page_num, page in enumerate(pdf.pages, start=1):
            print(f"\n--- PAGE {page_num} ---")

            words = page.extract_words(use_text_flow=True)

            #1 Récupérer les dates avec leurs positions X
            dates = []
            for w in words:
                if re.match(r"\d{1,2}-[a-zéû]+\.?", w["text"].lower()):
                    date_iso = convertir_date_fr(w["text"])
                    if date_iso:
                        dates.append({
                            "date": date_iso,
                            "x": w["x0"]
                        })
                        
            if not dates:
                continue
            
            #2 Trouver la ligne GBd

            for w in words:
                if w["text"] == mes_initiales:
                    y_ref = w["top"]

                    print(f">>> LIGNE TROUVEE POUR {mes_initiales}")

                    #3 Récupérer les rotations sur la même ligne
                    rotations = []
                    for rw in words:
                        if abs(rw["top"] - y_ref) < 3:
                            if re.match(r"[A-Z]\d+", rw["text"]):
                                rotations.append({
                                    "rotation": rw["text"],
                                    "x": rw["x0"]
                                })

                    #4 Associer rotations <-> date par proximité X
                    for rot in rotations:
                        date_proche = min(
                            dates,
                            key=lambda d: abs(d["x"] - rot["x"])
                        )
                        planning[date_proche["date"]] = rot["rotation"]

    return dict(sorted(planning.items()))

                    
                    
