Locaudio ![Bitdeli Badge](https://d2weczhvl823v0.cloudfront.net/wallarelvo/locaudio/trend.png)
========
Sound source localization in reconfigurable wireless acoustic sensor networks

## Problem Specification
Imagine a wireless sensor network of microphones dispersed in an environment. Using this wireless acoustic sensor network (WASN), we would like to be able to determine the positions of input sounds within the environment. More specifically, if we gave an input sound to our system, it would gather auditory information from the environment using the WASN combined with the positions of the nodes within the WASN to determine an *x, y* position of the sound and a corresponding confidence metric.

## Example Usages
- Tracking a bird in a jungle based on the bird's unique call
- Determining the position of an enemy tank using the unique sound made by the engine

## RESTful API 
To make use of this API, the Locaudio server and the RethinkDB database must be running.

### Notifying the server of a detection event
	
	POST /notify
	
#### Post form

	{
		x: <Float: X position>,
		y: <Float: Y position>,
		spl: <Float: Sound pressure level>,
		timestamp: <Float: Unix time in seconds>,
		fingerprint: [<Float>: Audio fingerprint]
	}

#### Return structure
	
	{
		error: <Integer: Error code>,
		message: <String: Error message>,
		name: <String: Sound name>
	}

### Getting positions of sounds

	GET /positions/:sound_name


#### Parameters
	
- `sound_name`: The name of the sounds

#### Return structure
##### If successful

	[
		{
			position: {
				x: <Float: X position of sound>,
				y: <Float: Y position of sound>
			},
			confidence: <Float (0 <= F <= 1)>
	]

##### If failure

	{
		error: <Integer: Error code>,
		message: <String: Error Message>
	}

### Get UI for sound position

	GET /viewer/:sound_name
	
#### Parameters
	
- `sound_name`: The name of the sound

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
