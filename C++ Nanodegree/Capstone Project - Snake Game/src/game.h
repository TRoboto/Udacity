#ifndef GAME_H
#define GAME_H

#include <random>
#include <SDL.h>
#include "controller.h"
#include "renderer.h"
#include "snake.h"
#include "obstacle.h"

class Game
{
public:
  Game(std::size_t grid_width, std::size_t grid_height, std::size_t obst_count);
  void Run(Controller const &controller, Renderer &renderer,
           std::size_t target_frame_duration);
  int GetScore() const;
  int GetSize() const;

private:
  Snake snake;
  Obstacle obstacle;
  SDL_Point food;

  std::random_device dev;
  std::mt19937 engine;
  std::uniform_int_distribution<int> random_w;
  std::uniform_int_distribution<int> random_h;

  int score{0};

  int obst_count;

  void PlaceFood();
  void PlaceObstacles();
  void Update();
};

#endif