# utils/pdf_export.py

import os
from datetime import datetime

from matplotlib.backends.backend_pdf import PdfPages
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas as rl_canvas
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

# --- MAIN ENTRY POINT ---

def export_report_to_pdf(
    path,
    figures=None,
    stats=None,
    summary=None,
    sections=None,
    title="Rapport de Simulation",
    author="Simulation App",
    add_toc=True,
    custom_logo_path=None
):
    """
    Génére un PDF rapport complet (figures matplotlib, stats, résumé, etc.)
    Params:
        path: destination du PDF
        figures: liste de matplotlib Figure
        stats: liste de tuples (titre, dict|DataFrame)
        summary: texte ou HTML (str)
        sections: liste de str, ex: ['summary', 'stats', 'figures']
        title, author: meta PDF
        add_toc: ajoute une table des matières
        custom_logo_path: chemin vers un logo (facultatif)
    """
    # Sélectionne sections par défaut
    sections = sections or ['summary', 'stats', 'figures']

    # === 1. Génére la page de garde, résumé, stats et TOC via ReportLab
    tmp_main = path + ".rl_temp.pdf"
    doc = SimpleDocTemplate(tmp_main, pagesize=A4, rightMargin=1.5*cm, leftMargin=1.5*cm, topMargin=1.8*cm, bottomMargin=1.5*cm)
    elements = []
    styles = getSampleStyleSheet()
    H1, H2, H3 = styles['Heading1'], styles['Heading2'], styles['Heading3']

    # --- Page de garde / titre
    elements.append(Paragraph(title, H1))
    elements.append(Spacer(1, 0.3*cm))
    if custom_logo_path and os.path.exists(custom_logo_path):
        from reportlab.platypus import Image
        elements.append(Image(custom_logo_path, width=3*cm, height=3*cm))
    elements.append(Spacer(1, 0.1*cm))
    elements.append(Paragraph(f"Créé le : {datetime.now():%d/%m/%Y à %H:%M}", styles["Normal"]))
    elements.append(Paragraph(f"Auteur : {author}", styles["Normal"]))
    elements.append(Spacer(1, 0.7*cm))

    # --- Table des matières
    if add_toc:
        elements.append(Paragraph("Table des matières", H2))
        toc = []
        if 'summary' in sections: toc.append("Résumé")
        if 'stats' in sections: toc.append("Statistiques")
        if 'figures' in sections: toc.append("Graphiques")
        elements.append(Paragraph("<br/>".join(f"{i+1}. {t}" for i, t in enumerate(toc)), styles["Normal"]))
        elements.append(PageBreak())

    # --- Résumé
    if summary and 'summary' in sections:
        elements.append(Paragraph("Résumé", H2))
        elements.append(Paragraph(summary, styles["Normal"]))
        elements.append(Spacer(1, 0.5*cm))
        elements.append(PageBreak())

    # --- Statistiques/Tableaux
    if stats and 'stats' in sections:
        elements.append(Paragraph("Statistiques", H2))
        for stat_title, stat_data in stats:
            elements.append(Paragraph(stat_title, H3))
            elements.append(_stats_table(stat_data, styles))
            elements.append(Spacer(1, 0.2*cm))
        elements.append(PageBreak())

    # --- Build main (non-graph) PDF
    doc.build(elements)

    # === 2. Combine figures matplotlib (1 fig = 1 page) via PdfPages
    tmp_figs = []
    if figures and 'figures' in sections:
        tmp_fig_path = path + ".mpl_temp.pdf"
        with PdfPages(tmp_fig_path) as pdf:
            for fig in figures:
                pdf.savefig(fig, bbox_inches="tight")
        tmp_figs.append(tmp_fig_path)

    # === 3. Fusionne tout dans le PDF final
    from PyPDF2 import PdfMerger
    merger = PdfMerger()
    merger.append(tmp_main)
    for p in tmp_figs:
        merger.append(p)
    merger.write(path)
    merger.close()

    # Clean temp
    os.remove(tmp_main)
    for p in tmp_figs:
        os.remove(p)
    return True

# --- Helpers ---

def _stats_table(data, styles):
    """Crée un tableau ReportLab depuis dict, list of tuples, or DataFrame."""
    from reportlab.platypus import Table, TableStyle
    import pandas as pd
    if isinstance(data, dict):
        rows = [["Clé", "Valeur"]]
        rows += [[str(k), str(v)] for k, v in data.items()]
    elif isinstance(data, pd.DataFrame):
        rows = [list(map(str, data.columns))]
        rows += data.astype(str).values.tolist()
    elif isinstance(data, (list, tuple)):
        rows = [list(map(str, data[0]))] if data and isinstance(data[0], (list, tuple)) else []
        rows += [list(map(str, r)) for r in data[1:]] if len(data) > 1 else []
    else:
        rows = [["Donnée", str(data)]]

    tbl = Table(rows, hAlign='LEFT')
    tbl.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#e6fbe2")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.HexColor("#417505")),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#f6f7fb")]),
        ('GRID', (0,0), (-1,-1), 0.2, colors.HexColor("#bfcddb")),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2),
        ('TOPPADDING', (0,0), (-1,-1), 2),
    ]))
    return tbl

# --- Exemple d'utilisation ---
"""
from utils.pdf_export import export_report_to_pdf

export_report_to_pdf(
    path="rapport_simulation.pdf",
    figures=[fig1, fig2],
    stats=[("Statistiques globales", {"Runs": 12, "Réserve max": 123456})],
    summary="Voici le résumé de la simulation effectuée sur la période 2020-2030...",
    sections=["summary", "stats", "figures"],
    title="Rapport Simulation Retraite",
    author="Nawfal RAZOUK"
)
"""
