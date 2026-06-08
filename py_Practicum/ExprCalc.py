import flet as ft
import ssl


# Flet 실행 시 발생하는 urllib.error.URLError 방지용 전역 설정
ssl._create_default_https_context = ssl._create_unverified_context


# ── 백엔드 연산 및 수식 보조 기능 ──
def get_priority(op):
    if op in ('+', '-'):
        return 1
    if op in ('*', '/'):
        return 2
    if op == '^':
        return 3
    return 0

def is_operator(ch):
    return ch in '+-*/^'

def apply_op(op, a, b):
    if op == '+': return a + b
    if op == '-': return a - b
    if op == '*': return a * b
    if op == '/':
        if b == 0:
            raise ZeroDivisionError("0으로 나눌 수 없습니다")
        return a / b
    if op == '^': return a ** b


# ── 코드 독립 구동을 위한 ArrayStack 클래스 구현 ──
class ArrayStack:
    def __init__(self):
        self.__top = []

    def push(self, e):
        self.__top.append(e)

    def pop(self):
        if self.is_empty():
            raise IndexError("스택이 비어 있습니다")
        return self.__top.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("스택이 비어 있습니다")
        return self.__top[-1]

    def is_empty(self):
        return len(self.__top) == 0

    def clear(self):
        self.__top.clear()


# ── ExprCalculator 클래스 ──
class ExprCalculator:
    def __init__(self):
        self.__stack = ArrayStack()

    def infix_to_postfix(self, expr):
        self.__stack.clear()
        output = []
        tokens = expr.split()

        for token in tokens:
            if token.lstrip('-').replace('.','',1).isdigit():
                output.append(token)
            elif token == '(':
                self.__stack.push(token)
            elif token == ')':
                while not self.__stack.is_empty() and self.__stack.peek() != '(':
                    output.append(self.__stack.pop())
                if not self.__stack.is_empty():
                    self.__stack.pop()
            elif is_operator(token):
                while (not self.__stack.is_empty()
                       and self.__stack.peek() != '('
                       and get_priority(self.__stack.peek()) >= get_priority(token)):
                    output.append(self.__stack.pop())
                self.__stack.push(token)

        while not self.__stack.is_empty():
            output.append(self.__stack.pop())

        return ' '.join(output)

    def infix_to_prefix(self, expr):
        self.__stack.clear()
        tokens = expr.split()[::-1]
        tokens = ['(' if t == ')' else ')' if t == '(' else t for t in tokens]

        output = []
        for token in tokens:
            if token.lstrip('-').replace('.','',1).isdigit():
                output.append(token)
            elif token == '(':
                self.__stack.push(token)
            elif token == ')':
                while not self.__stack.is_empty() and self.__stack.peek() != '(':
                    output.append(self.__stack.pop())
                if not self.__stack.is_empty():
                    self.__stack.pop()
            elif is_operator(token):
                while (not self.__stack.is_empty()
                       and self.__stack.peek() != '('
                       and get_priority(self.__stack.peek()) > get_priority(token)):
                    output.append(self.__stack.pop())
                self.__stack.push(token)

        while not self.__stack.is_empty():
            output.append(self.__stack.pop())

        return ' '.join(output[::-1])

    def eval_postfix(self, expr):
        self.__stack.clear()
        tokens = expr.split()

        for token in tokens:
            if token.lstrip('-').replace('.','',1).isdigit():
                self.__stack.push(float(token))
            elif is_operator(token):
                b = self.__stack.pop()
                a = self.__stack.pop()
                self.__stack.push(apply_op(token, a, b))

        if self.__stack.is_empty():
            return 0
        result = self.__stack.pop()
        return int(result) if result == int(result) else result

    def eval_infix(self, expr):
        postfix = self.infix_to_postfix(expr)
        return self.eval_postfix(postfix)

    # ── Flet GUI 런타임 환경 (0.85.2 규격 적용) ──
    def run(self, page: ft.Page):
        page.title = "수식 변환 & 계산 대시보드"
        page.window_width = 750
        page.window_height = 600
        page.window_min_width = 550
        page.window_min_height = 500
        page.padding = 0
        page.bgcolor = "#1e1e2e"

        calc_engine = self

        # 결과를 출력할 UI 텍스트 판넬 정의
        infix_txt = ft.Text("-", size=15, color="#cdd6f4", font_family="Consolas, monospace")
        prefix_txt = ft.Text("-", size=15, color="#fab387", font_family="Consolas, monospace")
        postfix_txt = ft.Text("-", size=15, color="#89b4fa", font_family="Consolas, monospace")
        result_txt = ft.Text("-", size=24, color="#a6e3a1", weight=ft.FontWeight.BOLD, font_family="Consolas, monospace")
        status_msg = ft.Text("수식을 입력하고 계산 버튼을 누르세요 (토큰 사이 공백 필수 예: 3 + 4 * 2)", size=12, color="#a6adc8", italic=True)

        # 입력창 컴포넌트
        input_field = ft.TextField(
            label="중위 표기식(Infix) 입력",
            hint_text="예: ( 1 + 2 ) * ( 3 + 4 )",
            bgcolor="#313244",
            border_color="#45475a",
            focused_border_color="#89b4fa",
            label_style=ft.TextStyle(color="#cdd6f4"),
            color="#cdd6f4",
            cursor_color="#89b4fa",
            expand=True
        )

        def on_calculate(e):
            expr = input_field.value.strip()
            if not expr:
                status_msg.value = "오류: 수식을 입력해 주세요"
                status_msg.color = "#f38ba8"
                page.update()
                return

            try:
                # 백엔드 계산기 함수 연동
                postfix_res = calc_engine.infix_to_postfix(expr)
                prefix_res = calc_engine.infix_to_prefix(expr)
                final_res = calc_engine.eval_infix(expr)

                # UI 바인딩 변수 업데이트
                infix_txt.value = expr
                prefix_txt.value = prefix_res
                postfix_txt.value = postfix_res
                result_txt.value = str(final_res)

                status_msg.value = "성공적으로 연산되었습니다."
                status_msg.color = "#a6e3a1"
            except ZeroDivisionError as ze:
                status_msg.value = f"오류: {ze}"
                status_msg.color = "#f38ba8"
            except Exception as ex:
                status_msg.value = f"수식 분석 오류 (공백 입력을 확인하세요)"
                status_msg.color = "#f38ba8"
            
            page.update()

        # 예제 항목 클릭 핸들러
        def on_example_click(e, expr_string):
            input_field.value = expr_string
            on_calculate(None)

        # 0.85.2 전용 버튼 생성 헬퍼 함수
        def safe_btn(label, icon, color, handler):
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
                    padding=ft.Padding(16, 12, 16, 12),
                ),
            )

        # 0.85.2 전용 예제 태그 생성용 칩 버튼 헬퍼
        def example_chip(expr_string):
            def click_wrapper(e):
                on_example_click(e, expr_string)
            return ft.ElevatedButton(
                content=ft.Text(expr_string, color="#cdd6f4", size=12),
                on_click=click_wrapper,
                style=ft.ButtonStyle(
                    bgcolor={"": "#313244"},
                    shape=ft.RoundedRectangleBorder(radius=15),
                    padding=ft.Padding(10, 6, 10, 6),
                )
            )

        # ── 레이아웃 요소 구성 ──
        header_area = ft.Container(
            content=ft.Text("수식 계산기 대시보드", size=18, color="#cdd6f4", weight=ft.FontWeight.BOLD),
            bgcolor="#181825",
            padding=ft.Padding(20, 15, 20, 15),
            border=ft.Border(bottom=ft.BorderSide(1, "#313244"))
        )

        input_container = ft.Container(
            content=ft.Column([
                ft.Row([
                    input_field,
                    safe_btn("계산 & 변환", ft.Icons.PLAY_ARROW_ROUNDED, "#a6e3a1", on_calculate)
                ], spacing=10),
                ft.Text("테스트 케이스 단축 선택:", size=12, color="#6c7086", weight=ft.FontWeight.BOLD),
                ft.Row([
                    example_chip("3 + 4 * 2"),
                    example_chip("( 3 + 4 ) * 2"),
                    example_chip("2 ^ 3 + 1"),
                    example_chip("( 1 + 2 ) * ( 3 + 4 )"),
                ], spacing=6, wrap=True)
            ], spacing=10),
            padding=ft.Padding(20, 15, 20, 15),
            bgcolor="#181825",
            border=ft.Border(bottom=ft.BorderSide(1, "#313244"))
        )

        # 결과 디스플레이 행 빌더
        def display_row(title, control_txt, title_color):
            return ft.Container(
                content=ft.Row([
                    ft.Text(f"{title}:", width=120, color=title_color, size=14, weight=ft.FontWeight.BOLD),
                    control_txt
                ]),
                padding=ft.Padding(15, 10, 15, 10),
                bgcolor="#181825",
                border_radius=6
            )

        result_container = ft.Container(
            content=ft.ListView([
                display_row("입력 중위(Infix)", infix_txt, "#cdd6f4"),
                display_row("변환 전위(Prefix)", prefix_txt, "#fab387"),
                display_row("변환 후위(Postfix)", postfix_txt, "#89b4fa"),
                ft.Container(
                    content=ft.Row([
                        ft.Text("최종 계산 결과:", width=120, color="#a6e3a1", size=15, weight=ft.FontWeight.BOLD),
                        result_txt
                    ]),
                    padding=ft.Padding(15, 15, 15, 15),
                    bgcolor="#242535",
                    border_radius=6,
                    border=ft.Border(
                        top=ft.BorderSide(1, "#45475a"),
                        bottom=ft.BorderSide(1, "#45475a"),
                        left=ft.BorderSide(1, "#45475a"),
                        right=ft.BorderSide(1, "#45475a")
                    )
                )
            ], expand=True, spacing=10),
            padding=ft.Padding(20, 20, 20, 20),
            expand=True
        )

        status_area = ft.Container(
            content=status_msg,
            bgcolor="#11111b",
            padding=ft.Padding(20, 8, 20, 8)
        )

        # 버전을 타는 에러 딱지를 완전 차단하는 빈 컨테이너 더미
        hidden_box = ft.Container(width=0, height=0, opacity=0)

        page.add(
            ft.Column([
                header_area,
                input_container,
                result_container,
                status_area,
                hidden_box
            ], expand=True, spacing=0)
        )

        page.update()


# ── 프로그램 실행부 ──
calculator_app = ExprCalculator()
ft.app(target=calculator_app.run)