import numpy as np
import matplotlib.pyplot as plt
import torch
import torch.nn as nn
import torch.nn.functional as F
import matplotlib.animation as animation
from copy import copy
from math import *
import random

c=1.0

# transformations
t0= lambda x: x
t1= lambda x: x[:,::-1].copy()
t2= lambda x: x[::-1,:].copy()
t3= lambda x: x[::-1,::-1].copy()
t4= lambda x: x.T
t5= lambda x: x[:,::-1].T.copy()
t6= lambda x: x[::-1,:].T.copy()
t7= lambda x: x[::-1,::-1].T.copy()

tlist=[t0, t1,t2,t3,t4,t5,t6,t7]
tlist_half=[t0,t1,t2,t3]

def flip(x, dim):
    indices = [slice(None)] * x.dim()
    indices[dim] = torch.arange(x.size(dim) - 1, -1, -1,
                                dtype=torch.long, device=x.device)
    return x[tuple(indices)]


t0inv= lambda x: x
t1inv= lambda x: flip(x,1)
t2inv= lambda x: flip(x,0)
t3inv= lambda x: flip(flip(x,0),1)
t4inv= lambda x: x.t()
t5inv= lambda x: flip(x,0).t()
t6inv= lambda x: flip(x,1).t()
t7inv= lambda x: flip(flip(x,0),1).t()

tinvlist = [t0inv, t1inv, t2inv, t3inv, t4inv, t5inv, t6inv, t7inv]
tinvlist_half=[t0inv, t1inv, t2inv, t3inv]

transformation_list = list(zip(tlist, tinvlist))
transformation_list_half = list(zip(tlist_half, tinvlist_half))

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu") 
device ='cpu'

def process_policy(policy, game):

    # for square board, add rotations as well
    if game.size[0]==game.size[1]:
        t, tinv = random.choice(transformation_list)

    # otherwise only add reflections
    else:
        t, tinv = random.choice(transformation_list_half)
     
    frame=torch.tensor(t(game.state*game.player), dtype=torch.float, device=device)
    input=frame.unsqueeze(0).unsqueeze(0)
    prob, v = policy(input)
    mask = torch.tensor(game.available_mask())
    
    # we add a negative sign because when deciding next move,
    # the current player is the previous player making the move
    return game.available_moves(), tinv(prob)[mask].view(-1), v.squeeze().squeeze()

class Node:
    def __init__(self, game, mother=None, prob=torch.tensor(0., dtype=torch.float)):
        self.game = game
          
        # child nodes
        self.child = {}
        # numbers for determining which actions to take next
        self.U = 0

        # V from neural net output
        # it's a torch.tensor object
        # has require_grad enabled
        self.prob = prob
        # the predicted expectation from neural net
        self.nn_v = torch.tensor(0., dtype=torch.float)
        
        # visit count
        self.N = 0

        # expected V from MCTS
        self.V = 0

        # keeps track of the guaranteed outcome
        # initialized to None
        # this is for speeding the tree-search up
        # but stopping exploration when the outcome is certain
        # and there is a known perfect play
        self.outcome = self.game.score


        # if game is won/loss/draw
        if self.game.score is not None:
            self.V = self.game.score*self.game.player
            self.U = 0 if self.game.score is 0 else self.V*float('inf')

        # link to previous node
        self.mother = mother

    def create_child(self, actions, probs):
        # create a dictionary of children
        games = [ copy(self.game) for a in actions ]

        for action, game in zip(actions, games):
            game.move(action)

        child = { tuple(a):Node(g, self, p) for a,g,p in zip(actions, games, probs) }
        self.child = child
        
    def explore(self, policy):

        if self.game.score is not None:
            raise ValueError("game has ended with score {0:d}".format(self.game.score))

        current = self

        
        # explore children of the node
        # to speed things up 
        while current.child and current.outcome is None:

            child = current.child
            max_U = max(c.U for c in child.values())
            #print("current max_U ", max_U) 
            actions = [ a for a,c in child.items() if c.U == max_U ]
            if len(actions) == 0:
                print("error zero length ", max_U)
                print(current.game.state)
                      
            action = random.choice(actions)            

            if max_U == -float("inf"):
                current.U = float("inf")
                current.V = 1.0
                break
            
            elif max_U == float("inf"):
                current.U = -float("inf")
                current.V = -1.0
                break
                
            current = child[action]
        
        # if node hasn't been expanded
        if not current.child and current.outcome is None:
            # policy outputs results from the perspective of the next player
            # thus extra - sign is needed
            next_actions, probs, v = process_policy(policy, current.game)
            current.nn_v = -v
            current.create_child(next_actions, probs)
            current.V = -float(v)

        
        current.N += 1

        # now update U and back-prop
        while current.mother:
            mother = current.mother
            mother.N += 1
            # beteen mother and child, the player is switched, extra - sign
            mother.V += (-current.V - mother.V)/mother.N

            #update U for all sibling nodes
            for sibling in mother.child.values():
                if sibling.U is not float("inf") and sibling.U is not -float("inf"):
                    sibling.U = sibling.V + c*float(sibling.prob)* sqrt(mother.N)/(1+sibling.N)

            current = current.mother


               
    def next(self, temperature=1.0):

        if self.game.score is not None:
            raise ValueError('game has ended with score {0:d}'.format(self.game.score))

        if not self.child:
            print(self.game.state)
            raise ValueError('no children found and game hasn\'t ended')
        
        child=self.child

        
        # if there are winning moves, just output those
        max_U = max(c.U for c in child.values())

        if max_U == float("inf"):
            prob = torch.tensor([ 1.0 if c.U == float("inf") else 0 for c in child.values()], device=device)
            
        else:
            # divide things by maxN for numerical stability
            maxN = max(node.N for node in child.values())+1
            prob = torch.tensor([ (node.N/maxN)**(1/temperature) for node in child.values() ], device=device)

        # normalize the probability
        if torch.sum(prob) > 0:
            prob /= torch.sum(prob)
            
        # if sum is zero, just make things random
        else:
            prob = torch.tensor(1.0/len(child), device=device).repeat(len(child))

        nn_prob = torch.stack([ node.prob for node in child.values() ]).to(device)

        nextstate = random.choices(list(child.values()), weights=prob)[0]
        
        # V was for the previous player making a move
        # to convert to the current player we add - sign
        return nextstate, (-self.V, -self.nn_v, prob, nn_prob)

    def detach_mother(self):
        del self.mother
        self.mother = None
