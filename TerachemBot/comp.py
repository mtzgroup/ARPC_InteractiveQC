# -*- coding: utf-8 -*-

from pubchem import Compound, get_cids, get_properties
from calculations import launch_calculation,get_capabilities,get_parameters


def compute(prop,name,phase,functional):  # check if the calculation can be performed  

   properties,phases = get_capabilities()

   if prop in properties and phase in phases:

      cids = get_cids(name, 'name')
      if not cids:
          raise ValueError("Sorry, I could not find {} on PubChem.".format(name))
      else:
          Natoms,atoms,geom,charge = get_parameters(cids)

          if geom is None:
             raise ValueError("Sorry, I could not find the coordinates of {} on PubChem.".format(name))

          else: 
             results = launch_calculation(prop, name, phase,phases[phase], atoms, geom, charge,True,functional)  # launch the calculation

   elif phase is None:
          raise ValueError("I need to know the phase.")
   elif prop in properties and not phase in phases:
          raise ValueError("I do not know that phase.")
   elif phase in phases and not prop in properties:
          raise ValueError("I do not know how to calculate that property.")

   return  results 

