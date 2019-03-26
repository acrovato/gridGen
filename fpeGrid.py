#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
## @package FPE grid creator
#
# Create a rectangular unstructured tetrahedral grid around a wing
# to be meshed with gmsh for Flow Full Potential solver
# Adrien Crovato

import wing as w
import tip as t
import box as b
import wake as wk

def main(_module, _output):
    # Get config
    p = getConfig(_module)

    # Create wing, wingtip, wake and bounding box
    wing = w.Wing(p['airfName'], p['span'], p['taper'], p['sweep'], p['dihedral'], p['twist'], p['rootChord'])
    if p['coWingtip']:
        tip = t.CTip(wing)
    else:
        tip = t.RTip(wing)
    box = b.Box(p['xoBox'], p['xfBox'], p['yfBox'], p['zoBox'], p['zfBox'])
    wake = wk.Wake(p['xoBox'], p['xfBox'], p['yfBox'], p['nSlope'], wing.spanPos)
    # Create interfaces

    # Write
    createWdir()
    outFile = _output + '.geo'
    # misc
    writeHeader(outFile, _module)
    wing.writeInfo(outFile)
    wing.writeOpts(outFile)
    # points
    wing.writePoints(outFile)
    tip.writePoints(outFile)
    box.writePoints(outFile)
    wake.writePoints(outFile)
    # lines
    wing.writeLines(outFile)
    tip.writeLines(outFile)
    # surfaces
    wing.writeSurfaces(outFile)
    tip.writeSurfaces(outFile)

    # Output
    print outFile, 'successfully created!'

    # eof
    print ''

def getConfig(_module):
    # Get prarmeters from config file
    import os, sys, ntpath
    sys.path.append(os.path.abspath(os.path.dirname(_module))) # tmp append module directory to pythonpath
    module = __import__(ntpath.basename(_module)) # import config as module
    p = module.getParams()
    # Fix path
    for i in range(0, len(p['airfName'])):
        p['airfName'][i] = os.path.join(os.path.abspath(os.path.dirname(_module)), p['airfPath'],p['airfName'][i])
    return p

def createWdir():
    import os
    wdir = os.path.join(os.getcwd(), 'workspace')
    print wdir
    if not os.path.isdir(wdir):
        print "creating", wdir
        os.makedirs(wdir)
    os.chdir(wdir)

def writeHeader(fname, _module):
    import ntpath
    file = open(fname, 'w')
    file.write('/******************************************/\n')
    file.write('/* Gmsh geometry for {0:>20s} */\n'.format(ntpath.basename(_module)))
    file.write('/* Generated by      {0:>20s} */\n'.format(ntpath.basename(__file__)))
    file.write('/* Adrien Crovato                         */\n')
    file.write('/* ULiege, 2018-2019                      */\n')
    file.write('/******************************************/\n\n')
    file.close()

if __name__ == "__main__":
    # Arguments parser
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', dest='mod', help='input config module (w/o .py)')
    parser.add_argument('-o', dest='out', help='output geo file (w/o .geo)', default='grid')
    args = parser.parse_args()

    main(args.mod, args.out)
