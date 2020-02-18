# -*- coding: utf-8 -*-

from collections import namedtuple
from itertools import product
from math import sqrt


class Rating:

    def __init__(self, map, wifi_range):
        self._map = map
        self._wifi_range = wifi_range
        self._reachables_map = []
        self.scoring_map = []

        # on value la carte une seule fois, à l'instanciation
        self._evaluate_map()

    @staticmethod
    def sort_coordinates_by_increasing_dist_to_source(coordinates, src):
        """
        Retourne la liste des coordonnées triées [loin...proche] de src

        :param coordinates: set(Pos(x,y)) ensemble de coordonnées à trier
        :param src: Pos(x,y) point de référence
        :return: les coordonnées de la plus lointaine à la plus proche
        :rtype: list(Pos(x,y))
        """

        coos = list(coordinates)
        coos.sort(
            key=lambda coo: sqrt((coo.x - src.x) ** 2 + (coo.y - src.y) ** 2))
        coos.reverse()

        return coos

    @staticmethod
    def gen_rec_coos(a, b):
        """
        Génère l'ensemble des coordonnées des cases d'un rectangle.

        :param a: Pos(x,y) un coin
        :param b: Pos(x,y) le coin opposé
        :return: set(Pos(x,y)) coordonnées de toutes les cases
        """

        xs = [x for x in range(min(a.x, b.x), max(a.x, b.x))]
        ys = [y for y in range(min(a.y, b.y), max(a.y, b.y))]

        return set(product(xs, ys))

    def keep_reachable_in_rectangle(self, coos, src):
        """
        Conserve l'ensemble des coordonnées atteignables à partir de la source.

        :param coos: set(Pos(x,y)) ens des coos d'un rectangle à filtrer
        :param src: l'emplacement de la borne wifi
        :return: un set contenant seulement les coordonnées atteignables
        """

        reachable_ones = set()
        coos = Rating.sort_coordinates_by_increasing_dist_to_source(coos, src)
        rectangle_finished = False

        # pour chaque case, on vérifie si elle est atteignable
        for index, coo in enumerate(coos):

            if self._map.cells[coo.x][coo.y].is_target:

                wall_present = False
                for coo2check in self.gen_rec_coos(coo2check, src):
                    if self._map.cells[coo2check.x][coo2check.y].is_wall():
                        wall_present = True
                    if wall_present:
                        break

                # il n'y a pas de mur
                if not wall_present:

                    # on est une case en diagonale
                    # on va pouvoir ajouter toutes les cases d'ici à la source
                    # plus besoin de vérifier les cases une à une
                    # ce rectangle est terminé !
                    if abs(src.x - coo.x) == abs(src.y - coo.y):
                        reachable_ones |= set(coos[index:])
                        rectangle_finished = True

                    # autre case (ajout aussi de la case en diagonale)
                    reachable_ones.add(coo2check)

            if rectangle_finished:
                break

        return reachable_ones

    def reachable_cells(self, src):
        """
        Donne les cellules atteignables cibles selon la propagation wifi.

        Principe :
        - utillisation d'un set afin d'éviter les doublons
        - on vérifie à part les cases disposées en forme de + (borne centre +)
        - puis autres cases
        - optimiste : si case en diagonale OK alors cases entre toutes OK aussi

        :param src: Pos(x,y) cellule source
        :returns: les cellules atteignables
        :rtype: set de tuples nommés (x,y)
        """

        # ensemble qui va contenir les coordonnées des cellules atteignables
        reachable_cells = set()

        # facilitateur de lecture
        Pos = namedtuple('Pos', 'x y')

        # on ne peut pas placer de borne sur un mur, ni sur le backbone
        if not self._map.cells[src.x][src.y].is_wall():

            # propagations linéaires dans les directions haut bas gauche droite
            # le premier mur arrête la propagation
            # les cases vides ne la stoppent pas mais ne sont pas gardées

            # haut
            top_extremity = self._map.limit_y(src.y - self._wifi_range)
            for y in range(top_extremity, src.y + 1):
                if self._map.cells[src.x][y].is_target():
                    reachable_cells.add(Pos(src.x, y))
                if self._map.cells[src.x][y].is_wall():
                    break
            # bas
            bottom_extremity = self._map.limit_y(src.y + self._wifi_range)
            for y in range(src.y, bottom_extremity + 1):
                if self._map.cells[src.x][y].is_target():
                    reachable_cells.add(Pos(src.x, y))
                if self._map.cells[src.x][y].is_wall():
                    break
            # gauche
            left_extremity = self._map.limit_x(src.x - self._wifi_range)
            for x in range(left_extremity, src.x + 1):
                if self._map.cells[x][src.y].is_target():
                    reachable_cells.add(Pos(x, src.y))
                if self._map.cells[x][src.y].is_wall():
                    break
            # droite
            right_extremity = self._map.limit_x(src.x + self._wifi_range)
            for x in range(src.x, right_extremity + 1):
                if self._map.cells[x][src.y].is_target():
                    reachable_cells.add(Pos(x, src.y))
                if self._map.cells[x][src.y].is_wall():
                    break

            # propagations en diagonale
            # on génère les coordonnées des cases englobées par le rectangle
            # de coins opposés routeur et extrémité de la portée wifi
            # pour chacun des angles HG, HD, BG, BD

            # haut gauche

            left_top = Pos(left_extremity, top_extremity)
            coos_lt = set(product([x for x in range(left_top.x, src.x + 1)],
                                  [y for y in range(left_top.y, src.y + 1)]))
            reachable_cells.add(self.keep_reachable_in_rectangle(coos_lt, src))

            # haut droite

            right_top = Pos(right_extremity, top_extremity)
            coos_rt = set(product([x for x in range(src.x, right_top.x + 1)],
                                  [y for y in range(right_top.y, src.y + 1)]))
            reachable_cells.add(self.keep_reachable_in_rectangle(coos_rt, src))

            # bas gauche

            left_bot = Pos(left_extremity, bottom_extremity)
            coos_lb = set(product([x for x in range(left_bot.x, src.x + 1)],
                                  [y for y in range(src.y, left_bot.y + 1)]))
            reachable_cells.add(self.keep_reachable_in_rectangle(coos_lb, src))

            # bas droite

            right_bot = Pos(right_extremity, bottom_extremity)
            coos_rb = set(product([x for x in range(src.x, right_bot.x + 1)],
                                  [y for y in range(src.y, right_bot.y + 1)]))
            reachable_cells.add(self.keep_reachable_in_rectangle(coos_rb, src))

        return reachable_cells

    def _evaluate_map(self):
        """
        Effectue la valuation de la carte selon la propagation des ondes wifi.
        1 point est octroyé par cellule ciblée atteignable.
        Retient dans un attribut les cases atteignables pour chaque case.
        """

        # facilitateur de lecture
        Pos = namedtuple('Pos', 'x y')

        # remplissage de la matrice contenant les listes de points atteignables
        # on en profite pour remplir la carte des scores de façon simultanée

        for x, col in enumerate(self._map):

            # colonnes intermédiaires de constuction des attributs de la classe
            reachable_col, scoring_col = [], []

            for y, cell in enumerate(col):

                # on conidère cette case comme routeur potentiel
                src = Pos(x, y)

                # on regarde les cases atteignables en wifi
                reachable_cells = self.reachable_cells(src)

                # on remplit les cartes de propagation et de valuation
                reachable_col.append(reachable_cells)
                scoring_col.append(len(reachable_cells))

            self._reachables_map.append(reachable_col)
            self.scoring_map.append(scoring_col)

    def re_evaluate_map(self, placed_router_pos):
        """
        Met à jour la carte valuée en fonction de la position du routeur placé.

        :param placed_router_pos: tuple(x,y) les coordonnées du routeur placé
        """

        # facilitateur d'accès
        Pos = namedtuple('Pos', 'x y')
        src = Pos(*placed_router_pos)

        # pour chaque case c couverte par ce nouveau routeur
        for c in self._reachables_map[src.x][src.y]:

            # pour chaque case v qui atteint cette case c
            # (les cases v atteignant c sont les cases que c peut atteindre)
            for v in self.reachable_cells(c):

                # diminuer de 1 le score procuré par v car case c déjà couverte
                if self.scoring_map[v.x][v.y] > 0:
                    self.scoring_map[v.x][v.y] -= 1
