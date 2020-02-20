# -*- coding: utf-8 -*-

"""

Point d'entrée du programme. Effectue les appels de plus haut niveau.
Est attendu en paramètre la liste des chemins vers les fichiers cartes.

"""

import sys
from os import listdir
from os.path import extsep, join, normpath, dirname

from packages.io.Parser import Parser
from packages.utils.log import log, log_task
from packages.utils.path import path_splitter

# emplacement des ressources accessibles au code
# la visibilité de python s'arrêtera au répertoire src
SRC_ROOT = normpath(join(dirname(__file__), '..'))
RES_DIR = join(SRC_ROOT, 'res')
IN_DIR = join(RES_DIR, 'in')
OUT_DIR = join(RES_DIR, 'out')

# si des fichiers sont fournis sur l'entrée standard, on les utilise
queue = sys.argv[1:]

# sinon on fournit les cartes par défaut
if len(queue) == 0:
    queue = [join(IN_DIR, file) for file in listdir(IN_DIR)]

log('{} file(s) to process in total'.format(len(queue)))

for filepath in queue:

    folder, name, ext = path_splitter(filepath)
    output_file = join(OUT_DIR, '{}{}{}'.format(name, extsep, 'out'))
    log_task('{} level solving'.format(name), 'begin')

    problem = Parser.load(filepath)
    
    solution = problem.solve()
    
    solution.write(output_file)

    log_task('{} level solving'.format(name), 'end')

log('finished')
