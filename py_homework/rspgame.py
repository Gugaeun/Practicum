import flet as ft
import random

def play_game(page: ft.Page):
    user_rsp = ["가위", "바위", "보"]
    user_wins = 0
    comp_wins = 0
    rounds = 0

    page.title = "🌸 가위바위보 🌸"
    page.bgcolor = "#fff5f7"  # 연한 핑크색

    result = ft.Text(size=20, color="#a61e4d", weight="bold")
    score = ft.Text(size=16, color="#c2255c")
    
    # 가위바위보 게임 시작하는 함수
    def play_round(e):
        nonlocal user_wins, comp_wins, rounds

        if rounds >= 5 or user_wins == 3 or comp_wins == 3:
            return

        user_sel = e.control.data

        # not in 은 != 와 같다.
        if user_sel not in user_rsp:
            result.value = "입력이 올바르지 않아요 🌸"
            page.update()
            return

        com_sel = random.choice(user_rsp)
        result.value = f"컴퓨터: {com_sel}"

        # 승패 판정하는 코드
        if user_sel == com_sel:
            result.value += "\n무승부입니다!"
        elif (user_sel == "가위" and com_sel == "보") or \
             (user_sel == "바위" and com_sel == "가위") or \
             (user_sel == "보" and com_sel == "바위"):
            result.value += "\n사용자 승리 🌸"
            user_wins += 1
        else:
            result.value += "\n컴퓨터 승리"
            comp_wins += 1

        rounds += 1

        score.value = f"{user_wins}승 {comp_wins}패 · {rounds}라운드"
        page.update()

    # 승패판정이 끝나고 다시 시작할 수 있게 하는 코드
    def reset_game(e):
        nonlocal user_wins, comp_wins, rounds
        user_wins = 0
        comp_wins = 0
        rounds = 0
        result.value = "다시 시작 🌸"
        score.value = ""
        page.update()

    # 🌸 카드 느낌 컨테이너를 만드는 코드
    card = ft.Container(
        content=ft.Column(
            [
                ft.Text("🌸 가위바위보 🌸", size=32, weight="bold", color="#880e4f"),
                ft.Text("🌷", size=14, color="#ad1457"),

                ft.Row(
                    [
                        ft.ElevatedButton("가위", data="가위", on_click=play_round),
                        ft.ElevatedButton("바위", data="바위", on_click=play_round),
                        ft.ElevatedButton("보", data="보", on_click=play_round),
                    ],
                    alignment=ft.MainAxisAlignment.CENTER
                ),

                result,
                score,

                ft.ElevatedButton("다시 시작", on_click=reset_game),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=15
        ),
        padding=30,
        border_radius=20,
        bgcolor="#ffffffcc",  # 반투명 흰색 (꽃잎 느낌)
        shadow=ft.BoxShadow(
            blur_radius=15,
            color="#f8bbd0"
        )
    )
    # 페이지에 UI를 추가하는 코드
    page.add(
        ft.Column(
            [
                ft.Text("🌸 🌸 🌸", size=20),
                card,
                ft.Text("🌷 🌸 🌷", size=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        )
    )

ft.app(target=play_game)