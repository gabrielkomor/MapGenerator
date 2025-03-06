#include "mapGeneratorCpp.h"
#include <cstdint>


 void fill_holes_and_spaces_in_obstacle(int8_t** game_map, int width, int height) 
    {
        for (int row = 1; row < height - 1; ++row) {
            for (int column = 1; column < width - 1; ++column) {
                // fill the empty spaces in the obstacles
                if (game_map[row][column] == 0) {
                    if (game_map[row - 1][column] != 0 && game_map[row + 1][column] != 0) {
                        game_map[row][column] = 1;
                    }
                    if (game_map[row][column - 1] != 0 && game_map[row][column + 1] != 0) {
                        game_map[row][column] = 1;
                    }
                }

                // fill the gaps between two obstacles
                if (game_map[row][column] == 0) {
                    if (game_map[row - 1][column] == 1 && game_map[row + 1][column] == 1) {
                        game_map[row][column] = 1;
                    }
                    if (game_map[row][column - 1] != 0 && game_map[row][column + 1] != 0) {
                        game_map[row][column] = 0;
                    }
                }
            }
        }
    }


void fill_holes_in_obstacle(int8_t** game_map, int width, int height)
{
    // fill holes in obstacles
    for (int row = 1; row < height - 2; ++row){
        for (int column = 1; column < width - 2; ++column){
            if (game_map[row][column] == 0){
                if (game_map[row][column - 1] == 1 && game_map[row][column + 1] == 1){
                    if (game_map[row - 1][column] == 1){
                        game_map[row][column] = 1;
                    }
                }
            }
        }
    }
}


void fill_rectangles_two_by_three_in_obstacles(int8_t** game_map, int width, int height, bool rectangle, int number_of_neighbours)
{
    // find rectangles 2 by 3
    for (int row = 1; row < height - 3; ++row){
        for (int column = 1; column < width - 2; ++column){
            // find rectangle
            if (game_map[row][column] == 0 && game_map[row][column + 1] == 0){
                if (game_map[row + 1][column] == 0 && game_map[row + 1][column + 1] == 0){
                    if (game_map[row + 2][column] == 0 && game_map[row + 2][column + 1] == 0){
                        rectangle = true;
                    }
                }
            } 

            if (rectangle){
                // left edge of rectangle
                if (game_map[row][column - 1] == 1 && game_map[row + 1][column - 1] == 1 && game_map[row + 2][column - 1] == 1){
                    number_of_neighbours += 1;
                }
                
                // top edge of rectangle
                if (game_map[row - 1][column] == 1 && game_map[row - 1][column + 1] == 1){
                    number_of_neighbours += 1;
                }

                // right edge of rectangle
                if (game_map[row][column + 2] == 1 && game_map[row + 1][column + 2] == 1 && game_map[row + 2][column + 2] == 1){
                    number_of_neighbours += 1;
                }

                // bottom edge of rectangle
                if (game_map[row + 3][column] == 1 && game_map[row + 3][column + 1] == 1){
                    number_of_neighbours += 1;
                }

                if (number_of_neighbours >= 3){
                    game_map[row][column] = 0;
                    game_map[row][column + 1] = 0;
                    game_map[row + 1][column] = 0;
                    game_map[row + 1][column + 1] = 0;
                    game_map[row + 2][column] = 0;
                    game_map[row + 2][column + 1] = 0;
                }

                number_of_neighbours = 0;
                rectangle = false;
            }
        }
    }
}


void fill_rectangles_three_by_two_in_obstacles(int8_t** game_map, int width, int height, bool rectangle, int number_of_neighbours)
{
    // find rectangle 3 by 2
    for (int row = 1; row < height - 2; ++row){
        for (int column = 1; column < width - 3; ++column){
            if (game_map[row][column] == 0 && game_map[row][column + 1] == 0 && game_map[row][column + 2] == 0){
                if (game_map[row + 1][column] == 0 && game_map[row + 1][column + 1] == 0 && game_map[row + 1][column + 2] == 0){
                    rectangle = true;
                }
            }

            if (rectangle){
                // left edge of rectangle
                if (game_map[row][column - 1] == 1 && game_map[row + 1][column - 1] == 1){
                    number_of_neighbours += 1;
                }

                // top edge of rectangle
                if (game_map[row - 1][column] == 1 && game_map[row - 1][column + 1] == 1 && game_map[row - 1][column + 2] == 1){
                    number_of_neighbours += 1;
                }

                // right edge of rectangle
                if (game_map[row][column + 3] == 1 && game_map[row + 1][column + 3] == 1){
                    number_of_neighbours += 1;
                }

                // bottom edge of rectangle
                if (game_map[row + 2][column] == 1 && game_map[row + 2][column + 1] == 1 && game_map[row + 2][column + 2] == 1){
                    number_of_neighbours += 1;
                }

                if (number_of_neighbours >= 3){
                    game_map[row][column] = 1;
                    game_map[row][column + 1] = 1;
                    game_map[row][column + 2] = 1;
                    game_map[row + 1][column] = 1;
                    game_map[row + 1][column + 1] = 1;
                    game_map[row + 1][column + 2] = 1;
                }

                number_of_neighbours = 0;
                rectangle = false;
            }
        }
    }
}


void fill_squares_three_by_three_in_obstacles(int8_t** game_map, int width, int height, bool square, int number_of_neighbours)
{
    // find squares 3 by 3
    for (int row = 1; row < height - 3; ++row){
        for (int column = 1; column < width - 3; ++column){
            // find square
            if (game_map[row][column] == 0 && game_map[row][column + 1] == 0 && game_map[row][column + 2] == 0){
                if (game_map[row + 1][column] == 0 && game_map[row + 1][column + 1] == 0 && game_map[row + 1][column + 2] == 0){
                    if (game_map[row + 2][column] == 0 && game_map[row + 2][column + 1] == 0 && game_map[row + 2][column + 2] == 0){
                        square = true;
                    }
                }
            }

            if (square){
                // left edge of square
                if (game_map[row][column - 1] == 1 && game_map[row + 1][column - 1] == 1 && game_map[row + 2][column - 1] == 1){
                    number_of_neighbours += 1;
                }

                // top edge of square
                if (game_map[row - 1][column] == 1 && game_map[row - 1][column + 1] == 1 && game_map[row - 1][column + 2] == 1){
                    number_of_neighbours += 1;
                }

                // right edge of square
                if (game_map[row][column + 1] == 1 && game_map[row + 1][column + 1] == 1 && game_map[row + 2][column + 1] == 1){
                    number_of_neighbours += 1;
                }

                // bottom edge of square
                if (game_map[row + 3][column] == 1 && game_map[row + 3][column + 1] == 1 && game_map[row + 3][column + 2] == 1){
                    number_of_neighbours += 1;
                }

                if (number_of_neighbours >= 2){
                    game_map[row][column] = 1;
                    game_map[row][column + 1] = 1;
                    game_map[row][column + 2] = 1;
                    game_map[row + 1][column] = 1;
                    game_map[row + 1][column + 1] = 1;
                    game_map[row + 1][column + 2] = 1;
                    game_map[row + 2][column] = 1;
                    game_map[row + 2][column + 1] = 1;
                    game_map[row + 2][column + 2] = 1;
                }

                number_of_neighbours = 0;
                square = false;
            }
        }
    }
}


void fill_squares_two_by_two_in_obstacles(int8_t** game_map, int width, int height, bool square, int number_of_neighbours)
{
    // find squares 2 by 2
    for (int row = 1; row < height - 2; ++row){
        for (int column = 1; column < width - 2; ++column){
            // find square
            if (game_map[row][column] == 0 && game_map[row][column + 1] == 0){
                if (game_map[row + 1][column] == 0 && game_map[row + 1][column + 1] == 0){
                    square = true;
                }
            }

            if (square){
                // left edge of square
                if (game_map[row][column - 1] == 1 && game_map[row + 1][column - 1] == 1){
                    number_of_neighbours += 1;
                }

                // top edge of square
                if (game_map[row - 1][column] == 1 && game_map[row - 1][column + 1] == 1){
                    number_of_neighbours += 1;
                }

                // right edge of square
                if (game_map[row][column + 2] == 1 && game_map[row + 1][column + 2] == 1){
                    number_of_neighbours += 1;
                }

                // bottom edge of square
                if (game_map[row + 2][column] == 1 && game_map[row + 2][column + 1] == 1){
                    number_of_neighbours += 1;
                }

                if (number_of_neighbours >= 3){
                    game_map[row][column] = 1;
                    game_map[row][column + 1] = 1;
                    game_map[row + 1][column] = 1;
                    game_map[row + 1][column + 1] = 1;
                }

                number_of_neighbours = 0;
                square = false;
            }
        }
    }
}
