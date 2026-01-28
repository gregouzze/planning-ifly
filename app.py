# app.py
# Ce fichier crée un petit serveur web pour afficher tes disponibilités

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from planner import generer_calendrier
from pdf_reader import extraire_mon_planning

app = FastAPI()

# 📄 CONFIG PDF
CHEMIN_PDF = "iFP.planning.pdf"   # ⬅️ mets le bon nom ici
MES_INITIALES = "GBd"

# ✏️ ICI TU MODIFIES TES CONSIGNES CLIENT
INFOS_CLIENT = """
<ul>
<li>Merci d’arriver 10 minutes en avance</li>
<li>Créneaux de 30 minutes</li>
<li>Annulation minimum 24h à l’avance</li>
</ul>
"""

@app.get("/", response_class=HTMLResponse)
def afficher_calendrier():

    # 🔍 1. Extraction du planning depuis le PDF
    planning = extraire_mon_planning(CHEMIN_PDF, MES_INITIALES)

    # 🧠 2. Génération du HTML
    calendrier = generer_calendrier(planning)

    html = f"""
    <html>
    <head>
        <title>Disponibilités Greg</title>
        <style>
            body {{
                font-family: Arial, sans-serif;
                background-color: #f4f6f8;
                margin: 0;
            }}
            .container {{
                max-width: 1200px;
                margin: auto;
                padding: 20px;
            }}
            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            h1 {{
                color: #003A8F;
            }}
            .logo {{
                height: 60px;
            }}
            .infos {{
                background: white;
                padding: 15px;
                border-left: 6px solid #00AEEF;
                margin: 30px 0;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                margin-bottom: 30px;
            }}
            th {{
                background-color: #003A8F;
                color: white;
                padding: 10px;
            }}
            td {{
                padding: 15px;
                border: 1px solid #ddd;
            }}
            .slot {{
                display: inline-block;
                background-color: #00AEEF;
                color: white;
                padding: 6px 12px;
                margin: 4px;
                border-radius: 6px;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>

    <div class="container">

        <div class="header">
            <h1>Disponibilités Greg</h1>
            <img class="logo" src="https://www.iflyworld.com/wp-content/uploads/2021/06/iFLY-logo.svg">
        </div>

        <div class="infos">
            <h3>📌 Informations importantes</h3>
            {INFOS_CLIENT}
        </div>

        {calendrier}

    </div>

    </body>
    </html>
    """

    return html
