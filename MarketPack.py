import flet as ft
import random


# 1. 상품 DB 생성
물품명 = [
    "비누", "치약", "샴푸", "린스", "바디워시", "폼클렌징", "칫솔", "수건",
    "휴지", "물티슈", "세탁세제", "섬유유연제", "주방세제", "수세미", "고무장갑",
    "쌀", "라면", "햇반", "생수", "우유", "계란", "두부", "콩나물", "시금치",
    "양파", "감자", "고구마", "사과", "바나나", "오렌지", "귤", "토마토",
    "김치", "된장", "고추장", "간장", "식용유", "참기름", "소금", "설탕",
    "커피", "차", "과자", "빵", "젤리", "초콜릿", "음료수", "맥주", "소주",
    "고기(돼지고기)", "고기(소고기)", "닭고기", "생선", "오징어", "새우", "게",
    "쌀국수", "파스타", "잼", "버터", "치즈", "요거트", "아이스크림", "통조림",
    "냉동만두", "어묵", "햄", "소시지", "김", "미역", "다시마", "멸치",
    "밀가루", "부침가루", "튀김가루", "빵가루", "식초", "소스", "향신료",
    "양초", "성냥", "건전지", "전구", "쓰레기봉투", "지퍼백", "호일", "랩"
]

물품DB = {}
for 품목 in 물품명:
    물품DB[품목] = {
        "가격": random.randrange(1000, 10000, 100),
        "재고": random.randint(3, 15),
        "매출": 0
    }

장바구니 = {}



# Flet UI

def main(page: ft.Page):
    page.title = "🛒 마트 계산 프로그램"

    # 구버전 호환
    try:
        page.scroll = ft.ScrollMode.AUTO
    except:
        page.scroll = "auto"

    장바구니뷰 = ft.Column()
    재고뷰 = ft.Column()
    총합텍스트 = ft.Text("총 합계: 0원", size=20, weight="bold")


    # 장바구니 업데이트
    def 장바구니_업데이트():
        장바구니뷰.controls.clear()
        합계 = 0

        for 상품, 수량 in 장바구니.items():
            가격 = 물품DB[상품]["가격"]
            합계 += 가격 * 수량

            장바구니뷰.controls.append(
                ft.Text(f"{상품} - {수량}개 ({가격}원)")
            )

        총합텍스트.value = f"총 합계: {합계}원"
        page.update()


    # 재고 업데이트
    def 재고_업데이트():
        재고뷰.controls.clear()

        for 상품, 정보 in 물품DB.items():
            재고뷰.controls.append(
                ft.Text(f"{상품} | 재고: {정보['재고']} | 매출: {정보['매출']}원")
            )

        page.update()


    # 상품 담기
    def 담기(e):
        상품 = e.control.data

        if 물품DB[상품]["재고"] <= 0:
            try:
                page.show_snack_bar(ft.SnackBar(ft.Text(f"{상품} 재고 없음")))
            except:
                pass
            return

        장바구니[상품] = 장바구니.get(상품, 0) + 1
        장바구니_업데이트()


    # 결제
    def 결제(e):
        for 상품, 수량 in 장바구니.items():
            재고 = 물품DB[상품]["재고"]

            if 재고 >= 수량:
                물품DB[상품]["재고"] -= 수량
                물품DB[상품]["매출"] += 물품DB[상품]["가격"] * 수량
            else:
                물품DB[상품]["매출"] += 물품DB[상품]["가격"] * 재고
                물품DB[상품]["재고"] = 0

        장바구니.clear()
        장바구니_업데이트()
        재고_업데이트()

        try:
            page.show_snack_bar(ft.SnackBar(ft.Text("결제 완료!")))
        except:
            pass


    # 상품 버튼 생성
    상품버튼들 = []
    for 상품 in 물품DB:
        상품버튼들.append(
            ft.ElevatedButton(
                f"{상품} ({물품DB[상품]['가격']}원)",
                data=상품,
                on_click=담기
            )
        )


    # UI 구성
    page.add(
        ft.Text("🛍️ 상품 선택", size=24, weight="bold"),

        ft.Container(
            content=ft.Row(
                상품버튼들,
                scroll="auto"
            ),
            padding=10
        ),

        ft.Divider(),

        ft.Text("🧺 장바구니", size=20),
        장바구니뷰,
        총합텍스트,

        ft.Row([
            ft.ElevatedButton("결제", on_click=결제),
        ]),

        ft.Divider(),

        ft.Text("📦 재고 및 매출", size=20),
        재고뷰
    )

    재고_업데이트()



# 실행
ft.app(target=main)