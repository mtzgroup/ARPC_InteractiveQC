from pubchempy import Compound, get_cids, get_properties
import json 
import requests
import numpy as np
from tcc import client 
from sys import argv

#########################################################################################################
#########################################################################################################
#                              Functions 
#########################################################################################################
#########################################################################################################

# Mathpix autentication 
MATHPIX_APP_ID =   # TO ADD
MATHPIX_APP_KEY =  # TO ADD 

# TCC autentication (contact us for valid key) 
URL_SERVER =       # TO ADD 
USER =             # TO ADD 
API_KEY =          # TO ADD 

def smiles_to_iupac(smiles):

#   Convert SMILES into IUPAC name using CACTUS database  

    CACTUS = "https://cactus.nci.nih.gov/chemical/structure/{0}/{1}"
    rep = "iupac_name"
    url = CACTUS.format(smiles, rep)
    response = requests.get(url)
    response.raise_for_status()
    return response.text

def image_to_smiles(filename):

#   Convert  image into SMILES   

    service = "https://api.mathpix.com/v3/text"
    response = requests.post(service, files={"file": open(filename,"rb")}, data={
              "options_json": json.dumps({
              "formats": ["text"],
              "include_smiles": True
           })
           }, headers={
               "app_id": MATHPIX_APP_ID,
               "app_key": MATHPIX_APP_KEY,
           })
    r = response.json()
    smiles = []

    if "text" in r:
       text = r["text"]
       i = text.find("<smiles>")
       if i != -1:
          j = text.find("</smiles>", i + 8)
          if j != -1:
             smiles = [text[i+8:j]]
             print('Recognized SMILES:', smiles[0])
             return (smiles[0])
       else:
          print ('Sorry, molecule not recognized')
          return (smiles)


def image_to_name(filename):

#   Convert  image into IUPAC name    

    smiles = image_to_smiles(filename) 
    if smiles:
       molecule_name = smiles_to_iupac(smiles)
    else:
       molecule_name = None 
    return molecule_name

def get_parameters(cids):        

#   Retrieve XYZ and molecular charge from PUBCHEM  

    cids = cids[0]
    try :
          c = Compound.from_cid(cids, record_type='3d')
          Natoms = len(c.to_dict(properties=['atoms'])['atoms'])
          charge = get_properties('charge',cids)[0]['Charge']
          coors = []
          atoms = []
          for i in range(Natoms):
              atoms.append(c.to_dict(properties=['atoms'])['atoms'][i]['element'])
              coors.append([c.to_dict(properties=['atoms'])['atoms'][i]['x'],c.to_dict(properties=['atoms'])['atoms'][i]['y'],c.to_dict(properties=['atoms'])['atoms'][i]['z']])
          geom = np.array(coors)
    except :
          Natoms = None
          atoms = None
          geom = None
          charge = None
     
    return Natoms,atoms,geom,charge

def launch_calculation(name, atoms, geom, charge):   

#   Perform the calculation

    ## Initialize client
    TC = client.Client(url=URL_SERVER, user=USER, api_key=API_KEY,  engine="terachem", verbose=False)

    ## Set the job specification
    tcc_options = {
        # TCC options
        'runtype':      'energy',
        'jobname':      'TerX calculation',
        'units':        'angstrom',
    # TeraChem engine options
        'atoms':        atoms,
        'charge':       charge,
        'spinmult':     1,
        'closed_shell': True,
        'restricted':   True,
        'method':       'pbe0',
        'basis':        '3-21g',
		'convthre': 3.0e-3,
		'precision':'single',
		'dftgrid': 0
    }
    
    result = TC.compute(geom, tcc_options)

    tc_out = result['dipole_moment']
    output = 'The dipole moment of {} in isolation is: '.format(name)
    output += '{:.1f} Debye. '.format(tc_out)

    return output 

def compute(name):  

#   Check if the coordinates are on PUBCHEM and launch the calculation 

    cids = get_cids(name, 'name')
    if not cids:
          raise ValueError("Sorry, I could not find {} on PubChem.".format(name))
    else:
          Natoms,atoms,geom,charge = get_parameters(cids)
          if geom is None:
             raise ValueError("Sorry, I could not find the coordinates of {} on PubChem.".format(name))
          else: 
             results = launch_calculation(name, atoms, geom, charge)
    return  results 

#########################################################################################################
#########################################################################################################
#                              MAIN 
#########################################################################################################
#########################################################################################################

if __name__ == "__main__":

#   Read input file 
    NARG = 1+1
    if (len(argv) != NARG):
      print (argv[0],'Error in argument number')
      print('USAGE:')
      print(argv[0],'image.jpg')
      exit(33)
   
    filename = argv[1]
   
#   Recognize molecule 

    print('WELCOME!')
    molecule = image_to_name(filename)

#   Launch calculation 

    if molecule:
       print('Molecule name:', molecule)
       output = compute(molecule)  
       print(output)
       print('Thank you for using TCC!')


