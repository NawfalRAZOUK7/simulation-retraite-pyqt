import os
import pandas as pd

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QToolBar, QShortcut, QFileDialog, QHBoxLayout
)
from PyQt5.QtGui import QIcon, QKeySequence
from PyQt5.QtCore import Qt

from ui.charts_window import TabReserve, TabComparaison, TabConfidence
from ui.dialogs import (
    show_error,
    show_info,
    validate_required_columns,
    show_preview_dataframe,
    confirm_export_success,
    confirm_export_failure,
)
from ui.theme import get_custom_palette, get_dark_palette
from utils.mpl_theme import set_mpl_theme
from utils.theme_utils import load_theme_pref, save_theme_pref

from utils.pdf_export import export_report_to_pdf
from ui.widgets.report_export_dialog import ReportExportDialog
from ui.widgets.animated_tool_button import AnimatedToolButton
from ui.widgets.fade_tab_widget import FadeTabWidget  # <--- NEW!

REQUIRED_COLUMNS = {"Annee", "Reserve", "Simulation"}
ASSETS_DIR = "assets"  # Place tes icônes sun.png et moon.png ici

class ChartsWindow(QMainWindow):
    def __init__(self, parent=None, data=None, data_scenarios=None):
        super().__init__(parent)
        self.dark_mode = load_theme_pref()
        self.setWindowTitle("Graphiques de Simulation")
        self.setGeometry(270, 270, 1000, 700)
        self.data = data  # DataFrame principal (réserve, etc.)
        self.data_scenarios = data_scenarios or {}  # Dictionnaire : nom_scénario -> DataFrame
        self.init_ui()
        self.apply_theme()  # Palette Qt & Matplotlib

        # --- RACCOURCIS CLAVIER ---
        self._add_shortcuts()

    def init_ui(self):
        # --- Toolbar principale (modern style + animated buttons) ---
        self.toolbar = QToolBar("Barre d'outils graphique")
        self.toolbar.setMovable(False)
        self.toolbar.setStyleSheet("""
            QToolBar {
                background: #f6f7fb;
                border: none;
                spacing: 2px;
                padding: 3px 8px;
                border-radius: 14px;
                box-shadow: 0px 3px 10px #dde1ee;
            }
        """)
        self.addToolBar(Qt.TopToolBarArea, self.toolbar)

        tool_btns = []

        # Enregistrer le graphique
        btn_save = AnimatedToolButton()
        btn_save.setIcon(QIcon("assets/save_icon.png") if os.path.exists("assets/save_icon.png") else QIcon())
        btn_save.setToolTip("Enregistrer le graphique affiché (Ctrl+S)")
        btn_save.clicked.connect(self.save_current_graphic)
        tool_btns.append(btn_save)

        # Importer un CSV
        btn_import = AnimatedToolButton()
        btn_import.setIcon(QIcon("assets/import_icon.png") if os.path.exists("assets/import_icon.png") else QIcon())
        btn_import.setToolTip("Importer un CSV… (Ctrl+O)")
        btn_import.clicked.connect(self.import_csv)
        tool_btns.append(btn_import)

        # Exporter rapport PDF
        btn_export_pdf = AnimatedToolButton()
        btn_export_pdf.setIcon(QIcon("assets/pdf_icon.png") if os.path.exists("assets/pdf_icon.png") else QIcon())
        btn_export_pdf.setToolTip("Exporter rapport PDF…")
        btn_export_pdf.clicked.connect(self.export_pdf_report)
        tool_btns.append(btn_export_pdf)

        # Basculer le mode sombre/clair
        dark_icon = "sun.png" if self.dark_mode else "moon.png"
        btn_toggle_dark = AnimatedToolButton()
        btn_toggle_dark.setIcon(QIcon(os.path.join(ASSETS_DIR, dark_icon)))
        btn_toggle_dark.setToolTip("Basculer mode sombre/clair")
        btn_toggle_dark.clicked.connect(self.toggle_dark_mode)
        tool_btns.append(btn_toggle_dark)

        # Add all animated buttons to toolbar
        for btn in tool_btns:
            self.toolbar.addWidget(btn)

        # --- Widget central avec onglets (FadeTabWidget instead of QTabWidget) ---
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)

        # ===== INFO-BAR UX Graphiques =====
        infobar = QLabel(
            "<div style='color:#666; background:#f6f7fb; border-radius:7px; padding:7px 18px; margin-bottom:6px;'>"
            "<b>Astuce :</b> "
            "Molette pour zoomer/dézoomer · glisser pour déplacer la vue · "
            "double-clic pour réinitialiser · clic droit pour le menu contextuel · "
            "survol des points = infos · barre Matplotlib ci-dessous pour pan/zoom/export.<br>"
            "<i>Essayez aussi les boutons bonus (export, crosshair, brush, etc.).</i>"
            "</div>"
        )
        infobar.setWordWrap(True)
        layout.addWidget(infobar)

        # ===== INFO-BAR FILTRES/EXPORT =====
        exportbar = QLabel(
            "<div style='color:#417505; background:#e6fbe2; border-radius:7px; padding:7px 18px; margin-bottom:8px;'>"
            "<b>⚠️ Export CSV :</b> "
            "Les filtres actifs s’appliquent aussi lors de l’export. Vous exportez uniquement la <b>vue filtrée</b> affichée ci-dessous (et non toutes les données brutes).<br>"
            "<i>Astuce : Utilisez les filtres dynamiques au-dessus des graphiques pour personnaliser votre export.</i>"
            "</div>"
        )
        exportbar.setWordWrap(True)
        layout.addWidget(exportbar)

        # --- Tabs: use FadeTabWidget (auto fade-in on tab switch) ---
        from ui.widgets.fade_tab_widget import FadeTabWidget
        self.tabs = FadeTabWidget(duration=340)  # smooth fade
        layout.addWidget(self.tabs)

        # Label d’aperçu DataFrame (après import)
        self.preview_label = QLabel()
        layout.addWidget(self.preview_label)
        self.preview_label.hide()

        self.refresh_tabs(self.data, self.data_scenarios)

    def _add_shortcuts(self):
        """Ajoute tous les raccourcis clavier principaux à la fenêtre."""
        # Navigation onglet suivant/précédent
        QShortcut(QKeySequence("Ctrl+Right"), self, activated=lambda: self.tabs.setCurrentIndex((self.tabs.currentIndex() + 1) % self.tabs.count()))
        QShortcut(QKeySequence("Ctrl+Left"), self, activated=lambda: self.tabs.setCurrentIndex((self.tabs.currentIndex() - 1) % self.tabs.count()))
        # Sauvegarde rapide du graphique courant
        QShortcut(QKeySequence("Ctrl+S"), self, activated=self.save_current_graphic)
        # Import CSV rapide
        QShortcut(QKeySequence("Ctrl+O"), self, activated=self.import_csv)

    def refresh_tabs(self, data, data_scenarios):
        """Recharge tous les onglets à partir des nouvelles données."""
        self.tabs.clear()

        # Onglet "Réserve sur 11 ans"
        if data is not None and isinstance(data, pd.DataFrame):
            self.tab_reserve = TabReserve(data)
        else:
            self.tab_reserve = QWidget()
            layout1 = QVBoxLayout(self.tab_reserve)
            layout1.addWidget(QLabel("Aucune donnée à afficher pour la réserve."))

        # Onglet "Intervalles de confiance"
        if data is not None and isinstance(data, pd.DataFrame):
            self.tab_confidence = TabConfidence(data)
        else:
            self.tab_confidence = QWidget()
            layout2 = QVBoxLayout(self.tab_confidence)
            layout2.addWidget(QLabel("Aucune donnée à afficher pour les intervalles de confiance."))

        # Onglet "Comparaison scénarios"
        if data_scenarios is not None and isinstance(data_scenarios, dict) and len(data_scenarios) > 0:
            self.tab_comparaison = TabComparaison(data_scenarios)
        else:
            self.tab_comparaison = QWidget()
            layout3 = QVBoxLayout(self.tab_comparaison)
            layout3.addWidget(QLabel("Aucune donnée de comparaison multi-scénarios."))

        self.tabs.addTab(self.tab_reserve, "Réserve sur 11 ans")
        self.tabs.addTab(self.tab_comparaison, "Comparaison scénarios")
        self.tabs.addTab(self.tab_confidence, "Intervalles de confiance")

    # ----- FONCTIONS GRAPHIQUES & CSV -----
    def save_current_graphic(self):
        """Appelle la méthode de sauvegarde du graphique de l'onglet actif (si dispo)."""
        widget = self.tabs.currentWidget()
        if hasattr(widget, 'save_graphic'):
            widget.save_graphic()
        else:
            show_info(self, "Aucun graphique exportable sur cet onglet.")

    def import_csv(self):
        """Ouvre un QFileDialog pour importer un CSV, le charge et valide les colonnes."""
        path, _ = QFileDialog.getOpenFileName(
            self, "Importer un CSV de simulation", "", "Fichiers CSV (*.csv);;Tous les fichiers (*)"
        )
        if not path:
            return
        try:
            df = pd.read_csv(path)
        except Exception as e:
            show_error(self, "Erreur d'import", f"Impossible de lire le CSV :\n{str(e)}")
            return

        ok, missing = validate_required_columns(df, REQUIRED_COLUMNS)
        if not ok:
            show_error(
                self,
                "CSV invalide",
                f"Le fichier doit contenir les colonnes : {', '.join(REQUIRED_COLUMNS)}\n"
                f"Colonnes manquantes : {', '.join(missing)}"
            )
            return

        self.data = df
        self.data_scenarios = None  # Reset, let parent logic handle multi-scenarios
        self.refresh_tabs(self.data, self.data_scenarios)
        self.preview_label.setText("<b>Aperçu des données importées :</b>")
        self.preview_label.show()
        show_preview_dataframe(self, df, n_rows=5)
        show_info(self, "Import réussi", f"Fichier CSV importé avec succès :\n{os.path.basename(path)}")

    # ----- PDF REPORT EXPORT -----
    def export_pdf_report(self):
        """Affiche le dialog, collecte les choix, génère le rapport PDF."""
        dlg = ReportExportDialog(self)
        if dlg.exec_():
            pdf_path, sections = dlg.get_result()
            if not pdf_path or not sections:
                return

            try:
                figures = []
                if "figures" in sections:
                    for tab in [getattr(self, n, None) for n in ["tab_reserve", "tab_confidence", "tab_comparaison"]]:
                        if hasattr(tab, "figure"):
                            figures.append(tab.figure)
                stats = None
                if "stats" in sections:
                    stats = {
                        "nb_scenarios": len(self.data_scenarios) if self.data_scenarios else 0,
                        "total_lignes": len(self.data) if isinstance(self.data, pd.DataFrame) else 0,
                    }
                summary = None
                if "summary" in sections:
                    summary = (
                        "Rapport de simulation de réserve et comparaisons.\n"
                        "Ce rapport a été généré automatiquement par l’application, "
                        "en fonction des options sélectionnées."
                    )
                ok, err = export_report_to_pdf(
                    figures=figures,
                    stats=stats,
                    summary=summary,
                    sections=sections,
                    path=pdf_path,
                )
                if ok:
                    confirm_export_success(pdf_path, parent=self)
                else:
                    confirm_export_failure(pdf_path, err, parent=self)
            except Exception as e:
                show_error(self, f"Erreur lors de l’export PDF :\n{e}")

    # ----- DARK MODE / LIGHT MODE -----
    def toggle_dark_mode(self):
        """Bascule entre mode sombre/clair et met à jour l’UI + matplotlib."""
        self.dark_mode = not self.dark_mode
        self.apply_theme()
        save_theme_pref(self.dark_mode)
        dark_icon = "sun.png" if self.dark_mode else "moon.png"
        # Change icon for the dark mode toggle button
        btn = None
        for widget in self.toolbar.findChildren(AnimatedToolButton):
            if widget.toolTip().startswith("Basculer mode sombre/clair"):
                btn = widget
                break
        if btn:
            btn.setIcon(QIcon(os.path.join(ASSETS_DIR, dark_icon)))
        self.redraw_all()

    def apply_theme(self):
        """Applique le thème actuel (palette Qt + matplotlib)."""
        from PyQt5.QtWidgets import QApplication
        palette = get_dark_palette() if self.dark_mode else get_custom_palette()
        QApplication.instance().setPalette(palette)
        set_mpl_theme(dark_mode=self.dark_mode)

    def redraw_all(self):
        """Redessine tous les onglets graphiques pour refléter le thème."""
        for tab in [getattr(self, n, None) for n in ["tab_reserve", "tab_confidence", "tab_comparaison"]]:
            if hasattr(tab, 'plot_reserve'):
                tab.plot_reserve()
            if hasattr(tab, 'plot_confidence'):
                tab.plot_confidence()
            if hasattr(tab, 'plot_comparaison'):
                tab.plot_comparaison()
        self.update()
