#include <iostream>
#include <vector>
#include <string>
#include <sstream>
#include <algorithm>
#include <cstdint>
#include <unordered_set>
#include <cctype>

// ==========================================
// 1. 64-bit Bitmask Board Representation
// ==========================================
class BitmaskBoard15 {
public:
    uint64_t raw;

    BitmaskBoard15() : raw(0) {}
    explicit BitmaskBoard15(uint64_t val) : raw(val) {}

    static uint64_t pack(const std::vector<uint8_t>& tiles) {
        uint64_t board = 0;
        for (int i = 0; i < 16; ++i) {
            board |= ((uint64_t)(tiles[i] & 0x0F) << (i * 4));
        }
        return board;
    }

    static std::vector<uint8_t> unpack(uint64_t board) {
        std::vector<uint8_t> tiles(16);
        for (int i = 0; i < 16; ++i) {
            tiles[i] = (uint8_t)((board >> (i * 4)) & 0x0F);
        }
        return tiles;
    }

    static uint8_t getTile(uint64_t board, int index) {
        return (uint8_t)((board >> (index * 4)) & 0x0F);
    }

    static uint64_t setTile(uint64_t board, int index, uint8_t value) {
        uint64_t mask = (uint64_t)0x0F << (index * 4);
        board &= ~mask;
        board |= ((uint64_t)(value & 0x0F) << (index * 4));
        return board;
    }
};

// ==========================================
// 2. Merge Sort Solvability Checker (O(N log N))
// ==========================================
long long mergeAndCount(std::vector<int>& arr, int temp[], int left, int right) {
    int mid, i, j, k;
    long long inv_count = 0;
    if (right > left) {
        mid = (right + left) / 2;
        inv_count += mergeAndCount(arr, temp, left, mid);
        inv_count += mergeAndCount(arr, temp, mid + 1, right);

        i = left;
        j = mid + 1;
        k = left;
        while ((i <= mid) && (j <= right)) {
            if (arr[i] <= arr[j]) {
                temp[k++] = arr[i++];
            } else {
                temp[k++] = arr[j++];
                inv_count += (mid - i + 1);
            }
        }
        while (i <= mid) {
            temp[k++] = arr[i++];
        }
        while (j <= right) {
            temp[k++] = arr[j++];
        }
        for (i = left; i <= right; i++) {
            arr[i] = temp[i];
        }
    }
    return inv_count;
}

long long countInversions(std::vector<int>& arr) {
    std::vector<int> temp(arr.size());
    return mergeAndCount(arr, temp.data(), 0, arr.size() - 1);
}

bool isSolvable15(const std::vector<uint8_t>& tiles) {
    std::vector<int> flat;
    int blankRowFromBottom = 0;
    for (int i = 0; i < 16; ++i) {
        int val = tiles[i];
        if (val == 0) {
            int row = i / 4; 
            blankRowFromBottom = 4 - row; 
        } else {
            flat.push_back(val);
        }
    }
    long long inversions = countInversions(flat);
    if (blankRowFromBottom % 2 == 1) {
        return (inversions % 2 == 0);
    } else {
        return (inversions % 2 != 0);
    }
}

// ==========================================
// 3. Trie Data Structure & DFS Pruning Solver
// ==========================================
struct TrieNode {
    bool isEndOfWord;
    TrieNode* children[26];
    TrieNode() : isEndOfWord(false) {
        for (int i = 0; i < 26; ++i) children[i] = nullptr;
    }
    ~TrieNode() {
        for (int i = 0; i < 26; ++i) {
            if (children[i]) delete children[i];
        }
    }
};

class Trie {
public:
    TrieNode* root;
    Trie() { root = new TrieNode(); }
    ~Trie() { delete root; }

    void insert(const std::string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            char lowerC = std::tolower(c);
            if (lowerC < 'a' || lowerC > 'z') continue;
            int idx = lowerC - 'a';
            if (!curr->children[idx]) {
                curr->children[idx] = new TrieNode();
            }
            curr = curr->children[idx];
        }
        curr->isEndOfWord = true;
    }

    bool search(const std::string& word) {
        TrieNode* curr = root;
        for (char c : word) {
            char lowerC = std::tolower(c);
            if (lowerC < 'a' || lowerC > 'z') return false;
            int idx = lowerC - 'a';
            if (!curr->children[idx]) return false;
            curr = curr->children[idx];
        }
        return curr != nullptr && curr->isEndOfWord;
    }

    bool startsWith(const std::string& prefix) {
        TrieNode* curr = root;
        for (char c : prefix) {
            char lowerC = std::tolower(c);
            if (lowerC < 'a' || lowerC > 'z') return false;
            int idx = lowerC - 'a';
            if (!curr->children[idx]) return false;
            curr = curr->children[idx];
        }
        return curr != nullptr;
    }
};

void dfsWordSearch(int r, int c, const std::vector<std::string>& grid, std::vector<std::vector<bool>>& visited,
                   TrieNode* node, std::string currentWord, std::unordered_set<std::string>& foundWords) {
    char ch = grid[r][c];
    char lowerCh = std::tolower(ch);
    if (lowerCh < 'a' || lowerCh > 'z') return;
    int idx = lowerCh - 'a';
    
    // Aggressive Prefix Pruning: instantly terminate if prefix is absent in Trie
    if (!node->children[idx]) return; 

    node = node->children[idx];
    currentWord += lowerCh;

    if (node->isEndOfWord && currentWord.length() >= 3) {
        foundWords.insert(currentWord);
    }

    visited[r][c] = true;
    int dr[] = {-1, -1, -1, 0, 0, 1, 1, 1};
    int dc[] = {-1, 0, 1, -1, 1, -1, 0, 1};

    for (int i = 0; i < 8; ++i) {
        int nr = r + dr[i];
        int nc = c + dc[i];
        if (nr >= 0 && nr < 4 && nc >= 0 && nc < 4 && !visited[nr][nc]) {
            dfsWordSearch(nr, nc, grid, visited, node, currentWord, foundWords);
        }
    }
    visited[r][c] = false;
}

// ==========================================
// 4. CLI Command Routing
// ==========================================
int main(int argc, char* argv[]) {
    if (argc < 2) {
        std::cout << "ERROR: No command provided." << std::endl;
        return 1;
    }

    std::string mode = argv[1];

    Trie trie;
    std::vector<std::string> defaultVocabulary = {
        "cat", "dog", "pixel", "lexicon", "puzzle", "code", "engine", "python", "tkinter",
        "cplusplus", "game", "desktop", "interface", "aesthetic", "cozy", "pastel", "matcha",
        "lavender", "cocoa", "board", "tile", "slide", "word", "search", "trie", "merge",
        "sort", "inversion", "solvable", "matrix", "binary", "bitmask", "data", "structure",
        "function", "class", "object", "render", "canvas", "button", "frame", "window",
        "app", "craft", "whimsical", "magic", "sparkle", "star", "flower", "leaf", "tea",
        "cats", "dogs", "puzzles", "lexicons", "pixels", "engines", "codes", "games", "cards",
        "soft", "warm", "cream", "brown", "green", "purple", "pink", "sweet", "honey", "sugar",
        "mint", "biscuit", "cookie", "cherry", "peach", "plum", "berry", "fluff", "cloud"
    };
    for (const auto& w : defaultVocabulary) {
        trie.insert(w);
    }

    if (mode == "--verify-pixel" && argc >= 3) {
        std::string arg = argv[2];
        std::vector<uint8_t> tiles(16);
        std::stringstream ss(arg);
        std::string valStr;
        int idx = 0;
        while (std::getline(ss, valStr, ',') && idx < 16) {
            tiles[idx++] = (uint8_t)std::stoi(valStr);
        }
        if (idx == 16) {
            bool solvable = isSolvable15(tiles);
            if (solvable) {
                std::cout << "SOLVABLE" << std::endl;
            } else {
                std::cout << "UNSOLVABLE" << std::endl;
            }
        } else {
            std::cout << "ERROR: Invalid board format (expected 16 comma-separated values)." << std::endl;
        }
    } else if (mode == "--check-word" && argc >= 3) {
        std::string word = argv[2];
        if (trie.search(word)) {
            std::cout << "VALID" << std::endl;
        } else {
            std::cout << "INVALID" << std::endl;
        }
    } else if (mode == "--solve-lexicon" && argc >= 3) {
        std::string arg = argv[2];
        std::vector<std::string> grid(4, std::string(4, ' '));
        std::stringstream ss(arg);
        std::string valStr;
        int idx = 0;
        while (std::getline(ss, valStr, ',') && idx < 16) {
            int r = idx / 4;
            int c = idx % 4;
            grid[r][c] = valStr[0];
            idx++;
        }
        if (idx == 16) {
            std::unordered_set<std::string> foundWords;
            std::vector<std::vector<bool>> visited(4, std::vector<bool>(4, false));
            for (int r = 0; r < 4; ++r) {
                for (int c = 0; c < 4; ++c) {
                    dfsWordSearch(r, c, grid, visited, trie.root, "", foundWords);
                }
            }
            for (const auto& w : foundWords) {
                std::cout << w << " ";
            }
            std::cout << std::endl;
        } else {
            std::cout << "ERROR: Invalid grid format." << std::endl;
        }
    } else {
        std::cout << "ERROR: Unknown command or missing arguments." << std::endl;
    }

    return 0;
}
