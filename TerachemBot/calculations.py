"""
Basic PyTC client example including authentication
"""

import numpy as np
import client
import math
from pubchem import Compound, get_cids, get_properties                                                                      


def get_capabilities():       # check user parameters request
    phases = {'gas': None,
         'water': 78.3553, 
         'acetonitrile': 35.688,
         'methanol': 32.613,
         'ethanol': 24.852,
         'isoquinoline': 11.00,
         'quinoline': 9.16,
         'chloroform': 4.7113,
         'diethylether': 4.2400,
         'dichloromethane': 8.93,
         'dichloroethane': 10.125,
         'carbontetrachloride': 2.2280,
         'benzene': 2.2706,
         'toluene': 2.3741,
         'chlorobenzene': 5.6968,
         'nitromethane': 36.562,
         'heptane': 1.9113,
         'cyclohexane': 2.0165,
         'aniline': 6.8882,
         'acetone': 20.493,
         'tetrahydrofuran': 7.4257,
         'dimethylsulfoxide': 46.826}

    properties = ['dipole', 'brightest','energy']

    return properties,phases

def get_parameters(cids):        # check molecule  
          
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


def launch_calculation(prop, name, phase,epsilon, atoms, geom, charge,output,functional):   # perform the calculation

    # TCC Authentication (contact us for valid key)
    URL_SERVER = # TO ADD 
    USER =       # TO ADD  
    API_KEY =    # TO ADD 


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
        'method':       functional,
        'basis':        '3-21g',
		'convthre': 3.0e-3,
		'precision':'single',
		'dftgrid': 0
    }
    
    if epsilon :
        tcc_options['pcm'] = 'cosmo'
        tcc_options['epsilon'] = epsilon

    if prop == 'brightest':
        tcc_options['cis'] = 'yes'
        tcc_options['cisnumstates'] = 2 
        tcc_options['cisconvtol'] = 1.0e-2
        
    
    result = TC.compute(geom, tcc_options)


    if prop == 'dipole':
        tc_out = result['dipole_moment']
        text = str('The dipole moment of {} is {:.2f} Debye'.format(name,round(tc_out,2))) 

    elif prop == 'energy':
        tc_out = result['energy']
        text = str('The SCF energy of {} is {:.6f} Hartree'.format(name,round(tc_out,2))) 


    elif prop == 'brightest':
        Tdip = [math.sqrt(result['cis_transition_dipoles'][i][0]**2+result['cis_transition_dipoles'][i][1]**2+result['cis_transition_dipoles'][i][2]**2) for i in range(2)]
        bright = Tdip.index(max(Tdip)) + 1 # convert to 1 indexed notation
        if bright == 1:
             bright_state = "first"
        elif bright == 2:
             bright_state = "second"

        final_number = (result['energy'][bright]-result['energy'][0])*27.2114
        tc_out = final_number

#    return tc_out 
    return text 



