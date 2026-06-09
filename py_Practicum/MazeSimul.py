import flet as ft
import ssl
import time
import random

# =================================================================
# Flet 실행 시 발생하는 urllib.error.URLError 방지용 전역 설정
# =================================================================
ssl._create_default_https_context = ssl._create_unverified_context


# ── 백엔드 미로 탐색용 헬퍼 함수 ──
def get_neighbors_ordered(r, c, maze_size):
    """
    탐색 우선순위: 우 -> 하 -> 좌 -> 상
    스택(LIFO) 특성에 맞춰 역순인 [상 -> 좌 -> 하 -> 우] 순서로 push하여
    꺼낼 때는 [우 -> 하 -> 좌 -> 상] 순서로 탐색하도록 유도합니다.
    """
    candidate_directions = [(-1, 0), (0, -1), (1, 0), (0, 1)]

    valid_neighbors = []
    for dr, dc in candidate_directions:
        nr, nc = r + dr, c + dc
        if 0 <= nr < maze_size and 0 <= nc < maze_size:
            valid_neighbors.append((nr, nc))
    return valid_neighbors

def is_passable(maze, r, c):
    """해당 위치가 통로인지 검사 (0이면 통로, 1이면 벽)"""
    return maze[r][c] == 0


# ── 랜덤 미로 생성기 ──
def generate_random_maze(size=6, start=(1, 0), end=(3, 5), solvable_chance=0.7):
    """
    재귀적 백트래킹(Recursive Backtracking) 알고리즘으로 미로를 생성합니다.
    
    - solvable_chance: 탈출 가능한 미로가 생성될 확률 (0.0 ~ 1.0)
    - 탈출 불가능한 경우: 생성된 미로에서 출구로 이어지는 마지막 통로를 벽으로 막습니다.
    """
    # 1. 모든 셀을 벽(1)으로 초기화
    maze = [[1] * size for _ in range(size)]

    # 2. 시작점과 출구는 항상 통로(0)로 확보
    sr, sc = start
    er, ec = end
    maze[sr][sc] = 0
    maze[er][ec] = 0

    # 3. 재귀적 백트래킹으로 내부 통로 생성
    #    짝수 인덱스 셀들을 "방(room)"으로 보고, 2칸씩 이동하며 벽을 뚫어나갑니다.
    def carve(r, c):
        directions = [(0, 2), (2, 0), (0, -2), (-2, 0)]
        random.shuffle(directions)
        for dr, dc in directions:
            nr, nc = r + dr, c + dc
            if 1 <= nr < size - 1 and 1 <= nc < size - 1 and maze[nr][nc] == 1:
                # 사이 벽 제거
                maze[r + dr // 2][c + dc // 2] = 0
                maze[nr][nc] = 0
                carve(nr, nc)

    # 짝수 좌표에서 시작 (내부 셀 기준)
    start_carve_r = 1 if sr % 2 == 1 else 2
    start_carve_c = 1 if sc % 2 == 1 else 2
    # 내부 시작점 연결
    maze[start_carve_r][start_carve_c] = 0
    carve(start_carve_r, start_carve_c)

    # 4. 시작점을 내부 미로와 연결 (시작점 바로 오른쪽/아래 셀이 통로면 연결)
    for dr, dc in [(0, 1), (1, 0)]:
        nr, nc = sr + dr, sc + dc
        if 0 <= nr < size and 0 <= nc < size and maze[nr][nc] == 0:
            maze[sr][sc] = 0
            break
    else:
        # 연결이 안 됐으면 강제 개통
        maze[sr][sc + 1] = 0 if sc + 1 < size else maze[sr + 1][sc]

    # 5. 출구를 내부 미로와 연결
    for dr, dc in [(0, -1), (-1, 0), (0, 1), (1, 0)]:
        nr, nc = er + dr, ec + dc
        if 0 <= nr < size and 0 <= nc < size and maze[nr][nc] == 0:
            break
    else:
        # 출구 왼쪽 강제 개통
        if ec - 1 >= 0:
            maze[er][ec - 1] = 0
        else:
            maze[er - 1][ec] = 0

    # 6. 탈출 불가능 미로 처리: solvable_chance 확률로 탈출 가능 여부 결정
    is_solvable = random.random() < solvable_chance
    if not is_solvable:
        # 출구 주변의 모든 인접 통로를 벽으로 막아 탈출 불가능하게 만듦
        blocked = False
        for dr, dc in [(0, -1), (-1, 0), (1, 0), (0, 1)]:
            nr, nc = er + dr, ec + dc
            if 0 <= nr < size and 0 <= nc < size and maze[nr][nc] == 0:
                maze[nr][nc] = 1
                blocked = True
        # 혹시 출구가 고립되지 않았으면 BFS로 경로를 차단
        if not blocked:
            maze[er][ec] = 1  # 출구 자체를 잠금 (탈출 불가)

    return maze


# ── ArrayStack 클래스 ──
class ArrayStack:
    def __init__(self, max_size=None):
        self.__data = []
        self.__max_size = max_size

    def push(self, e):
        self.__data.append(e)

    def pop(self):
        return self.__data.pop()

    def peek(self):
        return self.__data[-1]

    def is_empty(self):
        return len(self.__data) == 0

    def clear(self):
        self.__data.clear()

    def to_list(self):
        return list(self.__data)


# ── Flet GUI 통합 MazeSimulator 클래스 ──
class MazeSimulator:
    def __init__(self):
        self.maze_size = 6
        self.start = (1, 0)
        self.end = (3, 5)
        # 실행 시마다 새로운 랜덤 미로 생성
        self.maze = generate_random_maze(
            size=self.maze_size,
            start=self.start,
            end=self.end,
            solvable_chance=0.7
        )
        self.stack = ArrayStack()
        self.visited = set()
        self.path = []
        self.step = 0
        self.is_running = False
        self.game_over = False

    def init_solver(self):
        """탐색 알고리즘 데이터 상태 초기화 + 새 미로 생성"""
        self.stack.clear()
        self.visited.clear()
        self.path = []
        self.step = 0
        self.game_over = False

        # 초기화(리셋) 시마다 새로운 랜덤 미로 생성
        self.maze = generate_random_maze(
            size=self.maze_size,
            start=self.start,
            end=self.end,
            solvable_chance=0.7
        )

        start = self.start
        self.stack.push(start)

    def next_search_step(self):
        """1칸씩 탐색을 수행하며 정밀 DFS 시뮬레이션을 수행"""
        if self.game_over:
            return "ALREADY_DONE"

        if self.stack.is_empty():
            self.game_over = True
            return "NO_EXIT"

        current = self.stack.pop()
        r, c = current

        if current in self.visited:
            return self.next_search_step()

        self.step += 1
        self.visited.add(current)
        self.path.append(current)

        er, ec = self.end
        if r == er and c == ec:
            self.game_over = True
            return "SUCCESS"

        for nr, nc in get_neighbors_ordered(r, c, self.maze_size):
            if (nr, nc) not in self.visited and is_passable(self.maze, nr, nc):
                self.stack.push((nr, nc))

        return "SEARCHING"

    def run(self, page: ft.Page):
        page.title = "6x6 제한 난이도 끝판왕 미로 시뮬레이터"
        page.window_width = 800
        page.window_height = 700
        page.window_min_width = 650
        page.window_min_height = 600
        page.padding = 0
        page.bgcolor = "#1e1e2e"

        sim = self
        sim.init_solver()

        # UI 격자판 틀 정의
        maze_column_layout = ft.Column(spacing=6, alignment=ft.MainAxisAlignment.CENTER)

        status_text = ft.Text("초기화 상태. [자동 탐색]을 누르면 역대급 백트래킹(되돌아 나오기) 연산이 시작됩니다!", size=12, color="#a6adc8", italic=True)
        step_txt = ft.Text("단계: 0", size=14, color="#cdd6f4", weight=ft.FontWeight.BOLD)
        stack_txt = ft.Text("[]", size=13, color="#89b4fa", font_family="Consolas, monospace")

        def draw_maze_ui():
            maze_column_layout.controls.clear()
            current_pos = sim.path[-1] if sim.path else sim.start

            for r in range(sim.maze_size):
                row_controls = []

                for c in range(sim.maze_size):
                    cell_value = sim.maze[r][c]
                    bg_color = "#313244"
                    cell_content = None

                    # 1. 벽 컴포넌트 시각화
                    if cell_value == 1:
                        bg_color = "#45475a"
                        cell_content = ft.Icon(ft.Icons.BLOCK, color="#f38ba8", size=16)

                    # 2. 실시간 쥐 위치 하이라이트
                    elif (r, c) == current_pos:
                        bg_color = "#89b4fa"
                        cell_content = ft.Icon(ft.Icons.DIRECTIONS_WALK, color="#1e1e2e", size=18)

                    # 3. 방문 완료 흔적 (체크 마크)
                    elif (r, c) in sim.visited:
                        bg_color = "#252636"
                        cell_content = ft.Icon(ft.Icons.CHECK, color="#a6adc8", size=14)

                    # 시작점(S) 및 출구(E) 표식 고정
                    er, ec = sim.end
                    if (r, c) == sim.start and current_pos != sim.start:
                        cell_content = ft.Text("S", color="#a6e3a1", weight=ft.FontWeight.BOLD)
                    elif (r, c) == sim.end and current_pos != sim.end:
                        cell_content = ft.Text("E", color="#f9e2af", weight=ft.FontWeight.BOLD)

                    # 탈출 성공 시, 실제 최종 이동 경로를 연두색 격자로 하이라이트
                    if sim.game_over and (r, c) in sim.path and not sim.stack.is_empty():
                        bg_color = "#a6e3a1"
                        if (r, c) != current_pos:
                            cell_content = ft.Icon(ft.Icons.CHECK, color="#1e1e2e", size=14)

                    row_controls.append(
                        ft.Container(
                            content=cell_content,
                            alignment=ft.Alignment(0, 0),
                            bgcolor=bg_color,
                            width=50,
                            height=50,
                            border_radius=4,
                        )
                    )

                maze_column_layout.controls.append(
                    ft.Row(row_controls, spacing=6, alignment=ft.MainAxisAlignment.CENTER)
                )

            step_txt.value = f"단계: {sim.step}"
            stack_txt.value = f"{sim.stack.to_list()}"
            page.update()

        def perform_one_step_ui():
            result = sim.next_search_step()

            if result == "SUCCESS":
                status_text.value = f"🎉 하드코어 미로 정복 완료! 역대급 백트래킹을 극복하고 출구 안착!"
                status_text.color = "#a6e3a1"
                sim.is_running = False
            elif result == "NO_EXIT":
                status_text.value = "❌ 출구를 찾지 못했습니다. 미로가 막혀있습니다."
                status_text.color = "#f38ba8"
                sim.is_running = False
            elif result == "SEARCHING":
                status_text.value = "출구 코앞에서 트랩에 걸려 대규모 백트래킹 가동 중..."
                status_text.color = "#89b4fa"

            draw_maze_ui()
            return result

        # ── 이벤트 버튼 제어 핸들러 ──
        def on_step_click(e):
            if sim.is_running or sim.game_over:
                return
            perform_one_step_ui()

        def on_auto_click(e):
            if sim.game_over:
                return

            sim.is_running = True
            status_text.value = "자동 탐색 가동 중..."
            status_text.color = "#a6e3a1"

            while sim.is_running:
                res = perform_one_step_ui()
                if res in ("SUCCESS", "NO_EXIT"):
                    break
                time.sleep(0.35)

        def on_reset_click(e):
            sim.is_running = False
            sim.init_solver()
            status_text.value = "새로운 미로가 생성되었습니다. 다시 탐색을 시작해보세요."
            status_text.color = "#a6adc8"
            draw_maze_ui()

        # 버튼 빌더 헬퍼 함수
        def toolbar_btn(label, icon, color, handler):
            return ft.ElevatedButton(
                content=ft.Row(
                    [
                        ft.Icon(icon, color="#1e1e2e", size=18),
                        ft.Text(label, color="#1e1e2e", size=13, weight=ft.FontWeight.BOLD),
                    ],
                    spacing=4,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                on_click=handler,
                style=ft.ButtonStyle(
                    bgcolor={"": color},
                    shape=ft.RoundedRectangleBorder(radius=6),
                    padding=ft.Padding(14, 10, 14, 10),
                ),
            )

        # ── 레이아웃 조립 ──
        header_area = ft.Container(
            content=ft.Row([
                ft.Text("6x6 제한 난이도 끝판왕 미로 탐색기", size=18, color="#cdd6f4", weight=ft.FontWeight.BOLD),
            ], alignment=ft.MainAxisAlignment.START),
            bgcolor="#181825",
            padding=ft.Padding(20, 15, 20, 15),
            border=ft.Border(bottom=ft.BorderSide(1, "#313244"))
        )

        control_panel = ft.Container(
            content=ft.Row([
                toolbar_btn("자동 탐색", ft.Icons.PLAY_ARROW_ROUNDED, "#a6e3a1", on_auto_click),
                toolbar_btn("다음 단계", ft.Icons.SKIP_NEXT_ROUNDED, "#89b4fa", on_step_click),
                toolbar_btn("초기화", ft.Icons.REFRESH_ROUNDED, "#fab387", on_reset_click),
            ], spacing=10),
            padding=ft.Padding(20, 12, 20, 12),
            bgcolor="#181825",
            border=ft.Border(bottom=ft.BorderSide(1, "#313244"))
        )

        dashboard_monitor = ft.Container(
            content=ft.Column([
                ft.Row([
                    ft.Text("스택 내부 원소 상태: ", size=13, color="#6c7086", weight=ft.FontWeight.BOLD),
                    stack_txt
                ]),
                ft.Row([step_txt])
            ]),
            padding=ft.Padding(20, 10, 20, 10),
            bgcolor="#11111b"
        )

        maze_display_frame = ft.Container(
            content=maze_column_layout,
            alignment=ft.Alignment(0, 0),
            padding=ft.Padding(40, 30, 40, 30),
            expand=True
        )

        status_area = ft.Container(
            content=ft.Row([status_text]),
            bgcolor="#11111b",
            padding=ft.Padding(16, 6, 16, 6)
        )

        hidden_box = ft.Container(width=0, height=0, opacity=0)

        page.add(
            ft.Column([
                header_area,
                control_panel,
                dashboard_monitor,
                maze_display_frame,
                status_area,
                hidden_box
            ], expand=True, spacing=0)
        )

        draw_maze_ui()


# ── 실행부 ──
simulator = MazeSimulator()
ft.app(target=simulator.run)