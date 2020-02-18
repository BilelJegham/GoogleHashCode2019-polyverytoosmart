# -*- coding: utf-8 -*-

class Cell:

    VOID = 0
    WALL = 1
    TARGET = 2
    HOW_VOID_IS_GIVEN = '-'
    HOW_TARGET_IS_GIVEN = '.'
    HOW_WALL_IS_GIVEN = '#'

    def __init__(self, nature, is_router=False, has_backbone=False):
        """
            :param nature: prix du routeur
            :param is_router: le budget maximale
            :param has_backbone: la carte à analyser et traiter
        """
        self.nature = nature
        self.router = is_router
        self.backbone = has_backbone

    def __str__(self):
        representation = ''

        if self.nature == Cell.VOID:
            representation = Cell.HOW_VOID_IS_GIVEN
        if self.nature == Cell.TARGET:
            representation = Cell.HOW_TARGET_IS_GIVEN
        if self.nature == Cell.WALL:
            representation = Cell.HOW_WALL_IS_GIVEN

        return representation

    def is_void(self):
        return self.nature == Cell.VOID

    def is_target(self):
        return self.nature == Cell.TARGET

    def is_wall(self):
        return self.nature == Cell.WALL
