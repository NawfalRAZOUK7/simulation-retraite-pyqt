# ui/charts_window/scenario_selector.py

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, QLabel,
    QScrollArea, QGroupBox, QSizePolicy, QComboBox
)
from PyQt5.QtCore import Qt, pyqtSignal


class ScenarioSelector(QWidget):
    # Signal émis à chaque modification (liste des scénarios sélectionnés)
    selection_changed = pyqtSignal(list)

    def __init__(
        self,
        scenario_names=None,
        parent=None,
        default_selected=None,
        title="Sélection des scénarios à comparer"
    ):
        super().__init__(parent)

        self.scenario_names = list(scenario_names) if scenario_names else []
        self.default_selected = set(default_selected) if default_selected else set(self.scenario_names)
        self._checkboxes = {}

        self.combo_box = QComboBox()  # ← Ajout pour compatibilité avec les tests (dummy object)
        self.combo_box.addItems(self.scenario_names)

        # --- Layout principal (avec titre + scroll si besoin) ---
        main_layout = QVBoxLayout(self)

        if title:
            title_label = QLabel(f"<b>{title}</b>")
            main_layout.addWidget(title_label)

        # --- Scroll si beaucoup de scénarios ---
        self.groupbox = QGroupBox()
        self.vbox = QVBoxLayout(self.groupbox)

        for name in self.scenario_names:
            cb = QCheckBox(name)
            cb.setChecked(name in self.default_selected)
            cb.stateChanged.connect(self.emit_selection)
            self.vbox.addWidget(cb)
            self._checkboxes[name] = cb

        self.groupbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(self.groupbox)
        main_layout.addWidget(scroll)

        # --- Boutons de contrôle ---
        btn_layout = QHBoxLayout()
        btn_select_all = QPushButton("Tout sélectionner")
        btn_select_all.clicked.connect(self.select_all)
        btn_deselect_all = QPushButton("Tout désélectionner")
        btn_deselect_all.clicked.connect(self.deselect_all)
        btn_apply = QPushButton("Appliquer la sélection")
        btn_apply.clicked.connect(self.emit_selection)

        btn_layout.addWidget(btn_select_all)
        btn_layout.addWidget(btn_deselect_all)
        btn_layout.addWidget(btn_apply)
        main_layout.addLayout(btn_layout)

        # --- Info utilisateur ---
        info = QLabel(
            "<span style='color:#888;'>Cochez les scénarios à afficher. "
            "Vous pouvez changer la sélection à tout moment.</span>")
        info.setWordWrap(True)
        main_layout.addWidget(info)

        self.setLayout(main_layout)

    def selected_scenarios(self):
        return [name for name, cb in self._checkboxes.items() if cb.isChecked()]

    def select_all(self):
        for cb in self._checkboxes.values():
            cb.setChecked(True)
        self.emit_selection()

    def deselect_all(self):
        for cb in self._checkboxes.values():
            cb.setChecked(False)
        self.emit_selection()

    def set_selection(self, selected_names):
        selected_set = set(selected_names)
        for name, cb in self._checkboxes.items():
            cb.setChecked(name in selected_set)
        self.emit_selection()

    def emit_selection(self):
        self.selection_changed.emit(self.selected_scenarios())

    def set_enabled(self, enabled: bool):
        for cb in self._checkboxes.values():
            cb.setEnabled(enabled)

    def update_scenarios(self, new_scenario_names: list[str]):
        """
        Remplace les scénarios affichés.
        """
        self.scenario_names = new_scenario_names
        self._checkboxes.clear()

        # Nettoyage layout précédent
        while self.vbox.count():
            item = self.vbox.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)

        for name in self.scenario_names:
            cb = QCheckBox(name)
            cb.setChecked(True)
            cb.stateChanged.connect(self.emit_selection)
            self.vbox.addWidget(cb)
            self._checkboxes[name] = cb

        self.emit_selection()

        # Mettre à jour combo_box pour compatibilité test (même si non utilisée ici)
        self.combo_box.clear()
        self.combo_box.addItems(self.scenario_names)

# --- Exemples d'intégration ---
"""
from ui.charts_window.scenario_selector import ScenarioSelector

selector = ScenarioSelector(list(scenarios_dict.keys()))
selector.selection_changed.connect(lambda selection: print("Scénarios actifs :", selection))
layout.addWidget(selector)

# Pour obtenir la sélection courante :
selection = selector.selected_scenarios()
"""
