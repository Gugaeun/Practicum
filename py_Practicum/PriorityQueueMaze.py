# 우선순위 큐 기반 미로탐색
import math

def is_full_check(data, max_size):
    if max_size is None:
        return False
    return len(data) >= max_size

def is_empty_check(data):
    return len(data) == 0

def find_highest_priority(data):
    if not data:
        return -1
    best = 0
    for i in range(1, len(data)):
        if data[i][0] < data[best][0]:   # (distance, (r, c)) 형태
            best = i
    return best

def heuristic(r, c, goal_r, goal_c):
    return math.sqrt((goal_r - r) ** 2 + (goal_c - c) ** 2)

def get_neighbors(r, c, maze_size):
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]
    return [(r + dr, c + dc) for dr, dc in directions
            if 0 <= r + dr < maze_size and 0 <= c + dc < maze_size]

def is_passable(maze, r, c):
    return maze[r][c] == 0

def print_maze(maze, current=None, visited=None, path=None):
    MAZE_SIZE = len(maze)
    print("    ", end="")
    for c in range(MAZE_SIZE):
        print(f" {c} ", end="")
    print()

    for r in range(MAZE_SIZE):
        print(f"  {r} ", end="")
        for c in range(MAZE_SIZE):
            if path and (r, c) in path and (r, c) != (0, 0):
                print(" ✅ ", end="")
            elif current == (r, c):
                print(" 🐭 ", end="")
            elif visited and (r, c) in visited:
                print(" · ", end="")
            elif maze[r][c] == 1:
                print(" ■ ", end="")
            elif (r, c) == (0, 0):
                print(" S ", end="")
            elif (r, c) == (MAZE_SIZE - 1, MAZE_SIZE - 1):
                print(" E ", end="")
            else:
                print("   ", end="")
        print()

def print_step(step, current, dist, queue_list, maze, visited):
    print(f"\n  ── 단계 {step} ──────────────────────────────")
    print(f"  현재 위치     : {current}")
    print(f"  출구까지 거리 : {dist:.3f}")
    # 큐 상태: 거리 순으로 정렬해서 보여줌
    sorted_q = sorted(queue_list, key=lambda x: x[0])
    print(f"  큐 상태 (거리, 위치) : {[(round(d,2), pos) for d, pos in sorted_q]}")
    print_maze(maze, current=current, visited=visited)


# PriorityQueue 클래스
class PriorityQueue:
    def __init__(self, max_size=None):
        self.__data = []
        self.__max_size = max_size

    def enqueue(self, e):
        if self.is_full():
            raise OverflowError("우선순위 큐가 가득 찼습니다")
        self.__data.append(e)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("우선순위 큐가 비어 있습니다")
        idx = find_highest_priority(self.__data)   # 외부 함수 활용
        return self.__data.pop(idx)

    def peek(self):
        """가장 우선순위 높은 요소 확인 (삭제 X)"""
        if self.is_empty():
            raise IndexError("우선순위 큐가 비어 있습니다")
        idx = find_highest_priority(self.__data)
        return self.__data[idx]

    def is_full(self):
        return is_full_check(self.__data, self.__max_size)

    def is_empty(self):
        return is_empty_check(self.__data)

    def size(self):
        return len(self.__data)

    def clear(self):
        self.__data.clear()

    def to_list(self):
        return list(self.__data)

    def __str__(self):
        return str(self.__data)

# StrategicMazeSolver 클래스 (우선순위 큐 기반 전략적 탐색)
class StrategicMazeSolver:
    def __init__(self, maze):
        self.__maze = maze
        self.__maze_size = len(maze)
        self.__pqueue = PriorityQueue()
        self.__visited = set()
        self.__parent = {}
        # 출구 위치
        self.__goal = (self.__maze_size - 1, self.__maze_size - 1)

    def __is_exit(self, r, c):
        return (r, c) == self.__goal

    def __reconstruct_path(self, end):
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = self.__parent.get(cur)
        path.reverse()
        return path

    def solve(self, show_steps=True):
        self.__pqueue.clear()
        self.__visited.clear()
        self.__parent.clear()
        step = 0

        # 1단계: 시작위치를 거리와 함께 큐에 삽입
        start = (0, 0)
        goal_r, goal_c = self.__goal
        start_dist = heuristic(0, 0, goal_r, goal_c)  # 외부 함수 활용

        self.__pqueue.enqueue((start_dist, start))
        self.__visited.add(start)
        self.__parent[start] = None

        print("\n" + "=" * 60)
        print("      미로 탐색 시작 (전략적 탐색 - 우선순위 큐)")
        print(f"      출구: {self.__goal}  |  시작→출구 거리: {start_dist:.3f}")
        print("=" * 60)
        print("\n  ── 초기 미로 ────────────────────────────────")
        print_maze(self.__maze, current=start)

        while True:
            step += 1

            # 2단계: 큐가 공백이면 출구 없음
            if self.__pqueue.is_empty():
                print("\n  ❌ 출구를 찾지 못했습니다!")
                return False

            # 2단계: 가장 거리가 짧은 위치 꺼냄
            dist, current = self.__pqueue.dequeue()
            r, c = current

            if show_steps:
                print_step(step, current, dist,
                           self.__pqueue.to_list(),
                           self.__maze, self.__visited)

            # 3단계: 출구이면 탐색 성공
            if self.__is_exit(r, c):
                path = self.__reconstruct_path(current)
                print("\n" + "=" * 60)
                print("  ✅ 출구 발견! 전략적 탐색 성공!")
                print(f"  총 탐색 단계  : {step}")
                print(f"  탐색한 칸 수  : {len(self.__visited)}")
                print(f"  경로 길이     : {len(path)}칸")
                print(f"  탐색 경로     : {path}")
                print("\n  ── 탐색 경로 결과 ───────────────────────────")
                print_maze(self.__maze,
                           visited=self.__visited,
                           path=set(path))
                return True

            # 4단계: 주변 탐색 후 미방문 통로를 거리와 함께 큐에 삽입
            for nr, nc in get_neighbors(r, c, self.__maze_size):
                if (nr, nc) not in self.__visited and \
                   is_passable(self.__maze, nr, nc):
                    # 슬라이드 핵심: (x, y, -d) → 거리가 짧을수록 우선순위 높음
                    d = heuristic(nr, nc, goal_r, goal_c)  # 외부 함수 활용
                    self.__pqueue.enqueue((d, (nr, nc)))
                    self.__visited.add((nr, nc))
                    self.__parent[(nr, nc)] = current

        return False


# 슬라이드와 동일한 미로 (0: 통로, 1: 벽)
map_data = [
    ['1', '1', '1', '1', '1', '1'],
    ['0', '0', '0', '0', '0', '1'],
    ['1', '0', '1', '1', '0', '1'],
    ['1', '0', '1', '0', '0', '0'],
    ['1', '0', '1', '0', 'x', '1'],
    ['1', '1', '1', '1', '1', '1'],
]

maze = [[0 if cell in ('0', 'x') else 1 for cell in row] for row in map_data]

print("MAZE_SIZE =", len(maze))
print("\n  ── 원본 미로 구조 ───────────────────────────")
print_maze(maze)

# 전략적 탐색 실행
solver = StrategicMazeSolver(maze)
solver.solve(show_steps=True)

# 출구 없는 미로 테스트
print("\n\n" + "=" * 60)
print("        출구 없는 미로 테스트")
print("=" * 60)

no_exit_maze = [
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
]

solver2 = StrategicMazeSolver(no_exit_maze)
solver2.solve(show_steps=False)