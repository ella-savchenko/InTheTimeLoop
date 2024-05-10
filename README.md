# InTheTimeLoop
Framework for investigating data remanence in the main memory of virtual machines.

## Workflow
1. write specific patterns inside a virtual machine with writeDATA (InTheTimeLoop/writeDATA)
2. execute multiple experiments automatically with a shell script (InTheTimeLoop/experiments), powering on and off the virtual machine while executing writeDATA and logging the results of experiments (InTheTimeLoop/experiments/logs).
3. evaluate the results of experiments with searchDATA (InTheTimeLoop/searchDATA/evaluation) while searching for the pattern remanences.
4. visualize the evaluation´s results (InTheTimeLoop/searchDATA/visualization).
