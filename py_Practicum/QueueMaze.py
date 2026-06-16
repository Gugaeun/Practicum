# 큐 기반 미로탐색(너비 우선)


def is_full_check(data, max_size):
    if max_size is None:
        return False
    return len(data) >= max_size

def is_empty_check(data):
    return len(data) == 0

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
                print(" 👣 ", end="")
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



# ArrayQueue 클래스
class ArrayQueue:
    def __init__(self, max_size=None):
        self.__data = []
        self.__max_size = max_size

    def enqueue(self, e):
        if self.is_full():
            raise OverflowError("큐가 가득 찼습니다")
        self.__data.append(e)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다")
        return self.__data.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다")
        return self.__data[0]

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


# BFSMazeSolver 클래스 (큐 기반 BFS)
class BFSMazeSolver:
    def __init__(self, maze):
        self.__maze = maze
        self.__maze_size = len(maze)
        self.__queue = ArrayQueue()
        self.__visited = set()
        # 경로 추적: 각 위치에 도달한 이전 위치 저장
        self.__parent = {}

    def __is_exit(self, r, c):
        return r == self.__maze_size - 1 and c == self.__maze_size - 1

    def __reconstruct_path(self, end):
        path = []
        cur = end
        while cur is not None:
            path.append(cur)
            cur = self.__parent.get(cur)
        path.reverse()
        return path

    def __print_step(self, step, current):
        print(f"\n  ── 단계 {step} ──────────────────────────")
        print(f"  현재 위치 : {current}")
        print(f"  큐 상태   : {self.__queue.to_list()}")
        print_maze(self.__maze,
                   current=current,
                   visited=self.__visited)

    def solve(self, show_steps=True):
        self.__queue.clear()
        self.__visited.clear()
        self.__parent.clear()
        step = 0

        # 1단계: 시작위치 큐에 삽입
        start = (0, 0)
        self.__queue.enqueue(start)
        self.__visited.add(start)
        self.__parent[start] = None

        print("\n" + "=" * 55)
        print("        미로 탐색 시작 (BFS - 너비 우선)")
        print("=" * 55)
        print("\n  ── 초기 미로 ──────────────────────────")
        print_maze(self.__maze, current=start)

        while True:
            step += 1

            # 2단계: 큐가 공백이면 출구 없음
            if self.__queue.is_empty():
                print("\n  ❌ 출구를 찾지 못했습니다!")
                return False

            # 2단계: 큐 앞에서 현재위치 꺼냄
            current = self.__queue.dequeue()
            r, c = current

            if show_steps:
                self.__print_step(step, current)

            # 3단계: 출구이면 탐색 성공
            if self.__is_exit(r, c):
                path = self.__reconstruct_path(current)

                print("\n" + "=" * 55)
                print("  ✅ 출구 발견! BFS 탐색 성공!")
                print(f"  총 탐색 단계  : {step}")
                print(f"  탐색한 칸 수  : {len(self.__visited)}")
                print(f"  최단 경로 길이: {len(path)}칸")
                print(f"  최단 경로     : {path}")
                print("\n  ── 최단 경로 결과 ─────────────────────")
                print_maze(self.__maze,
                           visited=self.__visited,
                           path=set(path))
                return True

            # 4단계: 주변(상우하좌) 탐색 후 미방문 통로 큐에 삽입
            for nr, nc in get_neighbors(r, c, self.__maze_size):
                if (nr, nc) not in self.__visited and \
                   is_passable(self.__maze, nr, nc):
                    self.__queue.enqueue((nr, nc))
                    self.__visited.add((nr, nc))
                    self.__parent[(nr, nc)] = current  # 경로 추적용

        return False

# 0: 통로, 1: 벽
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
print("\n  ── 원본 미로 구조 ─────────────────────")
print_maze(maze)

# BFS 탐색 실행
solver = BFSMazeSolver(maze)
solver.solve(show_steps=True)

# 출구 없는 미로 테스트
print("\n\n" + "=" * 55)
print("        출구 없는 미로 테스트")
print("=" * 55)

no_exit_maze = [
    [0, 1, 0],
    [0, 1, 0],
    [0, 1, 0],
]

solver2 = BFSMazeSolver(no_exit_maze)
solver2.solve(show_steps=False)