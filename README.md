# AA222-FinalProject

Files:

- NetworkSimulator.py: definition of the NetworkSimulator class, which is used to run simulations
- SimulationResult.py: just defines a little struct-like class that is helpful 
- policies.py: definition of a variety of different policies (functions) we use to decide what quality level to use. Each policy function
will take in the same inputs and same outputs so we can keep the simulation code the same, just requires changing the function name when we
want to test a different function.
    - random policy
    - Using cross entropy
    - and more that we tested out!!

- constants.py: definitions of constants that are used in a wide variety of files