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
# ===============================
# 📝 MESSAGES CLIENT – À MODIFIER ICI
# ===============================

# 🔒 Message PERMANENT (consignes fixes)
INFOS_PERMANENTES = """
<ul>
  <li>Merci d’arriver au moins <strong>45 minutes avant</strong>l'heure de vol</li>
  <li>Ce site ne permet pas de réserver mais simplement de voir mes créneaux de vols<br>
  Pour réserver, entrer votre bon cadeau sur le site iflyfrance.com</li>
  <li>Coaching niveau 1 ventre</li>
  <li>Coaching niveau 2 dos</li>
</ul>
"""

# 🔥 Message PONCTUEL / PROMO (modifiable ou supprimable)
MESSAGE_PONCTUEL = """
<p>
🎉 <strong>OFFRE DU MOMENT</strong><br>
1 mois offert pour tout nouvel abonnement club <br>
Valable jusqu’au 31/01
</p>
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
            .promo {{
                background: #fff3cd;
                border-left: 6px solid #ffb300;
                padding: 15px;
                margin-bottom: 30px;
                font-size: 16px;
            }}
            .promo strong {{
                color: #c77700;
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
            {INFOS_PERMANENTES}
        </div>

        <div class="promo">
            {MESSAGE_PONCTUEL}
        </div>

        {calendrier}

    </div>

    </body>
    </html>
    """

    return html
