# -*- coding: utf-8 -*-

from packages.structure.Cell import Cell


class Map:

    def __init__(self, cells, backbone_source_pos):
        """
        :param cells: [[Cell,Cell],[Cell,Cell] liste de listes de cellules
        :param backbone_source_pos: tuple(x,y) position du backbone
        """
        self.cells = cells
        self.backbone_source_pos = backbone_source_pos

    def __str__(self):
        map_repr = str(self.backbone_source_pos) + '\n'

        for line in self.cells:
            line_repr = ''
            for cell in line:
                line_repr += str(cell)
            map_repr += line_repr + '\n'

        return map_repr

    def limit_x(self, x):
        """
        Limite une coordonnée x par les dimensions mini et maxi de la carte.

        :param x: int une coordonnée x
        :return: int le x limité à la [0, largeur de la carte]
        """

        # le x limité de retour
        limited_x = x

        # largeur maximum
        max_x = len(self.cells)

        # si la coordonnée est correcte, il n'est pas nécessaire de la modifier
        if not 0 <= limited_x <= max_x:

            dist_to_0, dist_to_max_x = abs(0 - x), abs(max_x - x)
            # on se fixe sur la bordure la plus proche
            if dist_to_0 <= dist_to_max_x:
                limited_x = 0
            else:
                limited_x = max_x

        return limited_x

    def limit_y(self, y):
        """
        Limite une coordonnée y par les dimensions mini et maxi de la carte.

        :param y: int une coordonnée y
        :return: int le y limité à la [0, hauteur de la carte]
        """

        # le y limité de retour
        limited_y = y

        # largeur maximum
        max_y = len(self.cells)

        # si la coordonnée est correcte, il n'est pas nécessaire de la modifier
        if not 0 <= limited_y <= max_y:

            dist_to_0, dist_to_max_x = abs(0 - y), abs(max_y - y)
            # on se fixe sur la bordure la plus proche
            if dist_to_0 <= dist_to_max_x:
                limited_y = 0
            else:
                limited_y = max_y

        return limited_y




if __name__ == '__main__':

    lCell = list()
    for x in range(2):
        lCelly = list()
        for y in range(2):
            c = Cell(Map.WALL)
            lCelly.append(c)
        lCell.append(lCelly)
    map = Map(lCell, (0, 0))
    print(len(map.cells))
