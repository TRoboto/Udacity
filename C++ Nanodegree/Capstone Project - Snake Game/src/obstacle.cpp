#include "obstacle.h"
#include "SDL.h"

void Obstacle::addObstacle(SDL_Point &obstacle)
{
    this->_obstacles.push_back(obstacle);
}

void Obstacle::clearObstacles()
{
    _obstacles.clear();
}