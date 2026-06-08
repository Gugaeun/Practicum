import flet as ft
import ssl
import time

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
        # [난이도 끝판왕] 6x6 규격 내에서 구현 가능한 가장 꼬인 미로 데이터
        # 출구 바로 앞까지 도달했다가 덫에 걸려 대규모 백트래킹을 수행하는 구조입니다.
        self.maze = [
            [1, 1, 1, 1, 1, 1],  # 0행: 전체 벽
            [0, 0, 0, 0, 0, 1],  # 1행: 시작점 (1,0)
            [1, 0, 1, 1, 0, 1],  # 2행: 중앙에 통로와 벽을 교차 배치하여 함정 생성
            [1, 0, 0, 0, 0, 0],  # 3행: [3][5]가 최종 출구(E). 바로 옆 [3][4]에서 통과 못하게 가로막음!
            [1, 1, 0, 1, 1, 1],  # 4행: 아래 바닥으로 돌아서 우회하게 만듦
            [1, 1, 0, 0, 0, 1]   # 5행: 굽이치는 최하단 탈출 베이스 통로
        ]
        self.maze_size = len(self.maze)
        self.stack = ArrayStack()
        self.visited = set()
        self.path = []
        self.step = 0
        self.is_running = False
        self.game_over = False

    def init_solver(self):
        """탐색 알고리즘 데이터 상태 초기화"""
        self.stack.clear()
        self.visited.clear()
        self.path = []
        self.step = 0
        self.game_over = False
        
        # 시작 위치 고정: 1행 0열
        start = (1, 0)
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

        # 출구 위치 고정: 3행 5열
        if r == 3 and c == 5:
            self.game_over = True
            return "SUCCESS"

        # 규칙대로 정렬된 이웃을 가져와서 스택에 쌓습니다.
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
            current_pos = sim.path[-1] if sim.path else (1, 0)

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
                    if (r, c) == (1, 0) and current_pos != (1, 0):
                        cell_content = ft.Text("S", color="#a6e3a1", weight=ft.FontWeight.BOLD)
                    elif (r, c) == (3, 5) and current_pos != (3, 5):
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
                time.sleep(0.35)  # 복잡한 동선을 더 흥미진진하게 볼 수 있도록 딜레이 살짝 조정

        def on_reset_click(e):
            sim.is_running = False
            sim.init_solver()
            status_text.value = "초기화되었습니다. 다시 탐색을 시작해보세요."
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