#!/usr/bin/env python3
"""Generate a one-page French CV PDF for the PAMAYE audiovisual portfolio."""
from pathlib import Path
import sys
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (
    BaseDocTemplate, Frame, PageTemplate, Paragraph, Spacer, Table, TableStyle
)

OUTPUT = Path(sys.argv[1]) if len(sys.argv) > 1 else Path("_site/cv-pamaye.pdf")
OUTPUT.parent.mkdir(parents=True, exist_ok=True)

NAVY = colors.HexColor("#101820")
GOLD = colors.HexColor("#D7AD56")
INK = colors.HexColor("#26323B")
MUTED = colors.HexColor("#5B6872")
PALE = colors.HexColor("#F2F5F7")
LINE = colors.HexColor("#DCE2E6")
WHITE = colors.white

font_candidates = [
    ("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf",
     "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"),
    ("/usr/share/fonts/truetype/liberation2/LiberationSans-Regular.ttf",
     "/usr/share/fonts/truetype/liberation2/LiberationSans-Bold.ttf"),
]
regular_path = bold_path = None
for reg, bold in font_candidates:
    if Path(reg).exists() and Path(bold).exists():
        regular_path, bold_path = reg, bold
        break

if regular_path and bold_path:
    pdfmetrics.registerFont(TTFont("CVSans", regular_path))
    pdfmetrics.registerFont(TTFont("CVSans-Bold", bold_path))
    REGULAR, BOLD = "CVSans", "CVSans-Bold"
else:
    # Helvetica supports standard French accented characters through WinAnsi.
    REGULAR, BOLD = "Helvetica", "Helvetica-Bold"

PAGE_W, PAGE_H = A4
LEFT = RIGHT = 13 * mm
TOP = 12 * mm
BOTTOM = 12 * mm
GAP = 7 * mm
CONTENT_W = PAGE_W - LEFT - RIGHT
COLUMN_W = (CONTENT_W - GAP) / 2

styles = getSampleStyleSheet()
styles.add(ParagraphStyle(
    name="CVName", fontName=BOLD, fontSize=19, leading=21.5,
    textColor=WHITE, spaceAfter=2
))
styles.add(ParagraphStyle(
    name="CVTagline", fontName=REGULAR, fontSize=8.1, leading=10,
    textColor=colors.HexColor("#E7D7B5")
))
styles.add(ParagraphStyle(
    name="CVContact", fontName=REGULAR, fontSize=7.25, leading=9.3,
    textColor=INK, spaceAfter=1
))
styles.add(ParagraphStyle(
    name="CVIntro", fontName=REGULAR, fontSize=7.65, leading=10.3,
    textColor=INK, spaceAfter=0
))
styles.add(ParagraphStyle(
    name="CVSection", fontName=BOLD, fontSize=8.6, leading=10.2,
    textColor=NAVY, spaceBefore=3.5, spaceAfter=4
))
styles.add(ParagraphStyle(
    name="CVBody", fontName=REGULAR, fontSize=7.15, leading=9.15,
    textColor=INK, spaceAfter=2.2
))
styles.add(ParagraphStyle(
    name="CVSmall", fontName=REGULAR, fontSize=6.8, leading=8.5,
    textColor=MUTED, spaceAfter=1.5
))
styles.add(ParagraphStyle(
    name="CVRole", fontName=BOLD, fontSize=7.6, leading=9.1,
    textColor=NAVY, spaceAfter=1
))
styles.add(ParagraphStyle(
    name="CVBullet", fontName=REGULAR, fontSize=7.05, leading=9,
    textColor=INK, leftIndent=8, firstLineIndent=-6, spaceAfter=1.3
))
styles.add(ParagraphStyle(
    name="CVFooter", fontName=REGULAR, fontSize=6.5, leading=8,
    textColor=MUTED
))
styles.add(ParagraphStyle(
    name="CVLink", fontName=BOLD, fontSize=7.05, leading=9,
    textColor=colors.HexColor("#8A641F"), spaceAfter=2
))

def para(text, style="CVBody"):
    return Paragraph(text, styles[style])

def section(title):
    return [
        Spacer(1, 1.2 * mm),
        para(escape(title.upper()), "CVSection"),
        Table([[""]], colWidths=[COLUMN_W], rowHeights=[0.7], style=TableStyle([
            ("BACKGROUND", (0, 0), (-1, -1), GOLD),
            ("LEFTPADDING", (0, 0), (-1, -1), 0),
            ("RIGHTPADDING", (0, 0), (-1, -1), 0),
            ("TOPPADDING", (0, 0), (-1, -1), 0),
            ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
        ])),
        Spacer(1, 1.8 * mm),
    ]

def bullet(text):
    return para("• " + text, "CVBullet")

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.5)
    canvas.line(LEFT, 8.5 * mm, PAGE_W - RIGHT, 8.5 * mm)
    canvas.setFont(REGULAR, 6.5)
    canvas.setFillColor(MUTED)
    canvas.drawString(LEFT, 5.3 * mm, "PAMAYE · Portfolio audiovisuel")
    canvas.drawRightString(PAGE_W - RIGHT, 5.3 * mm, f"CV professionnel · {doc.page}")
    canvas.restoreState()

doc = BaseDocTemplate(
    str(OUTPUT),
    pagesize=A4,
    leftMargin=LEFT,
    rightMargin=RIGHT,
    topMargin=TOP,
    bottomMargin=BOTTOM + 5 * mm,
    title="CV - Papa Mamadou Ndiaye (PAMAYE)",
    author="Papa Mamadou Ndiaye (PAMAYE)",
    subject="Régie diffusion, production et réalisation audiovisuelle",
)
frame = Frame(
    LEFT, BOTTOM + 5 * mm, CONTENT_W,
    PAGE_H - TOP - BOTTOM - 5 * mm,
    leftPadding=0, rightPadding=0, topPadding=0, bottomPadding=0,
    id="main"
)
doc.addPageTemplates([PageTemplate(id="cv", frames=[frame], onPage=on_page)])

story = []

# Masthead
header = Table(
    [[
        [
            para("PAPA MAMADOU NDIAYE", "CVName"),
            para("PAMAYE  |  AUDIOVISUEL · RÉGIE DIFFUSION · RÉALISATION EN DIRECT", "CVTagline"),
        ],
        para("<b>DAKAR, SÉNÉGAL</b><br/>+221 77 317 57 56<br/>ndiayepamaye@gmail.com", "CVContact")
    ]],
    colWidths=[CONTENT_W * 0.68, CONTENT_W * 0.32]
)
header.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), NAVY),
    ("TEXTCOLOR", (0, 0), (-1, -1), WHITE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 7 * mm),
    ("RIGHTPADDING", (0, 0), (-1, -1), 5 * mm),
    ("TOPPADDING", (0, 0), (-1, -1), 5 * mm),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 5 * mm),
]))
story.append(header)
story.append(Spacer(1, 3 * mm))

contact = Table([[
    para('<b>Portfolio</b> · <link href="https://pamayeprodact.github.io/portfolio-audiovisuel/" color="#8A641F">pamayeprodact.github.io/portfolio-audiovisuel</link>', "CVContact"),
    para('<b>Vidéo OMT</b> · <link href="https://youtu.be/0JjU11ekJU4?si=TbVAYpUiFr9tHINw" color="#8A641F">Coulisses Orange Music Talent</link>', "CVContact"),
]], colWidths=[CONTENT_W * .57, CONTENT_W * .43])
contact.setStyle(TableStyle([
    ("BACKGROUND", (0, 0), (-1, -1), PALE),
    ("BOX", (0, 0), (-1, -1), .4, LINE),
    ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
    ("LEFTPADDING", (0, 0), (-1, -1), 3 * mm),
    ("RIGHTPADDING", (0, 0), (-1, -1), 2 * mm),
    ("TOPPADDING", (0, 0), (-1, -1), 2.2 * mm),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 2.2 * mm),
]))
story.append(contact)
story.append(Spacer(1, 3 * mm))

story.extend(section("Profil professionnel"))
story.append(para(
    "Professionnel de l’audiovisuel à la 2STV depuis 2015, avec une expérience en régie diffusion, "
    "réalisation d’émissions et préparation de dispositifs de captation pour des directs et événements. "
    "A participé à des productions musicales, culturelles et institutionnelles au Sénégal et au Maroc. "
    "Développe également des compétences en communication digitale, gestion des réseaux sociaux et création de contenus.",
    "CVIntro"
))
story.append(Spacer(1, 2.5 * mm))

left = []
right = []

left.extend(section("Expérience professionnelle"))
left.append(para("2STV · Depuis 2015", "CVRole"))
left.append(para("Opérateur de régie diffusion et réalisation d’émissions", "CVSmall"))
left.append(bullet("Participation à l’exploitation de la régie diffusion, au suivi des sources vidéo et au contrôle multiview."))
left.append(bullet("Préparation technique et participation à la captation et à la réalisation de directs TV et d’événements."))
left.append(bullet("Contribution à des productions musicales, culturelles et institutionnelles."))
left.append(bullet("Utilisation des outils et équipements adaptés à la régie et au workflow de chaque production."))
left.append(Spacer(1, 1.2 * mm))
left.append(para("Orange Music Talent Sénégal (OMT)", "CVRole"))
left.append(para("Chargé de production à la 2STV · Réalisation des coulisses", "CVSmall"))
left.append(bullet("Chargé de production pour OMT et réalisation d’un contenu consacré aux coulisses de l’émission."))
left.append(para('<link href="https://youtu.be/0JjU11ekJU4?si=TbVAYpUiFr9tHINw" color="#8A641F">Voir la vidéo des coulisses OMT ↗</link>', "CVLink"))

left.extend(section("Réalisations sélectionnées"))
left.append(para("<b>Concert de Wally Seck</b> · Diourbel — régie de captation et réalisation du direct retransmis sur la 2STV.", "CVBody"))
left.append(para("<b>Finale Kaay Cover 2026</b> · Dakar — captation et réalisation en direct.", "CVBody"))
left.append(para("<b>Laylatoul Khadre</b> · Maroc, 2024 — mise en place de la régie et réalisation du direct.", "CVBody"))
left.append(para("<b>Inauguration de l’aéroport de Saint-Louis</b> — mission technique de captation et réalisation du direct.", "CVBody"))
left.append(para("<b>Vacances de ouf</b> — coordination des activités et des jeux, organisation du dispositif technique, régie de captation et participation à la réalisation audiovisuelle.", "CVBody"))
left.append(para('<link href="https://www.youtube.com/live/Vrk9NVsPKPA?si=fML6_rexH_WnVZgP" color="#8A641F">Concert Wally Seck ↗</link>  ·  <link href="https://www.youtube.com/live/2tRMub-wqKw?si=S64PllGszGI6YNdv" color="#8A641F">Kaay Cover ↗</link>  ·  <link href="https://youtu.be/olP9wP4LK2E" color="#8A641F">Laylatoul Khadre ↗</link>', "CVSmall"))

right.extend(section("Compétences audiovisuelles"))
right.append(bullet("Régie diffusion et suivi des sources."))
right.append(bullet("Réalisation d’émissions et directs TV."))
right.append(bullet("Captation événementielle et régie mobile."))
right.append(bullet("Préparation des dispositifs techniques et contrôle multiview."))
right.extend(section("Outils & environnements"))
right.append(para(
    "<b>Logiciels / diffusion :</b> OBS Studio, vMix, XTV Suite (AxelTech / Axel Technology).<br/>"
    "<b>Équipements / solutions vidéo :</b> Blackmagic Design, Sony, AJA.<br/>"
    "<b>Environnements :</b> systèmes de diffusion et playout, interfaces vidéo et acquisition, contrôle des sources et multiview.",
    "CVBody"
))
right.extend(section("Communication digitale"))
right.append(para(
    "Gestion et animation des réseaux sociaux · Planification éditoriale · Création de contenus numériques · "
    "Valorisation et promotion d’événements · Cohérence de l’image de marque.",
    "CVBody"
))
right.extend(section("Initiatives numériques"))
right.append(para("<b>PAMAYE PROD’ACT</b> — projet d’entreprise créative en audiovisuel et communication digitale.", "CVBody"))
right.append(para("<b>SEE SENEGAL</b> — concept de série promotionnelle sur la destination Sénégal.", "CVBody"))
right.append(para("<b>SENEGAL REK · TERANGA AI Concierge</b> — projet de plateforme numérique touristique.", "CVBody"))
right.append(para("<b>SUNU ZAP 3.0</b> et <b>KaF’Post</b> — concepts de services média et digitaux.", "CVBody"))
right.append(Spacer(1, 1.2 * mm))
right.append(para(
    "<i>Les projets personnels présentés correspondent à des initiatives et concepts à différents stades de développement.</i>",
    "CVSmall"
))

columns = Table([[left, right]], colWidths=[COLUMN_W, COLUMN_W])
columns.setStyle(TableStyle([
    ("VALIGN", (0, 0), (-1, -1), "TOP"),
    ("LEFTPADDING", (0, 0), (-1, -1), 0),
    ("RIGHTPADDING", (0, 0), (0, 0), GAP / 2),
    ("LEFTPADDING", (1, 0), (1, 0), GAP / 2),
    ("RIGHTPADDING", (1, 0), (1, 0), 0),
    ("TOPPADDING", (0, 0), (-1, -1), 0),
    ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
]))
story.append(columns)

doc.build(story)
print(f"CV PDF généré : {OUTPUT} ({OUTPUT.stat().st_size} octets)")
