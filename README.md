# Deep Learning Playfair Ciphers
**Authors:** Connor Onweller and Christopher Outhwaite

Deep learning approach to generating keys for Playfair Ciphers given plain text
and cipher text.

## Requirements:
* `python3`
* `tensorflow`
* `keras`
* `numpy`

## How to use
Run with the command:
```
python3 main.py
```

## Project Structure:
Training data is stored as a text file called `melville-moby_dick.txt` in the
`data` directory. The source code for this projects is stored in the directory
`src`.

## Our Model
We used a deep q learning based approach. We built a neural network with a ReLU
densely connected input layer, 7 densely connected ReLU hidden layers, and a
densely connected output layer with a linear activation function. We used an
epsilon greedy method to ensure that our model continued to explore as it
learned. We decided to use a positive living reward for our model, because the
goal of our model was to keep our agent in a living state for as long as
possible (a positive terminal state would only occur if our agent when through
the entirety of its plain and cipher text without making any mistakes in the
key it generated).

## File Breakdown
### main.py
Reads in the training data, and then builds/runs the neural network
off of that data.

### cipher.py
Contains methods to generate a cipher key, encipher text given a key, decipher
text given a key, and display a cipher key as a 5 x 5 matrix.

### training_data.py
Houses a method to generate usable training data from an arbitrary text file.
It reads in the file, removes unwanted characters, and then splits the text
into equally sized subsections and generates a key and a cipher text for each
subsection of plan text.

### keyenv.py
Contains the `KeyState` class. Contains information about the key the agent is
currently building, as well as the methods for the actions an agent can take to
continue building a key.

### model.py
Houses our `NNet` class, which contains the structure for our neural network. See model description for more info about how it works.

### agent.py
Contains our agent class. Contains various constant for our neural network,
such as the number of hidden layers, the discount rate, the learning rate, and
the epsilon values. Contains methods for the agent to store reward values from
each action for a given state, and contained methods for the agent to act as
well as update the neural network.


## Conclusions
The results of this project has shown us that deep learning might not be the
best approach to solve this problem. In order to represent the possible actions
an agent could take to create a cipher key in a reasonable amount of space, we
had to simplify the way the key was built. Even this simplified version of the
actions required over a thousand lines of code. After testing our code, we
concluded that our neural network preforms slightly better than an agent
choosing random actions. When our agent chose actions according to our neural
network it was able to successfully place 8.062 characters in each key it
attempted to generate. When it chose actions randomly, it was only able to
place about 7.383 characters per key.

One possible issue may just be that the computers we were running our program
on just weren't powerful enough. We were only able to get through about 9000
episodes of training, and even that took us about an hour to run. It could be
that if we were able to give our agent more training data, its performance
would improve.


## Resources Used
#### Deep Q-Learning with Keras and Gym by Keon Kim
[Article](https://keon.io/deep-q-learning)

[GitHub Repo](https://github.com/keon/deep-q-learning)

#### Deep Reinforcement Learning by Thomas Simonini
[Course Webpage](https://simoninithomas.github.io/Deep_reinforcement_learning_Course/)

[GitHub Repo](https://github.com/simoninithomas/Deep_reinforcement_learning_Course)

#### Get Started with TensorFlow
[Tutorials/Examples](https://www.tensorflow.org/tutorials/)

#### How to build your own AlphaZero AI using Python and Keras by David Foster
[Article](https://medium.com/applied-data-science/how-to-build-your-own-alphazero-ai-using-python-and-keras-7f664945c188)

[GitHub Repo](https://github.com/AppliedDataSciencePartners/DeepReinforcementLearning)
