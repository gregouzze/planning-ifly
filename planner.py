

# planner.py

# planner.py

from datetime import datetime, timedelta
from rotations import creneaux_pour_rotation

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

def lundi_de_la_semaine(date_iso):
    date = datetime.strptime(date_iso, "%Y-%m-%d")
    return date - timedelta(days=date.weekday())

def generer_calendrier(planning):
    """
    planning = dict { 'YYYY-MM-DD': 'Z7' }
    Retourne du HTML avec un tableau par semaine
    """

    semaines = {}

    # 1️⃣ Regrouper par semaine
    for date_iso, rotation in planning.items():
        lundi = lundi_de_la_semaine(date_iso).strftime("%Y-%m-%d")

        if lundi not in semaines:
            semaines[lundi] = {}

        semaines[lundi][date_iso] = creneaux_pour_rotation(rotation)

    # 2️⃣ Générer le HTML
    html = ""

    for lundi_iso in sorted(semaines.keys()):
        lundi = datetime.strptime(lundi_iso, "%Y-%m-%d")

        # 📅 Titre en JJ/MM/AAAA
        html += f"<h2>Semaine du {lundi.strftime('%d/%m/%Y')}</h2>"

        html += "<table><tr>"

        # 🗓️ En-têtes avec jour + numéro
        for i, jour in enumerate(JOURS):
            date_jour = lundi + timedelta(days=i)
            classe = "weekend" if jour in ["Samedi", "Dimanche"] else ""
            html += f"<th class='{classe}'>{jour} {date_jour.strftime('%d')}</th>"

        html += "</tr><tr>"

        # ⏰ Créneaux
        for i in range(7):
            jour_date = (lundi + timedelta(days=i)).strftime("%Y-%m-%d")
            creneaux = semaines[lundi_iso].get(jour_date, [])

            if creneaux:
                cell = "".join(f"<div class='slot'>{c}</div>" for c in creneaux)
            else:
                cell = "<div class='empty'>Aucune disponibilité</div>"

            today = datetime.today().strftime("%Y-%m-%d")
            classe = "today" if jour_date == today else ""
            html += f"<td class='{classe}'>{cell}</td>"

        html += "</tr></table>"

    return html
