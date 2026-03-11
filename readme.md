<h1 align="center">
  <br>
  <a href="https://romanlytvynua.github.io/Post-Markem-demo/"><img width="200" height="300" src="https://github.com/user-attachments/assets/b0b4a0ac-b7d4-4262-8df2-a51031a6499c" alt="Post-Markem Logo"/></a>
  <br>
  Post-Markem
  <br>
</h1>

<p align="center">
  <a href="#description">Description</a> •
  <a href="#architecture--data-privacy">Architecture</a> •
  <a href="#features">Key Features</a> •
  <a href="#how-to-use">How To Use</a>
</p>

## Description
<b>Post-Markem</b> is the analytical engine that enables you to perform a "post-mortem" of competitive ballroom dance adjudication protocols. 

In dance sport, results are purely subjective. Adjudicators decide whether competitors get recalled or what place they take based entirely on personal impression. While this respects the artistic aspect of dancing, it makes it difficult to hold adjudicators accountable—bias can easily be justified as a "personal view."

However, provided enough statistical data, mathematical variance and bias can be isolated. Post-Markem mathematically models subjective judging data to assemble structured feedback on adjudicators, exposing panel alignment, standard deviations, and directional bias.

### Architecture & Data Privacy (Demo Repository)
This repository is the **Read-Only Public Interface** of the Post-Markem project featuring a demo db. 
The data featured in the demo.db was injested from real-world competitions. In order to preserve the privacy of the people involved all people names,
metadata, competition names, category names were masked. However, the actual marks and ratings are real. 

## Features

- [x] <b>Maverick Score</b> - A deviation metric that quantifies how frequently an adjudicator's marks contradict the final calculated panel result.
- [x] <b>Bias Detector</b> - A directional metric that identifies when an adjudicator consistently marks a specific competitor significantly higher or lower than the panel average.
- [x] <b>Trust Leaderboard</b> - A global ranking of adjudicators based on their cumulative impartiality.
- [x] <b>Coalition Scanner</b> – A correlation matrix that detects "Bloc Voting" by identifying pairs of adjudicators with statistically unlikely agreement rates.
- [ ] <b>Weighted Simulation</b> - A "What If" engine that recalculates the results by applying a reliability weight to each adjudicator's vote.

## How To Use

To run this demo locally on your machine:

```bash
# Clone this repository
$ git clone https://github.com/RomanLytvynUA/Post-Markem-demo.git

# Go into the repository
$ cd Post-Markem-demo

# Create and activate a Python virtual environment
$ python -m venv venv
$ source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install the dependencies
$ pip install -r requirements.txt

# Run the Flask application
$ python run.py