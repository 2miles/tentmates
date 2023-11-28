# Heart Anomalies

### Miles Whitaker

Homework 3: Machine Learning Question 2.
CS-441 AI, Nov 2023, Bart Massey

The background for this problem is explained [here](https://drdobbs.com/mates/184410645). It was given by Dennis Sasha in the August 1998 Dr. Dobb's Journal. Given a bunch of campers that need to be packed into tents, and preferences of these campers for tent-mates, find an optimally-happy packing

### What I did

- My algorithm randomly assigns people to tents. Then makes individual swaps until its in a better state. It will swap to a better state up to 2 times in a row by default. Then randomly assign people and do it again.

### What is still to be done

- I would like to get my time down to a few seconds.

## Running

To run the program with a default goal score of 175 run the program with no arguments

```
python3 tentmates.py
```

### Arguments:

#### `--verbose`

Show the number of restarts that happened.

If in test mode show the timings of easch run as they complete.

#### `--goal GOAL`

The minimum accepted total preference score. Between 0 and 175. The default is 175.

#### `--test TEST`

Run in timing mode. The number of timing tests to run.

When this option is given the program will not output a tent assignment instead it will output the average timing for TEST number of timing tests.

#### `--swaps SWAPS`

Number of consecutive swaps to a better state allowed before restart. Default is 2.

## Examples:
