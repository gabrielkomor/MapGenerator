#ifndef PLIK_H
#define PLIK_H

#ifdef __cplusplus
extern "C" {
#endif

#include <cstdint>

__declspec(dllexport) void fill_holes_and_spaces_in_obstacle(int8_t** game_map, int width, int height);
__declspec(dllexport) void fill_holes_in_obstacle(int8_t** game_map, int width, int height);
__declspec(dllexport) void fill_rectangles_two_by_three_in_obstacles(int8_t** game_map, int width, int height, bool rectangle, int number_of_neighbours);
__declspec(dllexport) void fill_rectangles_three_by_two_in_obstacles(int8_t** game_map, int width, int height, bool rectangle, int number_of_neighbours);
__declspec(dllexport) void fill_squares_two_by_two_in_obstacles(int8_t** game_map, int width, int height, bool square, int number_of_neighbours);
__declspec(dllexport) void fill_squares_three_by_three_in_obstacles(int8_t** game_map, int width, int height, bool square, int number_of_neighbours);

#ifdef __cplusplus
}
#endif

#endif // PLIK_H
