import flet as ft
import random

def main(page: ft.Page):
    page.title = "업다운 게임"
    page.bgcolor = "#f0f4f8"  # 배경색

    # randint => 랜덤 정수를 뽑아주는 함수, random 과 같이 쓰임
    answer = random.randint(1, 100)
    count = 0

    title = ft.Text("🎮 업다운 게임", size=25, weight="bold")

    # TextField => 사용자로부터 텍스트를 입력하게 함
    input_box = ft.TextField(
        label="숫자 입력 (1~100)",
        text_align="center",
        width=200
    )
    # tries = 시도를 표시하기 위한 변수
    result = ft.Text("시작!", size=18)
    tries = ft.Text("시도: 0")

    def check(e):
        nonlocal count
        # input_box.value = 입력창에 사용자가 입력한 값, .isdigit() = 문자열이 전부 숫자인지 검사하는 함수
        if input_box.value.isdigit():
            num = int(input_box.value)
            count += 1

            if num < answer:
                result.value = "UP!! "
                result.color = "skyblue"
            elif num > answer:
                result.value = "DOWN! "
                result.color = "red"
            else:
                result.value = "정답!!!"
                result.color = "green"

            tries.value = "시도: " + str(count)
            input_box.value = ""

        page.update()

    #ElevatedButton => 살짝 떠있는 듯하게 보이는 버튼
    button = ft.ElevatedButton("확인", on_click=check, width=200)

    # 꾸미기
    page.add(
        ft.Container(
            content=ft.Column(
                [title, input_box, button, result, tries],
                alignment="center",
                horizontal_alignment="center",
                spacing=15
            ),
            padding=30,
            border_radius=15,
            bgcolor="white"  # 카드 느낌
        )
    )

ft.app(target=main)