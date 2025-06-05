"""
plot_helpers.py
UX Ultimate — Matplotlib & PyQtGraph for PyQt
- Tooltips, sélection, click, export
- Brush/zoom zone, synchronisation de graphes, crosshair, context-menu
- Double-clic reset zoom, infobox dynamique, popup légende
- Lignes de référence dynamiques
"""

# ===== MATPLOTLIB BONUS =====

def mpl_add_tooltips(figure, ax, x, y, labels=None, fmt="({x}, {y})", precision=0):
    """
    Tooltips dynamiques sur survol de points matplotlib.
    """
    scatter = ax.scatter(x, y, s=38, color="#2077B4", zorder=5, picker=8)
    annot = ax.annotate("", xy=(0,0), xytext=(12,12), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="#fffbe8", ec="#707070"),
                        arrowprops=dict(arrowstyle="->"),
                        fontsize=10, visible=False)
    def update_annot(ind):
        idx = ind["ind"][0]
        _x, _y = x[idx], y[idx]
        annot.xy = (_x, _y)
        if labels:
            annot.set_text(labels[idx])
        else:
            annot.set_text(fmt.format(x=round(_x, precision), y=round(_y, precision)))
        annot.set_visible(True)
    def on_motion(event):
        vis = annot.get_visible()
        if event.inaxes == ax:
            cont, ind = scatter.contains(event)
            if cont:
                update_annot(ind)
                figure.canvas.draw_idle()
            elif vis:
                annot.set_visible(False)
                figure.canvas.draw_idle()
        elif vis:
            annot.set_visible(False)
            figure.canvas.draw_idle()
    figure.canvas.mpl_connect("motion_notify_event", on_motion)

def mpl_add_click_callback(figure, ax, callback):
    """
    Callback sur click de point matplotlib (utilisé pour afficher infos custom).
    """
    scatter = ax.collections[0] if ax.collections else None
    if not scatter: return
    def onclick(event):
        if event.inaxes == ax:
            cont, ind = scatter.contains(event)
            if cont and ind["ind"]:
                idx = ind["ind"][0]
                x, y = scatter.get_offsets()[idx]
                callback(x, y, idx, event)
    figure.canvas.mpl_connect("button_press_event", onclick)

def mpl_add_export_button(figure, canvas, filename_default="export_graphique.png"):
    """
    Ajoute un bouton d'export image (PNG/PDF/SVG) du graphique matplotlib.
    """
    from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
    btn = QPushButton("Exporter l'image")
    def export_graph():
        path, _ = QFileDialog.getSaveFileName(
            canvas.parent() if hasattr(canvas, "parent") else None,
            "Exporter le graphique",
            filename_default,
            "PNG (*.png);;PDF (*.pdf);;SVG (*.svg)"
        )
        if path:
            try:
                figure.savefig(path)
                QMessageBox.information(canvas.parent(), "Succès", f"Graphique exporté :\n{path}")
            except Exception as e:
                QMessageBox.critical(canvas.parent(), "Erreur", f"Erreur export :\n{str(e)}")
    btn.clicked.connect(export_graph)
    # Ajoute dynamiquement (ne duplique pas si déjà présent)
    if hasattr(canvas.parent(), "layout"):
        canvas.parent().layout().addWidget(btn)
    return btn

def mpl_add_reference_line(ax, x=None, y=None, color="#C44D58", label=None):
    """
    Ajoute une ligne de référence verticale/horizontale.
    """
    if x is not None:
        ax.axvline(x, color=color, linestyle="--", lw=1.4, label=label)
    if y is not None:
        ax.axhline(y, color=color, linestyle="--", lw=1.4, label=label)

def mpl_add_brush_zoom(figure, ax, on_select=None):
    """
    "Brush zoom" zone rectangulaire avec sélection (matplotlib natif).
    """
    from matplotlib.widgets import RectangleSelector
    def onselect(eclick, erelease):
        ax.set_xlim(eclick.xdata, erelease.xdata)
        ax.set_ylim(eclick.ydata, erelease.ydata)
        figure.canvas.draw_idle()
        if on_select: on_select(eclick, erelease)
    rs = RectangleSelector(ax, onselect, drawtype='box', useblit=True,
                           button=[1],  # Only left click
                           minspanx=5, minspany=5, spancoords='pixels',
                           interactive=True)
    return rs

def mpl_add_crosshair(figure, ax):
    """
    Affiche un crosshair qui suit la souris sur le graphique matplotlib.
    """
    import matplotlib.lines as mlines
    vline = mlines.Line2D([], [], color='#C44D58', linestyle='--', lw=1, alpha=0.6)
    hline = mlines.Line2D([], [], color='#C44D58', linestyle='--', lw=1, alpha=0.6)
    ax.add_line(vline)
    ax.add_line(hline)
    def mouse_move(event):
        if not event.inaxes: return
        vline.set_data([event.xdata, event.xdata], ax.get_ylim())
        hline.set_data(ax.get_xlim(), [event.ydata, event.ydata])
        figure.canvas.draw_idle()
    figure.canvas.mpl_connect('motion_notify_event', mouse_move)

def mpl_add_doubleclick_reset(figure, ax, orig_xlim, orig_ylim):
    """
    Double-clic pour reset le zoom (UX pro).
    """
    def ondbl(event):
        if event.dblclick and event.inaxes == ax:
            ax.set_xlim(orig_xlim)
            ax.set_ylim(orig_ylim)
            figure.canvas.draw_idle()
    figure.canvas.mpl_connect('button_press_event', ondbl)

def mpl_add_context_menu(figure, ax, items):
    """
    Menu contextuel (clic droit) sur matplotlib.
    """
    from PyQt5.QtWidgets import QMenu
    def context_menu(event):
        if event.button == 3:
            menu = QMenu()
            for (label, callback) in items:
                act = menu.addAction(label)
                act.triggered.connect(lambda _=None, cb=callback: cb())
            menu.exec_(figure.canvas.mapToGlobal(figure.canvas.cursor().pos()))
    figure.canvas.mpl_connect('button_press_event', context_menu)

def mpl_infobox(ax, text, xy, color="#2077B4"):
    """
    Affiche une infobox temporaire.
    """
    return ax.annotate(
        text, xy=xy, xytext=(12,18), textcoords='offset points',
        bbox=dict(boxstyle="round", fc=color, ec="white"),
        color="white", fontsize=10, zorder=10
    )

def mpl_add_legend_popup(figure, ax):
    """
    Popup dynamique sur la légende (bonus UX).
    """
    legend = ax.get_legend()
    if legend:
        def on_hover(event):
            if event.inaxes == ax and legend.contains(event)[0]:
                legend.set_frame_on(True)
                legend.get_frame().set_facecolor("#f8fbff")
                figure.canvas.draw_idle()
            else:
                legend.set_frame_on(False)
                figure.canvas.draw_idle()
        figure.canvas.mpl_connect("motion_notify_event", on_hover)

# ===== PYQTGRAPH BONUS =====

def pg_add_tooltips(plotwidget, x_data, y_data, fmt="({x}, {y})"):
    import pyqtgraph as pg
    spots = [{'pos': (x, y), 'data': (x, y)} for x, y in zip(x_data, y_data)]
    scatter = pg.ScatterPlotItem(
        spots=spots,
        symbol='o',
        size=11,
        brush=pg.mkBrush("#2077B4"),
        hoverable=True
    )
    plotwidget.addItem(scatter)
    def on_hover(event):
        if event.isExit():
            plotwidget.setToolTip("")
            return
        points = event.points()
        if points:
            x, y = points[0].pos()
            plotwidget.setToolTip(fmt.format(x=int(x), y=int(y)))
        else:
            plotwidget.setToolTip("")
    scatter.hoverEvent = on_hover

def pg_add_click_callback(plotwidget, callback):
    import pyqtgraph as pg
    for item in plotwidget.listDataItems():
        if isinstance(item, pg.ScatterPlotItem):
            def on_click(plot, points):
                if points:
                    x, y = points[0].pos()
                    idx = points[0].index()
                    callback(x, y, idx, None)
            item.sigClicked.connect(on_click)

def pg_add_export_button(parent_widget, plotwidget, filename="export_graphique.csv"):
    from PyQt5.QtWidgets import QPushButton, QFileDialog, QMessageBox
    import pandas as pd
    btn = QPushButton("Exporter données")
    def export_data():
        data_items = plotwidget.listDataItems()
        for item in data_items:
            if hasattr(item, 'getData'):
                x, y = item.getData()
                df = pd.DataFrame({'x': x, 'y': y})
                path, _ = QFileDialog.getSaveFileName(parent_widget, "Exporter CSV", filename, "CSV (*.csv)")
                if path:
                    df.to_csv(path, index=False)
                    QMessageBox.information(parent_widget, "Succès", f"Données exportées :\n{path}")
                break
    btn.clicked.connect(export_data)
    parent_widget.layout().addWidget(btn)
    return btn

def pg_add_reference_line(plotwidget, x=None, y=None, color="#C44D58", label=None):
    import pyqtgraph as pg
    if x is not None:
        vline = pg.InfiniteLine(pos=x, angle=90, pen=pg.mkPen(color, width=2, style=pg.QtCore.Qt.DashLine))
        plotwidget.addItem(vline)
    if y is not None:
        hline = pg.InfiniteLine(pos=y, angle=0, pen=pg.mkPen(color, width=2, style=pg.QtCore.Qt.DashLine))
        plotwidget.addItem(hline)

def pg_add_brush_selection(plotwidget, callback):
    import pyqtgraph as pg
    roi = pg.RectROI([1,1],[2,2], pen=pg.mkPen('r', width=2))
    plotwidget.addItem(roi)
    roi.sigRegionChanged.connect(lambda: callback(roi.getArraySlice(plotwidget.plotItem.dataItems[0].getData(), plotwidget.image, roi)))
    return roi

def pg_add_crosshair(plotwidget):
    import pyqtgraph as pg
    vline = pg.InfiniteLine(angle=90, movable=False, pen=pg.mkPen('#C44D58', style=pg.QtCore.Qt.DashLine))
    hline = pg.InfiniteLine(angle=0, movable=False, pen=pg.mkPen('#C44D58', style=pg.QtCore.Qt.DashLine))
    plotwidget.addItem(vline)
    plotwidget.addItem(hline)
    def mouseMoved(evt):
        pos = evt[0]
        if plotwidget.sceneBoundingRect().contains(pos):
            mousePoint = plotwidget.plotItem.vb.mapSceneToView(pos)
            vline.setPos(mousePoint.x())
            hline.setPos(mousePoint.y())
    plotwidget.scene().sigMouseMoved.connect(mouseMoved)

def pg_add_context_menu(plotwidget, actions):
    from PyQt5.QtWidgets import QMenu
    def contextMenuEvent(event):
        menu = QMenu()
        for label, callback in actions:
            action = menu.addAction(label)
            action.triggered.connect(lambda _=None, cb=callback: cb())
        menu.exec_(event.screenPos().toPoint())
    plotwidget.setContextMenuPolicy(plotwidget.CustomContextMenu)
    plotwidget.contextMenuEvent = contextMenuEvent

def pg_add_infobox(plotwidget, text, pos, color="#2077B4"):
    import pyqtgraph as pg
    label = pg.TextItem(text, color=color)
    label.setPos(*pos)
    plotwidget.addItem(label)
    return label

def pg_sync_zooms(widgets):
    """
    Synchronise le zoom/pan entre plusieurs plotwidgets pyqtgraph.
    """
    if not widgets:
        return
    ref = widgets[0].plotItem
    for w in widgets[1:]:
        w.plotItem.setXLink(ref)
        w.plotItem.setYLink(ref)

# === UTILS ===

def nice_tick_formatter(val):
    absval = abs(val)
    if absval >= 1_000_000:
        return f"{val/1_000_000:.1f}M"
    elif absval >= 1_000:
        return f"{val/1_000:.1f}k"
    else:
        return str(val)

# ==== PDF EXPORT BONUS ====

def get_figures_from_tabs(tabs, tab_names=("tab_reserve", "tab_comparaison", "tab_confidence")):
    """
    Retourne une liste de Figure matplotlib actuellement affichées dans les onglets.
    - tabs: le QTabWidget ou un dict des objets tab.
    - tab_names: noms d'attributs à chercher (par défaut ceux du charts_window).
    Utilisé pour les exports PDF (matplotlib.backends.backend_pdf).
    """
    figures = []
    for name in tab_names:
        tab = getattr(tabs, name, None) if hasattr(tabs, name) else None
        if tab and hasattr(tab, "figure"):
            fig = getattr(tab, "figure")
            if fig:  # Peut tester isinstance(fig, matplotlib.figure.Figure) si besoin
                figures.append(fig)
    return figures

def get_figures_from_tabwidgets(qtabwidget):
    """
    Version alternative : parcours un QTabWidget (ex: self.tabs) et extrait toutes les Figure des widgets.
    """
    figures = []
    for i in range(qtabwidget.count()):
        tab = qtabwidget.widget(i)
        if hasattr(tab, "figure"):
            fig = getattr(tab, "figure")
            if fig:
                figures.append(fig)
    return figures

# ==== EXEMPLES ====
"""
# Matplotlib (dans ta Tab) :
mpl_add_tooltips(figure, ax, x, y, fmt="Année: {x} - Réserve: {y} DH")
mpl_add_click_callback(figure, ax, lambda x, y, idx, evt: print(f"Clique sur {x},{y}"))
mpl_add_export_button(figure, canvas)
mpl_add_reference_line(ax, y=0)
mpl_add_brush_zoom(figure, ax)
mpl_add_crosshair(figure, ax)
mpl_add_doubleclick_reset(figure, ax, orig_xlim, orig_ylim)
mpl_add_context_menu(figure, ax, [("Exporter", ...), ("Réinitialiser", ...)])
mpl_add_legend_popup(figure, ax)

# PyQtGraph :
pg_add_tooltips(pgwidget, x, y)
pg_add_click_callback(pgwidget, lambda x, y, idx, evt: print(f"Clique sur {x},{y}"))
pg_add_export_button(self, pgwidget)
pg_add_reference_line(pgwidget, y=0)
pg_add_brush_selection(pgwidget, lambda sel: print("Sélection", sel))
pg_add_crosshair(pgwidget)
pg_add_context_menu(pgwidget, [("Exporter", ...), ("Reset", ...)])
pg_sync_zooms([pgwidget1, pgwidget2])
pg_add_infobox(pgwidget, "Texte Info", (x, y))

# Récupérer les figures pour PDF export :
from ui.widgets import plot_helpers

# 1. Si tu as un objet charts_window:
figures = plot_helpers.get_figures_from_tabs(self)

# 2. Si tu as un QTabWidget :
figures = plot_helpers.get_figures_from_tabwidgets(self.tabs)

# Ensuite : utilise matplotlib.backends.backend_pdf pour export, ou passes-les à ta logique PDF.
"""
