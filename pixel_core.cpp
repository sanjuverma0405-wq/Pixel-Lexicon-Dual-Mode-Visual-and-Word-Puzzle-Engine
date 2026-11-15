#include <stdio.h>
#include <stdint.h>
#include <stdbool.h>

typedef uint64_t u64;

// Pack 16 board tiles (0-15) into a 64-bit unsigned integer (4 bits per tile)
u64 c_pack_board(const int tiles[16]) {
    u64 board = 0;
    for (int i = 0; i < 16; i++) {
        board |= ((u64)(tiles[i] & 0xF)) << (4 * i);
    }
    return board;
}

// Extract a single tile from position 0-15
int c_get_tile(u64 board, int pos) {
    return (int)((board >> (4 * pos)) & 0xF);
}

// Slide a tile into the blank (0) slot
u64 c_slide_tile(u64 board, int blank_pos, int target_pos) {
    u64 tile = c_get_tile(board, target_pos);
    board &= ~(0xFULL << (4 * target_pos));  // Clear target position
    board |= (tile << (4 * blank_pos));       // Place tile into blank position
    return board;
}