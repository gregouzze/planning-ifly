

# planner.py

from rotations import ROTATIONS

def generer_calendrier(planning):
    """
    Génère le HTML du calendrier à partir du planning extrait du PDF
    """
    html = ""

    for date_iso, rotation in planning.items():
        creneaux = ROTATIONS.get(rotation, [])

        # format date lisible
        date_affichee = date_iso.replace("-", "/")

        html += f"""
        <h2>{date_affichee} – Rotation {rotation}</h2>
        <table>
            <tr>
                <th>Créneaux disponibles</th>
            </tr>
            <tr>
                <td>
        """

        for c in creneaux:
            html += f'<span class="slot">{c}</span>'

        html += """
                </td>
            </tr>
        </table>
        """

    return html
