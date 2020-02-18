# -*- coding: utf-8 -*-

from collections import namedtuple

from packages.structure.Cell import Cell
from packages.structure.Map import Map
from packages.structure.Problem import Problem
from packages.utils.log import log


class Parser:

    @staticmethod
    def load(source_file):
        """
        Parse un fichier-carte et en construit une représentation en mémoire.

        :param source_file: le chemin absolu de la carte à traiter en entrée
        :return: une représentation structurée du problème
        :rtype: Problem
        """

        with open(source_file) as f:

            # informations d'en-tête

            r, c, r_range = map(int, f.readline().split())
            bb_cost, r_cost, budget = map(int, f.readline().split())
            Pos = namedtuple('Pos', 'x y')
            bb_pos = Pos(*map(int, f.readline().split()))

            # tuiles
            cells = []
            for l in f:
                row = []
                for c in l:
                    to_append = ''
                    if c == Cell.HOW_VOID_IS_GIVEN:
                        to_append = Cell(Cell.VOID)
                    elif c == Cell.HOW_TARGET_IS_GIVEN:
                        to_append = Cell(Cell.TARGET)
                    elif c == Cell.HOW_WALL_IS_GIVEN:
                        to_append = Cell(Cell.WALL)
                    else:
                        to_append = Cell(-1)

                    row.append(to_append)
                cells.append(row)
            # création du problème
            the_map = Map(cells, bb_pos)
            the_map.cells[bb_pos.x][bb_pos.y].has_backbone = True
            problem = Problem(r_range, bb_cost, r_cost, budget, the_map)

        return problem
