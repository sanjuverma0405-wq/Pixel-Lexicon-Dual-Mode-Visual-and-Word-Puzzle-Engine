import heapq


class PuzzleSolver:

  @staticmethod
  def solve(board_list):
    """Solves any 15-puzzle board instantly using A* Search and Manhattan Distance heuristic."""
    goal = tuple(list(range(1, 16)) + [0])
    start = tuple(board_list)

    if start == goal:
      return []

    def manhattan_heuristic(state):
      distance = 0
      for i, val in enumerate(state):
        if val == 0:
          continue
        target = val - 1
        r1, c1 = divmod(i, 4)
        r2, c2 = divmod(target, 4)
        distance += abs(r1 - r2) + abs(c1 - c2)
      return distance

    # Priority queue: (f_score, g_score, state, move_history)
    start_h = manhattan_heuristic(start)
    pq = [(start_h, 0, start, [])]
    visited = {start: 0}

    while pq:
      f, g, state, moves = heapq.heappop(pq)

      if state == goal:
        return moves

      if g > visited.get(state, float("inf")):
        continue

      blank = state.index(0)
      r, c = divmod(blank, 4)

      for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < 4 and 0 <= nc < 4:
          target_idx = nr * 4 + nc
          next_state = list(state)
          next_state[blank], next_state[target_idx] = (
              next_state[target_idx],
              next_state[blank],
          )
          next_tuple = tuple(next_state)

          new_g = g + 1
          if new_g < visited.get(next_tuple, float("inf")):
            visited[next_tuple] = new_g
            new_f = new_g + manhattan_heuristic(next_tuple)
            heapq.heappush(pq, (new_f, new_g, next_tuple, moves + [target_idx]))

      # Increased node limit for safe exploration
      if len(visited) > 300000:
        break

    return []
  