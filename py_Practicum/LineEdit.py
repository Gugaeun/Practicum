import flet as ft
import ssl

ssl._create_default_https_context = ssl._create_unverified_context


# ── 데이터 검증 함수 ──
def is_valid_insert_pos(data, pos):
    return 0 <= pos <= len(data)

def is_valid_pos(data, pos):
    return 0 <= pos < len(data)

def display_list(label, data):
    print(f"[{label}] → {data}")

def sort_items(data, key=None, reverse=False):
    return sorted(data, key=key, reverse=reverse)

def merge_lists(lst1, lst2):
    return lst1 + lst2


# ── ArrayList 클래스 ──
class ArrayList:
    def __init__(self, max_size=None):
        self.__data = []
        self.__max_size = max_size

    def insert(self, pos, e):
        if self.is_full():
            raise OverflowError("리스트가 가득 찼습니다")
        if not is_valid_insert_pos(self.__data, pos):
            raise IndexError(f"유효하지 않은 삽입 위치: {pos}")
        self.__data.insert(pos, e)

    def delete(self, pos):
        if not is_valid_pos(self.__data, pos):
            raise IndexError(f"유효하지 않은 삭제 위치: {pos}")
        return self.__data.pop(pos)

    def append(self, e):
        if self.is_full():
            raise OverflowError("리스트가 가득 찼습니다")
        self.__data.append(e)

    def is_empty(self):
        return len(self.__data) == 0

    def is_full(self):
        if self.__max_size is None:
            return False
        return len(self.__data) >= self.__max_size

    def get_entry(self, pos):
        if not is_valid_pos(self.__data, pos):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        return self.__data[pos]

    def size(self):
        return len(self.__data)

    def clear(self):
        self.__data.clear()

    def find(self, item):
        try:
            return self.__data.index(item)
        except ValueError:
            return -1

    def replace(self, pos, item):
        if not is_valid_pos(self.__data, pos):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        self.__data[pos] = item

    def sort(self, key=None, reverse=False):
        self.__data = sort_items(self.__data, key=key, reverse=reverse)

    def merge(self, other):
        if isinstance(other, ArrayList):
            self.__data = merge_lists(self.__data, other.to_list())
        elif isinstance(other, list):
            self.__data = merge_lists(self.__data, other)
        else:
            raise TypeError("list 또는 ArrayList만 병합 가능합니다")

    def display(self, label="ArrayList"):
        display_list(label, self.__data)

    def display_with_lineno(self):
        for i in range(len(self.__data)):
            print(f"  {i+1}: {self.__data[i]}")

    def to_list(self):
        return list(self.__data)

    def __len__(self):
        return self.size()

    def __str__(self):
        return str(self.__data)


# ── LineEditor 클래스 ──
class LineEditor:
    def __init__(self):
        self.__lines = ArrayList()

    def insert_line(self, line_no, text):
        pos = line_no - 1
        self.__lines.insert(pos, text)

    def delete_line(self, line_no):
        pos = line_no - 1
        return self.__lines.delete(pos)

    def replace_line(self, line_no, text):
        pos = line_no - 1
        self.__lines.replace(pos, text)

    def get_lines(self):
        return self.__lines.to_list()

    def size(self):
        return self.__lines.size()

    def is_empty(self):
        return self.__lines.is_empty()

    def load_file(self, filename):
        self.__lines.clear()
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f:
                self.__lines.append(line.rstrip('\n'))

    def save_file(self, filename):
        with open(filename, 'w', encoding='utf-8') as f:
            for i in range(self.__lines.size()):
                f.write(self.__lines.get_entry(i) + '\n')

    def run(self, page: ft.Page):
        page.title = "ArrayList 라인 편집기"
        page.window_width = 720
        page.window_height = 620
        page.window_min_width = 520
        page.window_min_height = 420
        page.padding = 0
        page.bgcolor = "#1e1e2e"

        editor = self
        selected_index = [-1]

        # ── 상태바 ──
        status_text = ft.Text("준비", size=12, color="#a6adc8", italic=True)

        def set_status(msg, error=False):
            status_text.value = msg
            status_text.color = "#f38ba8" if error else "#a6e3a1"
            page.update()

        # ── 입력창 & 삽입 위치 ──
        text_input = ft.TextField(
            label="내용",
            hint_text="삽입하거나 변경할 텍스트를 입력하세요",
            bgcolor="#313244",
            border_color="#45475a",
            focused_border_color="#89b4fa",
            label_style=ft.TextStyle(color="#cdd6f4"),
            color="#cdd6f4",
            cursor_color="#89b4fa",
            expand=True,
        )

        insert_pos_group = ft.RadioGroup(
            content=ft.Row([
                ft.Radio(value="before", label="앞에 삽입", fill_color="#89b4fa"),
                ft.Radio(value="after",  label="뒤에 삽입", fill_color="#89b4fa"),
            ]),
            value="before",
        )

        # ── 리스트뷰 ──
        line_list = ft.ListView(expand=True, spacing=2, padding=8)

        def build_row(idx, text, selected=False):
            bg        = "#313244" if selected else "transparent"
            num_color = "#89b4fa" if selected else "#6c7086"
            txt_color = "#cdd6f4" if selected else "#bac2de"

            def on_click(e, i=idx):
                selected_index[0] = i
                refresh_list()

            return ft.Container(
                content=ft.Row([
                    ft.Text(f"{idx + 1:>3}", size=13, color=num_color, width=36,
                            font_family="Consolas, monospace"),
                    ft.Text(text or " ", size=13, color=txt_color, expand=True,
                            no_wrap=True, font_family="Consolas, monospace"),
                ]),
                bgcolor=bg,
                border_radius=4,
                padding=ft.Padding(8, 4, 8, 4),
                on_click=on_click,
                ink=True,
            )

        def refresh_list():
            line_list.controls.clear()
            lines = editor.get_lines()
            if not lines:
                line_list.controls.append(
                    ft.Container(
                        content=ft.Text("(비어 있음)", color="#6c7086", italic=True, size=13),
                        padding=ft.Padding(12, 8, 12, 8),
                    )
                )
            else:
                for i, text in enumerate(lines):
                    line_list.controls.append(
                        build_row(i, text, selected=(i == selected_index[0]))
                    )
            page.update()

        # ── 버튼 동작 ──
        def on_insert(e):
            text = text_input.value
            if not text:
                set_status("삽입할 내용을 입력하세요", error=True)
                return
            n   = editor.size()
            sel = selected_index[0]
            direction = insert_pos_group.value

            if n == 0:
                pos = 0
            elif sel == -1:
                set_status("삽입할 위치의 행을 먼저 선택하세요", error=True)
                return
            else:
                pos = sel if direction == "before" else sel + 1

            try:
                editor.insert_line(pos + 1, text)
                selected_index[0] = pos
                text_input.value = ""
                refresh_list()
                set_status(f"{pos + 1}번 행에 삽입했습니다")
            except Exception as ex:
                set_status(str(ex), error=True)

        def on_delete(e):
            sel = selected_index[0]
            if sel == -1 or sel >= editor.size():
                set_status("삭제할 행을 선택하세요", error=True)
                return
            try:
                removed = editor.delete_line(sel + 1)
                if editor.is_empty():
                    selected_index[0] = -1
                elif sel >= editor.size():
                    selected_index[0] = editor.size() - 1
                refresh_list()
                set_status(f"'{removed}' 삭제했습니다")
            except Exception as ex:
                set_status(str(ex), error=True)

        def on_replace(e):
            sel  = selected_index[0]
            text = text_input.value
            if sel == -1 or sel >= editor.size():
                set_status("변경할 행을 선택하세요", error=True)
                return
            if not text:
                set_status("변경할 내용을 입력하세요", error=True)
                return
            try:
                editor.replace_line(sel + 1, text)
                text_input.value = ""
                refresh_list()
                set_status(f"{sel + 1}번 행을 변경했습니다")
            except Exception as ex:
                set_status(str(ex), error=True)

        def on_load_result(e):
            if e.files:
                path = e.files[0].path
                try:
                    editor.load_file(path)
                    selected_index[0] = -1
                    refresh_list()
                    set_status(f"'{path}' 로드 완료 ({editor.size()}줄)")
                except Exception as ex:
                    set_status(f"로드 실패: {ex}", error=True)

        def on_save_result(e):
            if e.path:
                try:
                    editor.save_file(e.path)
                    set_status(f"'{e.path}' 저장 완료 ({editor.size()}줄)")
                except Exception as ex:
                    set_status(f"저장 실패: {ex}", error=True)

        file_picker_load = ft.FilePicker()
        file_picker_load.on_result = on_load_result
        
        file_picker_save = ft.FilePicker()
        file_picker_save.on_result = on_save_result

        def on_load(e):
            file_picker_load.pick_files(
                dialog_title="파일 불러오기",
                allowed_extensions=["txt", "py", "md", "csv"],
            )

        def on_save(e):
            file_picker_save.save_file(
                dialog_title="파일 저장",
                file_name="document.txt",
            )

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
        toolbar = ft.Container(
            content=ft.Row([
                toolbar_btn("삽입",     ft.Icons.ADD,                  "#a6e3a1", on_insert),
                toolbar_btn("삭제",     ft.Icons.DELETE_OUTLINE,       "#f38ba8", on_delete),
                toolbar_btn("변경",     ft.Icons.EDIT_OUTLINED,        "#89dceb", on_replace),
                ft.VerticalDivider(width=1, color="#45475a"),
                toolbar_btn("불러오기", ft.Icons.FOLDER_OPEN_OUTLINED, "#fab387", on_load),
                toolbar_btn("저장",     ft.Icons.SAVE_OUTLINED,        "#b4befe", on_save),
            ], spacing=8),
            bgcolor="#181825",
            padding=ft.Padding(16, 10, 16, 10),
        )

        doc_header = ft.Container(
            content=ft.Text("문서", size=11, color="#6c7086", weight=ft.FontWeight.W_600),
            bgcolor="#181825",
            padding=ft.Padding(16, 6, 16, 6),
            border=ft.Border(bottom=ft.BorderSide(1, "#313244")),
        )

        input_area = ft.Container(
            content=ft.Column([
                ft.Row([text_input]),
                ft.Row([
                    ft.Text("삽입 위치:", color="#a6adc8", size=13),
                    insert_pos_group,
                ]),
            ], spacing=6),
            bgcolor="#181825",
            padding=ft.Padding(16, 10, 16, 10),
            border=ft.Border(top=ft.BorderSide(1, "#313244")),
        )

        status_area = ft.Container(
            content=status_text,
            bgcolor="#11111b",
            padding=ft.Padding(16, 6, 16, 6),
        )

        # 파일 피커를 투명 인간 컨테이너 생성
        hidden_pickers = ft.Container(
            content=ft.Row([file_picker_load, file_picker_save]),
            width=0,
            height=0,
            opacity=0,
        )

        page.add(
            ft.Column([
                toolbar,
                doc_header,
                ft.Container(content=line_list, expand=True, bgcolor="#1e1e2e"),
                input_area,
                status_area,
                hidden_pickers,
            ], expand=True, spacing=0)
        )

        refresh_list()


# ── 실행부 ──
editor = LineEditor()
ft.app(target=editor.run)