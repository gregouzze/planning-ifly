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
Valable jusqu’au 01/03
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
                font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
                background-color: #f2f4f7;
                margin: 0;
                padding: 0;
                color: #1f2937;
            }}

            .container {{
                max-width: 1200px;
                margin: auto;
                padding: 25px;
            }}

            .header {{
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 30px;
            }}

            h1 {{
                margin: 0;
                font-size: 32px;
                color: #003A8F;
            }}

            .logo {{
                height: 55px;
            }}

            .promo {{
                background: #fff3cd;
                border-left: 6px solid #ffb300;
                padding: 15px;
                margin-bottom: 30px;
                font-size: 16px;
                border-radius: 6px;
            }}

            .promo strong {{
                color: #c77700;
            }}

            .infos {{
                background: #ffffff;
                padding: 18px;
                border-left: 6px solid #00AEEF;
                margin-bottom: 35px;
                border-radius: 6px;
            }}

            h2 {{
                margin-top: 45px;
                margin-bottom: 10px;
                color: #003A8F;
                font-size: 22px;
            }}

            table {{
                width: 100%;
                border-collapse: collapse;
                background: white;
                border-radius: 8px;
                overflow: hidden;
                box-shadow: 0 6px 18px rgba(0,0,0,0.05);
                margin-bottom: 35px;
            }}

            th {{
                background-color: #003A8F;
                color: white;
                padding: 14px;
                font-weight: 600;
                font-size: 15px;
            }}

            th.weekend {{
                background-color: #002a66;
            }}

            td {{
                padding: 14px;
                text-align: center;
                border: 1px solid #e5e7eb;
                vertical-align: top;
                min-height: 90px;
            }}

            td.today {{
                background-color: #e6f6ff;
                border: 2px solid #00AEEF;
            }}

            .slot {{
                display: inline-block;
                background: linear-gradient(135deg, #00AEEF, #0090c9);
                color: white;
                padding: 7px 14px;
                margin: 5px 4px;
                border-radius: 20px;
                font-size: 14px;
                font-weight: 500;
                box-shadow: 0 3px 8px rgba(0,0,0,0.15);
            }}

            .empty {{
                color: #9ca3af;
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
