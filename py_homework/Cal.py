import flet as ft
# 계산기
class Cal:
    def __init__(self, num):
        self.num = num

    def calculate(self, pm):
        result = self.num[0]

        for i in range(1, len(self.num)):
            if pm == "+":
                result += self.num[i]
            elif pm == "-":
                result -= self.num[i]
            elif pm == "/":
                result /= self.num[i]
            else:
                result *= self.num[i]

        return result

    def avg(self):
        return sum(self.num) / len(self.num)

    def maxnum(self):
        return max(self.num)

    def minnum(self):
        return min(self.num)


def main(page: ft.Page):
    page.title = "Cal Calculator"
    page.bgcolor = "#f1f3f5"
    page.window_width = 380
    page.window_height = 550

    input_box = ft.TextField(
        label="숫자 입력 (공백으로 구분)",
        bgcolor="white"
    )

    op = ft.Dropdown(
        label="연산 선택",
        options=[
            ft.dropdown.Option("+"),
            ft.dropdown.Option("-"),
            ft.dropdown.Option("*"),
            ft.dropdown.Option("/"),
        ]
    )

    result = ft.Text(size=18, weight="bold")

    def run_calc(e):
        try:
            nums = list(map(int, input_box.value.split()))
            pm = op.value

            cal = Cal(nums)

            result.value = (
                f"계산 결과: {cal.calculate(pm)}\n"
                f"평균: {cal.avg()}\n"
                f"최대값: {cal.maxnum()}\n"
                f"최소값: {cal.minnum()}"
            )

        except:
            result.value = "입력 오류 (숫자만 입력)"

        page.update()

    page.add(
        ft.Container(
            content=ft.Column([
                ft.Text("🧮 Calculator", size=24, weight="bold"),
                input_box,
                op,
                ft.ElevatedButton("계산하기", on_click=run_calc),
                result
            ], spacing=15),
            padding=20,
            bgcolor="white",
            border_radius=15,
            shadow=ft.BoxShadow(blur_radius=20)
        )
        
    )

ft.app(target=main)