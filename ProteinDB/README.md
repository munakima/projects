# System for Repurposing and Analyzing Biomolecular Atomic Data   
The Protein Data Bank (PDB) is a repository of raw atomic coordinates of biomolecules. Any structural bioinformatics study requires post-processing of the raw data into derived information to be used in subsequent analysis. One of the most widely used derived pieces of information are non-covalent atomic contacts within and among biomolecules. Non-covalent atomic contacts define the structure and interactions of most biomolecules. Analysis of this information is crucial across many fields such as protein folding or protein-protein interaction prediction. Diverse structural bioinformatics studies tend to require similar collection and processing of intra- or inter-molecular atomic contacts from the raw structures in the PDB. In this project a system will be developed  that aims to provide information about contacts in a flexible and easy to use format.     
    
We have identified several stages common to bioinformatics studies based on atomic contacts. These steps are     
1) quality filtering of structures 
2)accessible surface and surface area change identification 
3)atomic contact identification 
4)contact visualization. 
Automated protocols will be created that collect contact data according to standardized and widely used metrics. The system will have a provision to be updated on a monthly basis and be accompanied by suitable web-based analytics tools to facilitate biomolecular atomic data repurposing.        
    
## The dataset   
Raw data from the Protein Data Bank(PDB: (http://www.rcsb.org/pdb/) ) which is a repository of experimentally determined three-dimensional structures of biological macromolecules (mostly proteins and nucleic acids) and associated small molecules (e.g., drugs, cofactors, inhibitors).The PDB archive is growing at a yearly rate of approximately 10%, and structural biologists are determining atomic level 3D structures for a growing number of ever larger and more complex molecular assemblies.    
    
## Atomic coordinate data    
Every PDB structure deposition includes the atomic coordinates defining the 3D structural model of the macromolecule. Atomic positions are specified as Cartesian coordinates (x, y, z) using Ångström units (i.e. 0.1 nm) and a right-handed coordinate system. Additional method-specific attributes are provided for individual atoms (e.g. B-factors or temperature-factors for MX structures)    
   
   
Accessible surface area According to the raw data, 

## Authors

- [@Qianhua Ma](https://github.com/munakima)


## Requirements

Note: There will not offer any dataset to download.


This code is designed to run Windows system. You would have to install tensorflow by yourself. Tensorflow you can install using pip.
```bash
  pip install tensorflow
```
**optparse** module makes easy to write command-line tools     
python2 and python3 use `argparse`   
