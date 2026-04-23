import random as rand
import flet as ft
import asyncio # 프레임이 하나씩 점수 나오게 해주는 도구(프로그램이 멈추지 않게 해주는 도구)


def bowling_random_game():
    result = []

    for frame in range(1, 11):
        if frame < 10:
            if rand.random() < 0.3:
                result.append(10)
            else:
                first = rand.randint(0, 9)
                second = rand.randint(0, 10 - first)
                result.append(first)
                result.append(second)
        else:
            first = rand.randint(0, 10)
            result.append(first)

            if first == 10:
                second = rand.randint(0, 10)
                result.append(second)

                if second == 10:
                    third = rand.randint(0, 10)
                else:
                    third = rand.randint(0, 10 - second)

                result.append(third)
            else:
                second = rand.randint(0, 10 - first)
                result.append(second)

                if first + second == 10:
                    third = rand.randint(0, 10)
                    result.append(third)

    return result


def score_bowling_random_game(result):
    score = 0
    index = 0
    frame_scores = []

    for frame in range(10):
        if result[index] == 10:
            score += 10 + result[index+1] + result[index+2]
            frame_scores.append(score)
            index = index + 1
        elif result[index] + result[index+1] == 10:
            score += 10 + result[index+2]
            frame_scores.append(score)
            index = index + 2
        else:
            score += result[index] + result[index+1]
            frame_scores.append(score)
            index = index + 2

    return frame_scores


def score_Cal(n, prev=None):
    if n == 10:
        return "X"
    elif prev is not None and n + prev == 10:
        return "/"
    elif n == 0:
        return "-"
    return str(n)



# 프레임 UI

def make_frame(frame_num):
    return ft.Column([
        ft.Text(str(frame_num), size=12),
        ft.Row([
            ft.Container(width=30, height=25, border=ft.border.all(1)),
            ft.Container(width=30, height=25, border=ft.border.all(1))
        ], spacing=0),
        ft.Container(width=60, height=30, border=ft.border.all(1))
    ], spacing=0)


def update_frame(frame_ui, rolls, score):
    cells = frame_ui.controls[1].controls

    for i in range(len(cells)):
        if i < len(rolls):
            prev = rolls[i-1] if i > 0 else None
            cells[i].content = ft.Text(score_Cal(rolls[i], prev))
        else:
            cells[i].content = ft.Text("")

    frame_ui.controls[2].content = ft.Text(str(score))



# 메인 flet UI

def main(page: ft.Page):

    page.title = "🎳 볼링 점수판"

    frames = []
    board = ft.Row(spacing=5)

    for i in range(10):
        f = make_frame(i+1)
        frames.append(f)
        board.controls.append(f)

    # 최종 점수 Text
    total_score_text = ft.Text("", size=20, weight="bold")

    async def run_game(e):
        total_score_text.value = ""  # 초기화
        result = bowling_random_game()
        scores = score_bowling_random_game(result)

        index = 0

        for frame in range(10):

            if result[index] == 10:
                rolls = [10]
                index += 1
            else:
                rolls = [result[index], result[index+1]]
                index += 2

            update_frame(frames[frame], rolls, scores[frame])

            page.update()
            await asyncio.sleep(0.7) # time 이 오류가 나서, asyncio 사용

        # 마지막에 총 점수 출력
        await asyncio.sleep(0.5)
        total_score_text.value = f"🎯 최종 점수: {scores[-1]}"
        page.update()

    # 중앙 정렬
    page.add(
        ft.Column(
            [
                ft.Text("🎳 볼링 점수판", size=22, weight="bold"),
                ft.Row(
                    [ft.ElevatedButton("게임 실행", on_click=run_game)],
                    alignment="center"
                ),
                ft.Row(
                    [board],
                    alignment="center"
                ),
                total_score_text
            ],
            horizontal_alignment="center"
        )
    )


ft.app(target=main)