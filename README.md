# CFD-HWZI_framework
The CFD-HWZI_framework is a Python-based code designed for high-wind zone identification (HWZI) using Computational Fluid Dynamics (CFD) simulation results. 
This framework operates with a single script, determineHWZI.py, which processes the input data and identifies potential high-wind zones for wind farm mapping in complex terrains.
The script requires five input files:
Four .csv files containing velocity field data from CFD simulations. These files represent wind speed distributions under different directional scenarios at various locations around the terrain.
One .stl file, which contains the topographic geometry data of Lemukutan Island. This file is crucial for modeling the terrain and understanding how the wind interacts with the island’s surface features.
he framework enables users to process the CFD simulation data and generate outputs relevant for high-wind zone identification, which can be used for further analysis in wind energy applications.
