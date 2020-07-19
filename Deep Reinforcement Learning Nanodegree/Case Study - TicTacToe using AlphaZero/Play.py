import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

import numpy as np
import time

from copy import copy

class Play:
    
    def __init__(self, game, player1=None, player2=None, name='game'):
        self.original_game=game
        self.game=copy(game)
        self.player1=player1
        self.player2=player2
        self.player=self.game.player
        self.end=False
        self.play()

    def reset(self):
        self.game=copy(self.original_game)
        self.click_cid=None
        self.end=False
        
    def play(self, name='Game'):
        
        self.reset()
        
        if self.game.w * self.game.h <25:
            figsize=(self.game.w/1.6, self.game.h/1.6)

        else:
            figsize=(self.game.w/2.1, self.game.h/2.1)

        
        self.fig=plt.figure(name, figsize=figsize)
        if self.game.w * self.game.h <25:
            self.fig.subplots_adjust(.2,.2,1,1)
        else:
            self.fig.subplots_adjust(.1,.1,1,1)
            
        self.fig.show()
        w,h=self.game.size
        self.ax=self.fig.gca()
        self.ax.grid()
        # remove hovering coordinate tooltips
        self.ax.format_coord = lambda x, y: ''
        self.ax.set_xlim([-.5,w-.5])
        self.ax.set_ylim([-.5,h-.5])
        self.ax.set_xticks(np.arange(0, w, 1))
        self.ax.set_yticks(np.arange(0, h, 1))
        self.ax.set_aspect('equal')
    
        for loc in ['top', 'right', 'bottom', 'left']:
            self.ax.spines[loc].set_visible(False)


        # fully AI game
        if self.player1 is not None and self.player2 is not None:
            self.anim = FuncAnimation(self.fig, self.draw_move, frames=self.move_generator, interval=500, repeat=False)
            return
        
        # at least one human
        if self.player1 is not None:
            # first move from AI first
            succeed = False
            while not succeed:
                loc = self.player1(self.game)
                succeed = self.game.move(loc)

            self.draw_move(loc)
            
        self.click_cid=self.fig.canvas.mpl_connect('button_press_event', self.click)

            
    def move_generator(self):
        score = None
        # game not concluded yet
        while score is None:
            self.player = self.game.player
            if self.game.player == 1:
                loc = self.player1(self.game)
            else:
                loc = self.player2(self.game)
                
            success = self.game.move(loc)

            # see if game is done
            if success:
                score=self.game.score
                yield loc
                
        
    def draw_move(self, move=None):
        if self.end:
            return
        
        i,j=self.game.last_move if move is None else move
        c='salmon' if self.player==1 else 'lightskyblue'
        self.ax.scatter(i,j,s=500,marker='o',zorder=3, c=c)
        score = self.game.score
        self.draw_winner(score)
        self.fig.canvas.draw()


    def draw_winner(self, score):
        if score is None:
            return
        
        if score == -1 or score == 1:
            locs = self.game.get_winning_loc()
            c='darkred' if score==1 else 'darkblue'
            self.ax.scatter(locs[:,0],locs[:,1], s=300, marker='*',c=c,zorder=4)

        # try to disconnect if game is over
        if hasattr(self, 'click_cid'):
            self.fig.canvas.mpl_disconnect(self.click_cid)

        self.end=True
        
    
    def click(self,event):
        
        loc=(int(round(event.xdata)), int(round(event.ydata)))
        self.player = self.game.player
        succeed=self.game.move(loc)

        if succeed:
            self.draw_move()

        else:
            return
        
        if self.player1 is not None or self.player2 is not None:

            succeed = False
            self.player = self.game.player
            while not succeed:
                if self.game.player == 1:
                    loc = self.player1(self.game)
                else:
                    loc = self.player2(self.game)
                succeed = self.game.move(loc)
               
            self.draw_move()
