# ProteinDB
Collection and analysis of protein coordinates and derived data.

# Requirements.

python3 
   
`Biopython` is Python Tools for Computational Molecular Biology.     
Install biopython.   
```bash
  pip install biopython
```
    
Library of `pandas` help us easy stored data into csv.   
Install pandas.     
```bash
  pip install pandas
```
Library of `matplotlib` is used for visualization.   
Install matplotlib.     
```bash
  pip install matplotlib
```

`wget` help us to download large databases.   
Install wget.     
```bash
  pip install wget
```
```
`Vmware` is used to download and install virtual ubuntu. 
should be downloaded from the official Vmware website.
```
`gcc` is necessary for running c++ program.   
Install gcc.     
```bash
  sudo apt update
  sudo apt install build-essential
```
Import the format_alignment package.   
```bash
  from Bio.pairwise2 import format_alignment 
```

`CD-hit` is used to perform clustering of sequences.   
Install CD-hit.     
```bash
  sudo apt install cd-hit
```

`Freesasa` is used to compute sasa of Biopython structures.     
Install freesasa.   
```bash
  pip install freesasa
```
Import the `pairwise2` package.   
```bash
  from Bio import pairwise2 
```

Import the `format_alignment` package.   
```bash
  from Bio.pairwise2 import format_alignment  
```

Use the `DSSP` program to calculate secondary structure and accessibility.   
Install the DSSP package(only install on an Ubuntu system).    
```bash
  conda install -c salilab dssp
```
Import the DSSP package.   
```bash
  from Bio.PDB.DSSP import DSSP   
```
The program installs itself as mkdssp, not dssp, and Biopython looks to execute dssp, so we need to symlink the name dssp to mkdssp.   
```bash
  dssp = DSSP(model, path, dssp='/home/ubuntu/anaconda3/bin/mkdssp')
```
    
`optparse` module makes easy to write command-line tools.    
python2 and python3 use `argparse`.  

# Contents
`DB.py`- Path of database and directories.  

`PDBStructure.py` - Used to parse detailed coordinate data from the PDB files (chains, surface etc.).

`PDBMeta.py` - Used to parse metadata associated with PDB file (resolution, deposition_date source etc.).

`PROTEINDBAPI.py` - This is a simple api for our database code to test metadata and structures
 
`cdhit-seq-analyse.py` - used to analyse the cluster files generated using cd-hit program

`PDBMetaExtractor.py` - extract all the metadata from the pdb code and store them in a dictionary
 
`sequence_utils.py` - modify and create new pdb file for the purpose of clustering
 
`extract_alphafold_ids.py` -   to append the alphafold db to pdb file for the purpose of clustering

`sequence.py` - generate pdb file for the purpose of cd-hit clustering and alignment of sequences 

`pdb_growth_data.py` - generate a graph about the growth of protein structure over the years

`SequenceHandler.py`  - extracting sequence information and storing them in dictionary

`PDBContactMap.py` - Used to calculate the maximum contact chain pair in structures.

`PDBFreesasa.py` - Used to calculate the solvent accessibility surface areas and buried surface areas of structures.

`PDBdssp.py` - Used to calculate the number of elements(loops, alpha-helix and beta-sheet) of the secondary structure of PDB structures .

`PDBGenerateDataset.py` - Generate the dataset that we used for analysis.

`xpdb.py` - Reading large PDB files with Biopython

