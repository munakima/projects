import PDBStructure as pdbStru
import freesasa 
import DB
import pandas as pd
from os.path import join

def getGivenChainSasa(struc,targetChains):
	    allchains = pdbStru.PDBstructure(struc).allChains() # all chains of a clean structure
	    delChains = [c for c in allchains if c not in targetChains] # mark chains except targetChains
	    [struc[0].detach_child(c) for c in delChains] # delete chains except targetChains
	    freesasa.setVerbosity(1) # nowarnings FreeSASA: warning
	    structure = freesasa.structureFromBioPDB(struc[0])  # <- Faulty line
	    result = freesasa.calc(structure)
	    return '%0.2f' % result.totalArea()

def calContactSeperateBuriedArea(path, selChains):
	    structure = pdbStru.getOneStrucByPath(path)
	    struc = pdbStru.cleanStructure(structure)
	    sasa = {}
	    sasa['Structure_id'] = struc.id
	    targetChains = selChains.split('_') # ['A', 'B']
	    # a clean structure removed Unknown residues and atoms in order to avoid error when doing freesasa calculate
	    totalSasa = getGivenChainSasa(struc,targetChains)
	    chain_len=0
	    buried_sasa = float(totalSasa)
	    sasa['chain_pair'] = selChains
	    sasa['total_sasa'] = totalSasa
	    for chain in struc[0]:
	        if chain.id in targetChains:
	            for res in chain:
	                chain_len += 1
	    sasa['pair_length'] = chain_len
	    for chain in targetChains:
	        stru = pdbStru.getOneStrucByPath(path) # initialize structure
	        clean_struc = pdbStru.cleanStructure(stru)
	        chainSasa = getGivenChainSasa(clean_struc, chain) # get sasa of a single chain
	        buried_sasa -= float(chainSasa)
	    sasa['bsa'] = '% .2f' % -(buried_sasa/2)  # formula  buried area= -((totalSasa-chain1 sasa - chain2 sasa)/2)
	    return sasa
	
def calAsaBsaByChainpairs(mer=None):
    buried_list=[]
    csv_df = pd.read_csv(DB.ChainResPairs_csv)
    chain_pair_df=['structure_id','chain_pair']
    if(mer==None):
        for index, row in csv_df.iterrows():
            path=DB.pdb_db+'/pdb'+row['structure_id']+DB.ENT_FORMAT
            values=row['chain_pair']
            pair=calContactSeperateBuriedArea(path, values)
            df=pd.DataFrame([pair])
            pdbStru.saveCsv(DB.sasa_db,DB.ChainPair_sasa_bsa_csv,df)#DB.ChainPair_sasa_bsa_csv
            buried_list.append(pair)
    elif(mer=='dimer'):
        df=pd.read_csv(DB.dimer_csv)#dimer_csv
        li=list(df['structure_id'])
        for index, row in csv_df.iterrows():
            if(row['structure_id'] in li):
                path=DB.pdb_db+'/pdb'+row['structure_id']+DB.ENT_FORMAT
                values=row['chain_pair']
                pair=calContactSeperateBuriedArea(path, values)
                df=pd.DataFrame([pair])
                pdbStru.saveCsv(DB.sasa_db,DB.dimer_ChainPair_sasa_bsa_csv,df)#DB.ChainPair_sasa_bsa_csv
                buried_list.append(pair)
    return buried_list

def getResSasa(clean,k,v):
     struFree = freesasa.structureFromBioPDB(clean)
     result = freesasa.calc(struFree)
     dic = result.residueAreas()
     complex_res = dic[k][v]
     complex = '%.2f' % complex_res.total
     return complex

def remainTargetRes(struc, targetChain):
     model = struc
     allchains=[c.id for c in model]
     delChains = [c for c in allchains if c not in targetChain] # mark chains except targetChains
     [model.detach_child(c) for c in delChains] # delete chains except targetChains
     return struc

def getResAsaByChainResPairs(file_format):
	df=pd.read_csv(DB.ChainResPairs_csv)
	res_col=['structure_id','res_pair']
	res_list=df['res_pair'].tolist()
	res_str={}
	for index, row in df.iterrows():
		line=row['res_pair'].replace(" ", "").replace("'", "").strip("[").strip("]").split(',')
		print(row['structure_id'])
		lista=[]
		listb = []
		res_sasa_list = {} 
		stru_pair={}
		for j in line:
			A=j.split('~')[0]
			B=j.split('~')[1]
			lista.append(A.split('_')[0]+'_'+A.split('_')[2])
			listb.append(B.split('_')[0]+'_'+B.split('_')[2])
		chain_res=list(set(lista))+list(set(listb))

		pdb_path=DB.pdb_db+'/pdb'+row['structure_id']+file_format
		for c in chain_res:
			chain_arr = []
			structure=pdbStru.getOneStrucByPath(pdb_path)
			struc=pdbStru.cleanStructure(structure)
			sp=c.split('_')
			comb=getResSasa(struc[0], sp[0],sp[1])
			stru_s = remainTargetRes(struc[0], sp[0])
			single = getResSasa(struc[0], sp[0], sp[1])
			chain_arr.append(single)
			chain_arr.append(comb)
			res_sasa_list[c] = chain_arr
		stru_pair['structure_id']=row['structure_id']
		new_res={i:res_sasa_list[i] for i in sorted (res_sasa_list)}
		stru_pair['res_sasa']=new_res
		df=pd.DataFrame({'structure_id':[stru_pair['structure_id']],'res_sasa':[stru_pair['res_sasa']]},columns=['structure_id','res_sasa'])
		pdbStru.saveCsv(DB.sasa_db,DB.ResPairs_sasa_csv,df)

def mergin(file1,file2,mergin_file):
	csv1=pd.read_csv(file1)
	csv2=pd.read_csv(file2)
	df=pd.merge(csv1,csv2)
	df.to_csv(mergin_file,index=False, header=True)

def fullStrucASA(struc):
	freesasa_structure = freesasa.structureFromBioPDB(struc[0])  # <- Faulty line
	result = freesasa.calc(freesasa_structure)
	return '%0.2f' % result.totalArea()

def generateASABystructure(struc,dir_path,file):#alphaFoldHuman_sasa_csv
	sasa=fullStrucASA(struc)
	chains=pdbStru.PDBstructure(struc).chainLine()
	df=pd.DataFrame({'structure_id':[struc.id], 'chain_id':[chains],'sasa':[sasa]},columns=['structure_id', 'chain_id','sasa'])
	print(df)
	pdbStru.saveCsv(dir_path,file,df)

if __name__ == '__main__':
	test_directory = join('data','test_db')
	
	from optparse import OptionParser

	parser = OptionParser()

	parser.add_option("--sasa", dest="sasa", action="store_true",
		help="get sasa by chain list", metavar="Structure")
	parser.add_option("--totalsasa", dest="totalsasa", action="store_true",
		help="get dimer", metavar="Structure")
	parser.add_option("--bsa", dest="bsa", action="store_true",
		help="get dimer", metavar="Structure")
	parser.add_option("--keep_onechain_struc", dest="keep_onechain_struc", action="store_true",
		help="get dimer", metavar="Structure")
	parser.add_option("--pdb_code", dest="pdb_code",
		help="Holds the pdb code", metavar="PDBCODE")

	(options, args) = parser.parse_args()
	# test getGivenChainSasa
	if options.sasa == True:
		#python PDBFreesasa.py --sasa
		pdb_code = '1ahw'
		chains = ['A', 'B']
		path=test_directory+'/pdb'+pdb_code+DB.ENT_FORMAT
		structure=pdbStru.getOneStrucByPath(path)
		struc=pdbStru.cleanStructure(structure)
		sasa = getGivenChainSasa(struc,chains)
		if(sasa!='18773.39'):
			print('Fail')

	# test remainTargetRes
	if options.totalsasa == True:
		#python PDBFreesasa.py --totalsasa --pdb_code 1ahw
		pdb_code = '1ahw'
		path=test_directory+'/pdb'+pdb_code+DB.ENT_FORMAT
		structure=pdbStru.getOneStrucByPath(path)
		struc=pdbStru.cleanStructure(structure)
		sasa = remainTargetRes(struc)
		if(sasa!='54779.16'):
			print('Fail')

	# test remainTargetRes
	if options.keep_onechain_struc == True:
		#python PDBFreesasa.py --keep_onechain_struc --pdb_code 1ahw
		pdb_code = '1ahw'
		chain = 'A'
		path=test_directory+'/pdb'+pdb_code+DB.ENT_FORMAT
		structure=pdbStru.getOneStrucByPath(path)
		struc=pdbStru.cleanStructure(structure)
		new = remainTargetRes(struc[0],chain)
		chains=[c for c in new.get_chains()]
		if(len(chains)>1 or chains[0].id!=chain):
			print('Fail')

	# test calContactSeperateBuriedArea
	if options.bsa == True:
		#python PDBFreesasa.py --bsa --pdb_code 1ahw
		pdb_code = '1ahw'
		chains = 'A_B'
		path=test_directory+'/pdb'+pdb_code+DB.ENT_FORMAT
		structure=pdbStru.getOneStrucByPath(path)
		struc=pdbStru.cleanStructure(structure)
		sasa = calContactSeperateBuriedArea(path,chains)
		if(sasa['bsa'].strip()!='1815.48'):
			print('Fail')
