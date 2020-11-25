#! /usr/bin/env python3
import argparse
from os import system

from spring_package.DBKit import createFile
from spring_package.Molecule import Molecule


def getId(line):
    line = line.strip()
    if len(line) != 6 or line[4:5] != "_":
        raise Exception("Invalid list entry (`PDB_CHAIN`): %s." % line)
    return line[:4].upper() + line[4:6]


def main(args):
    logFile = open(args.log, "w")
    system("mkdir -p %s" % args.temp)
    pdbCount = 0
    partnerList = set()
    entries = list()
    with open(args.list) as file:
        for line in file:
            entries.append(getId(line))
    logFile.write("Found %s template entries.\n" % len(entries))
    for entryId in entries:
        pdb = entryId[:4].lower()
        pdbChain = entryId[5:6]
        pdbFile = "%s/temp.pdb" % args.temp
        pdbDatabaseId = "%s.pdb" % pdb
        createFile(pdbDatabaseId, args.index, args.database, pdbFile)
        try:
            mol = Molecule(pdbFile)
        except Exception:
            logFile.write("Warning: File '%s' not found.\n" % pdbDatabaseId)
            continue
        pdbCount = pdbCount + 1
        logFile.write("Processing %s, chain %s.\n" % (pdb, pdbChain))
        logFile.write("Found %d biomolecule(s).\n" % len(mol.biomol.keys()))
        for biomolNumber in mol.biomol:
            if biomolNumber == 0:
                logFile.write("Processing biomolecule.\n")
                bioMolecule = mol
            else:
                logFile.write("Processing biomolecule %d.\n" % biomolNumber)
                bioMolecule = mol.createUnit(biomolNumber)
            nChains = len(bioMolecule.calpha.keys())
            print("Found %d chain(s)." % nChains)
            if nChains > 1 and pdbChain in bioMolecule.calpha:
                for bioChain in bioMolecule.calpha:
                    if bioChain == pdbChain:
                        continue
                    partnerPdbChain = "%s_%s" % (pdb.upper(), bioChain[:1])
                    partnerList.add("%s\t%s" % (entryId, partnerPdbChain))
            else:
                logFile.write("Skipping: Chain not found or single chain [%s].\n" % pdbChain)
        logFile.flush()
    with open(args.output, 'w') as output_file:
        for entry in sorted(partnerList):
            output_file.write("%s\n" % entry)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='List filtering.')
    parser.add_argument('-l', '--list', help='List of PDB chains [PDB_CHAIN]', required=True)
    parser.add_argument('-i', '--index', help='PDB Database Index file (ffindex)', required=True)
    parser.add_argument('-d', '--database', help='PDB Database files (ffdata)', required=True)
    parser.add_argument('-o', '--output', help='Output file', required=True)
    parser.add_argument('-t', '--temp', help='Temporary Directory', required=True)
    parser.add_argument('-g', '--log', help='Log File', required=True)
    args = parser.parse_args()
    main(args)