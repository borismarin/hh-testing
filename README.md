HH model with OSB model validation
==========================================

Sample [OpenSourceBrain](http://www.opensourcebrain.org/) project, containing [LEMS/NeuroML2](http://www.neuroml.org/lems/), [NEURON](http://www.neuron.yale.edu/neuron/) and [GENESIS](http://www.genesis-sim.org/) implementations of the [Hodgkin-Huxley model](http://en.wikipedia.org/wiki/Hodgkin–Huxley_model), tested and validated using the [OSB model validation framework](https://github.com/borismarin/osb-model-validation/). 

Each one of the simulators is downloaded and built in a travis worker, and tests specified via [omt](NEURON/hh.nrn.omt)/[mep](hh.mep) files are run.    


-------------------------------------------------------------------------------------------------------------------------------------
OSB Model Validation: [![Build Status](https://travis-ci.org/borismarin/hh-testing.svg)](https://travis-ci.org/borismarin/hh-testing)
