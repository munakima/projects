# This is a simple api for our database code.
# System
import os
from os.path import join

# Our repo
from PDBMetaExtractor import MetaDataExtractor
from SequenceHandler import SequenceHandler
from sequence import align_sequences, generate_pdb_file
import PDBStructure as pdbStru
import PDBContactMap as pdbMap

# Locations
test_directory = join('data', 'testdata')
meta_directory = join('data', 'metadata')


##########
# METADATA#
##########

# retrieve metadata
# python ProteinDBAPI.py --metadata --pdb_code 1ahw 
def get_metadata(pdb_code):
    """
    #Data are IDCODE, HEADER, ACCESSION DATE, COMPOUND, SOURCE, AUTHOR LIST, RESOLUTION, EXPERIMENT TYPE (IF NOT X-RAY)
    #For 100d you should get
    #100D	DNA-RNA HYBRID	12/05/94	CRYSTAL STRUCTURE OF THE HIGHLY DISTORTED CHIMERIC DECAMER R(C)D(CGGCGCCG)R(G)-SPERMINE COMPLEX-SPERMINE BINDING TO PHOSPHATE ONLY AND MINOR GROOVE TERTIARY BASE-PAIRING		Ban, C., Ramakrishnan, B., Sundaralingam, M.	1.9	X-RAY DIFFRACTION
    #All neatly formatted in an array e.g. {'resolution':1.9,'date':12/05/94 ...}
    """

    extractor = MetaDataExtractor(pdb_code)
    metadata = extractor.get_metadata_dict()
    return metadata


# retrieve the sequence as in pdb_seqres
def get_fasta_sequence(pdb_code, chain):
    """
    it generates pdb name, molecule type, length of sequence, sequence name (chain) and the sequence
   
    """
    sequence_handler = SequenceHandler()
    sequences = sequence_handler.extract_sequences(join(meta_directory, "pdb_seqres.txt"))

    fasta_sequence = sequences.get(pdb_code + '_' + chain)
    return fasta_sequence


###########
# STRUCTURE#
###########

# Get chain ids for a given structure.
# The input needs to be a PDB structure in .pdb format
def get_chain_ids(pdb_structure):
    return pdbStru.getChainIds(pdb_structure)


# Get chain from a given pdb structure.
# The input needs to be a PDB structure in .pdb format.
def get_structure_sequence(pdb_structure, chain):
    return pdbStru.getStructureSequence(pdb_structure, chain)


# Get the pairwise atomic distances.
# The resulting file is a dictionary where each element corresponds to pairwise distance between closest heavy atoms
# (A_12,L_43) -> 17.1 means distance between residue 12 on chain H and residue 43 on chain L is 17.1
def get_pairwise_distances(pdb_structure, chain_1, chain_2):
    dic_dis_chain, res_dis_dic = pdbMap.contact_map(pdb_structure, chain_1, chain_2)
    return res_dis_dic


if __name__ == '__main__':
    from optparse import OptionParser

    parser = OptionParser()
    # Meta
    parser.add_option("--resolution", dest="resolution", action="store_true",
                      help="Indicate we wish to get resolution metadata", metavar="RESOLUTION")

    parser.add_option("--align", dest="align", action="store_true",
                      help="Indicate we wish to get align metadata", metavar="ALIGNED")

    parser.add_option("--organism", dest="organism", action="store_true",
                      help="Indicate we wish to get organism metadata", metavar="ORGANISM")

    parser.add_option("--metadata", dest="metadata", action="store_true",
                      help="Indicate we wish to get all metadata", metavar="METADATA")

    parser.add_option("--source", dest="source", action="store_true",
                      help="Indicate we wish to get all source", metavar="SOURCE")

    parser.add_option("--compound", dest="compound", action="store_true",
                      help="Indicate we wish to get all compound", metavar="COMPOUND")

    parser.add_option("--abstract", dest="abstract", action="store_true",
                      help="Indicate we wish to get the abstract", metavar="ABSTRACT")

    parser.add_option("--author", dest="author", action="store_true",
                      help="Indicate we wish to get the author", metavar="AUTHOR")

    parser.add_option("--method", dest="method", action="store_true",
                      help="Indicate we wish to get the abstract", metavar="METHOD")
    # structure
    parser.add_option("--chain_ids", dest="chain_ids", action="store_true",
                      help="Indicate we wish to retrieve chain ids from a structure", metavar="CHAIN IDS")
    parser.add_option("--fasta", dest="fasta", action="store_true",
                      help="Indicate we wish to retrieve fasta sequence of a given chain", metavar="CHAIN IDS")
    parser.add_option("--structure_sequence", dest="structure_sequence", action="store_true",
                      help="Indicate we are testing getting sequence from structure", metavar="STRUCTURESEQUENCE")
    parser.add_option("--pdb_code", dest="pdb_code",
                      help="Holds the pdb code", metavar="PDBCODE")
    parser.add_option("--pdb_structure", dest="pdb_structure",
                      help="Holds the full path of the pdb structure", metavar="PDBSTRUCTURE")
    parser.add_option("--distances", dest="pdb_structure",
                      help="Holds the full path of the pdb structure", metavar="PDBSTRUCTURE")
    (options, args) = parser.parse_args()

    # Simplified Tests.
    pdb_code = options.pdb_code
    # python ProteinDBAPI.py --metadata --pdb_code 1ahw
    metadata = get_metadata(pdb_code)

    # Test getting resolution
    if options.resolution:
        # python3 ProteinDBAPI.py --resolution --pdb_code 1ahw
        # test retrieval of resolution for 1ahw https://www.rcsb.org/structure/1AHW
        # pdb_code = '1ahw'
        resolution = metadata.get('resolution')
        print('Got resolution', resolution)
        if resolution != 3.00:
            print('Fail')

    # Test getting the organism  source information
    if options.source:
        # python3 ProteinDBAPI.py --source --pdb_code 1ahw
        source = metadata.get('source')
        print(source)
        if source != 'organism scientific':
            print('Fail')

    # Test getting the sequence alignment score
    if options.align:
        # python ProteinDBAPI.py --align --pdb_code 1ahw
        align_sequences(pdb_code)

    # Test getting the organism
    if options.organism:
        # python3 ProteinDBAPI.py --organism --pdb_code 1ahw
        organism = metadata.get('organism')
        print(organism)
        if organism.lower() != 'mus musculus':
            print('Fail')

    # Test getting the author
    if options.author:
        # python3 ProteinDBAPI.py --author --pdb_code 1ahw
        author = metadata.get('author')
        print(author.split(","))
        if author.lower() != 'huang, M':
            print('Fail')

    # Test getting the chain and compound information
    if options.compound:
        # python3 ProteinDBAPI.py --compound --pdb_code 1ahw
        compound = metadata.get('compound')
        print(compound)
        if compound != 'immunoglobulin':
            print('Fail')

    # Test getting the method
    if options.method:
        # python3 ProteinDBAPI.py --method --pdb_code 1ahw
        method = metadata.get('structure_method')
        print(method)
        assert method == 'X-RAY DIFFRACTION', "for pdb_code 1ahw, method must be equal to 'X-RAY DIFFRACTION'"

    # Test getting the abstract information
    # python ProteinDBAPI.py --abstract --pdb_code 1ahw
    if options.abstract:
        # pdb_code = '1ahw'
        metadata = metadata.get('abstract')
        assert metadata != None, "CANNOT FIND 'ABSTRACT'"
        print(metadata)

    ###########
    # SEQUENCES#
    ###########
    # Test getting metadata 
    # python ProteinDBAPI.py --metadata --pdb_code 1ahw
    if options.metadata:
        # pdb_code = '1ahw'
        metadata = get_metadata(pdb_code)
        print(metadata)

    # Test getting fasta sequence
    if options.fasta:
        # python3 ProteinDBAPI.py --fasta --pdb_code 1ahw
        # pdb_code = '1ahw'
        chain = 'A'
        sequence = get_fasta_sequence(pdb_code, chain)
        print(sequence)

    # Test getting sequence
    if options.structure_sequence:
        # python3 ProteinDBAPI.py --structure_sequence --pdb_code 1ahw
        pdb_file = join(test_directory, 'sample.pdb')
        pdb_chain = 'F'
        name, sequence = get_structure_sequence(pdb_file, pdb_chain)
        print('Sequence from structure', sequence)
        if sequence != 'TDSPVECMG':
            print('Fail')

        # Test getting distances
    if options.distances:
        # key of directory is dist['A_1,B_1'] -> value of directory 33.25 means distance
        # between residue 1 on chain A and residue 1 on chain B is 33.25
        # python3 ProteinDBAPI.py --distances 1ahw_A_1ahw_B
        pdb_code = join(test_directory, '1ahw.pdb')
        pdb_chain_1 = 'A'
        pdb_chain_2 = 'B'
        dist = get_pairwise_distances(pdb_code, pdb_chain_1, pdb_chain_2)
        # print ('distances among residues',dist)
        if dist['A_1,B_1'] != '33.25':
            print('Fail')
