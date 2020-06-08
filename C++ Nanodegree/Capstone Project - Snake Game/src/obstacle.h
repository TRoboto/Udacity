#ifndef OBSTACLE_H
#define OBSTACLE_H

#include <random>
#include <SDL.h>
#include <vector>

class Obstacle
{
public:
    Obstacle(int width, int height) : grid_width(width), grid_height(height){};

    void addObstacle(SDL_Point &obstacle);
    std::vector<SDL_Point> getObstacles() const { return _obstacles; }

    void clearObstacles();

private:
    std::vector<SDL_Point> _obstacles;
    int grid_width;
    int grid_height;
};

#endif