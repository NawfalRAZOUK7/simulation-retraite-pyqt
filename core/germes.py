# core/germes.py

from core import logger

def _clamp_germe(val):
    """Force le germe à rester dans [1, 30000]"""
    if val is None or val == 0:
        return 1  # Valeur par défaut si None ou 0
    return max(1, min(val, 30000))

class GermesAlea:
    """
    Classe pour gérer la génération pseudo-aléatoire contrôlée via 3 germes IX, IY, IZ.
    Compatible avec les exigences du sujet de simulation discrète.
    """

    def __init__(self, IX, IY, IZ):
        """
        Initialise les germes. Logger un warning si un germe est None ou 0.
        Force les germes à rester dans [1, 30000].
        """
        self.IX = _clamp_germe(IX)
        self.IY = _clamp_germe(IY)
        self.IZ = _clamp_germe(IZ)
        if None in (IX, IY, IZ) or 0 in (IX, IY, IZ):
            logger.warning("Un ou plusieurs germes étaient None ou 0 à l'initialisation : IX=%s, IY=%s, IZ=%s. Correction automatique appliquée.", IX, IY, IZ)
        else:
            logger.info("GermesAlea initialisés : IX=%d, IY=%d, IZ=%d", self.IX, self.IY, self.IZ)

    def alea(self):
        """
        Génère un float pseudo-aléatoire [0,1[ avec incrément des germes (méthode classique).
        Log un warning si les germes n'ont pas été initialisés correctement.
        Force les germes à rester dans [1, 30000] après chaque itération.
        """
        if None in (self.IX, self.IY, self.IZ) or 0 in (self.IX, self.IY, self.IZ):
            logger.warning("Appel à alea() avec germes invalides : IX=%s, IY=%s, IZ=%s", self.IX, self.IY, self.IZ)
            self.IX, self.IY, self.IZ = _clamp_germe(self.IX), _clamp_germe(self.IY), _clamp_germe(self.IZ)
            return 0.5  # Valeur neutre pour éviter le crash

        # Algorithme congruentiel triple pour [0,1[
        self.IX = (171 * self.IX) % 30269
        self.IY = (172 * self.IY) % 30307
        self.IZ = (170 * self.IZ) % 30323

        # Clamp des germes après calcul pour éviter tout débordement ou mauvaise valeur
        self.IX = _clamp_germe(self.IX)
        self.IY = _clamp_germe(self.IY)
        self.IZ = _clamp_germe(self.IZ)

        r = (self.IX/30269.0 + self.IY/30307.0 + self.IZ/30323.0) % 1.0
        if not (0 <= r < 1):
            logger.warning("Valeur de alea() hors bornes [0,1[: r=%s", r)
        return r

    def get_germes(self):
        """
        Retourne les germes courants sous forme de tuple.
        """
        return self.IX, self.IY, self.IZ

    def set_germes(self, IX, IY, IZ):
        """
        Met à jour les germes. Log l'action.
        Clamp les germes dans [1, 30000].
        """
        self.IX = _clamp_germe(IX)
        self.IY = _clamp_germe(IY)
        self.IZ = _clamp_germe(IZ)
        logger.info("Mise à jour des germes : IX=%d, IY=%d, IZ=%d", self.IX, self.IY, self.IZ)

    def next_germes(self, inc=5):
        """
        Incrémente chaque germe d'une valeur donnée (par défaut 5) pour diversifier les runs.
        Log l'action.
        Clamp les germes dans [1, 30000] après incrément.
        """
        self.IX = _clamp_germe(self.IX + inc)
        self.IY = _clamp_germe(self.IY + inc)
        self.IZ = _clamp_germe(self.IZ + inc)
        logger.debug("Germes incrémentés de %d : IX=%d, IY=%d, IZ=%d", inc, self.IX, self.IY, self.IZ)

# Exemple d'utilisation :
# g = GermesAlea(100, 200, 300)
# rnd = g.alea()
# g.next_germes()
# print(g.get_germes())
