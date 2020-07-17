# Learning Algorithm
The algorithm used to train the agent is the Deep Deterministic Policy Gradient algorithm. The algorithm works as follows:
* Define and initialize two networks, the Actor network that is used to approximate the policy and the critic network which estimate the value function.
* Initialize a replay memory to store agent's interactions with the environment.
* Start a loop through a given episodes followed by another loop of a given number of time-steps in each episode.
* The training loop consists mainly of two steps:
	1. __Acting__ where the agent chooses an action from the state using the Actor network.
	2. __Learning__ where the Actor network optimize its weights such that the estimated value of the input state is maximized. This is achieved by help of the Critic network which is used as a feedback.
* In each time-step, a soft update to the __target__ Actor and Critic weights happens where their weights are mixed with 0.01% of the __local__ networks weights.

# Actor Network Architecture 

* The architecture is shown below. 
* The input size is 33 and the output size is 4. 
* A batch normalization layer is applied to the first layer.
* First two layers are followed by relu activation function.
* Last layer is followed by tanh activation function.

```
Actor(
  (fc1): Linear(in_features=33, out_features=256, bias=True)
  (bnorm): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (fc2): Linear(in_features=256, out_features=128, bias=True)
  (fc3): Linear(in_features=128, out_features=4, bias=True)
)
```

# Critic Network Architecture 

* The architecture is shown below. 
* The input size is 33 and the output size is 1. 
* A batch normalization layer is applied to the first layer.
* First two layers are followed by relu activation function.
* Last layer is not followed by an activation function.

```
Critic(
  (fcs1): Linear(in_features=33, out_features=256, bias=True)
  (bnorm): BatchNorm1d(256, eps=1e-05, momentum=0.1, affine=True, track_running_stats=True)
  (fc2): Linear(in_features=260, out_features=128, bias=True)
  (fc3): Linear(in_features=128, out_features=1, bias=True)
)
```

# Hyperparameters used for training

```
BUFFER_SIZE = int(1e5)  # replay buffer size
BATCH_SIZE = 128        # minibatch size
GAMMA = 0.99            # discount factor
TAU = 1e-3              # for soft update of target parameters
LR_ACTOR = 3e-4         # learning rate of the actor 
LR_CRITIC = 3e-4        # learning rate of the critic
WEIGHT_DECAY = 0        # L2 weight decay
```

# Average rewards over 100 episodes

The average reward over 100 episodes is illustrated below. The environment has been solved in 174 episodes with an average score of 30.13. However, the agent is trained for 400 episodes, so that the agent has the ability to achieve a better score. As a result, the best average score is achieved in 342 episodes with a score of 35.54.

![reward](result.png)

# Future ideas

1. Use Asynchronous Actor Critic where multiple agents run independently in parallel and they optimize the network in an asynchronous manner.
2. Use Prioritized Experience Replay where important replays are prioritized over other replays.