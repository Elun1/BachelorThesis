# BachelorThesis

Python scripts to run jobs from the SpecCPU2006 suite.

Caveats:

    *Running multiple instances of calculix and tonto from the same src dir doesn't work properly
  
    *Don't run more totaljobs than you have cpu cores
    
    *Start threads in a few functions are static, change to fit your system

Testing:

    *You need bash, /usr/bin/time and python3
  
    *Use the bash loops for testing (400.jobA.sh etc)
    
  
See documentation for function descriptions
