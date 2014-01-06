Locaudio ![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/wallarelvo/locaudio/trend.png)
========
Sound source localization in reconfigurable wireless acoustic sensor networks

## Problem Specification
Imagine a wireless sensor network of microphones dispersed in an environment. Using this wireless acoustic sensor network (WASN), we would like to be able to determine the positions of input sounds within the environment. More specifically, if we gave an input sound to our system, it would gather auditory information from the environment using the WASN combined with the positions of the nodes within the WASN to determine an *x, y* position of the sound and a corresponding confidence metric.

## Getting Started
### To Install Dependencies
`make depend`

#### To Generate Documentation
`make documentation`

### To Start the Locaudio Server
**NOTE: All commands should be spawned from different terminal sessions**

1. Run RethinkDB
	- `rethinkdb`

1. Run the server
	-  `python run.py localhost 8000`

#### To Run Tests
**NOTE: All commands should be spawned from different terminal sessions**

1. Start the Locaudio server
	
1. `make run_tests`
