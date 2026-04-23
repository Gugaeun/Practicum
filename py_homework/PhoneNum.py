import flet as ft



# 1. 부모 클래스
class Person:
    def __init__(self, name, email, phone):
        self.name = name
        self.email = email
        self.phone = phone

    def get_info(self):
        return f"{self.name} / {self.phone}"



# 2. 자식 클래스 (상속)
class Worker(Person):
    def __init__(self, name, email, phone, job):
        super().__init__(name, email, phone)
        self.job = job

    def get_info(self):
        return f"{self.name} / {self.phone} / 직업: {self.job}"



# 3. 전화번호부 클래스
class PhoneBook:
    def __init__(self):
        self.persons = {}

    def add(self, person):
        self.persons[person.name] = person

    def delete(self, name):
        if name in self.persons:
            del self.persons[name]

    def get_all(self):
        return list(self.persons.values())



# 4. flet 메인 UI

def main(page: ft.Page):
    pb = PhoneBook()

    page.title = "📱 전화번호부"
    page.window_width = 400
    page.window_height = 700

    try:
        page.scroll = ft.ScrollMode.AUTO
    except:
        page.scroll = "auto"

    try:
        search_icon = ft.icons.SEARCH
        blue_color = ft.colors.BLUE_50
    except:
        search_icon = ft.Icons.SEARCH
        blue_color = ft.Colors.BLUE_50

    # 입력창
    name = ft.TextField(label="이름")
    email = ft.TextField(label="이메일")
    phone = ft.TextField(label="전화번호")
    job = ft.TextField(label="직업")

    # 검색창 기능
    search_field = ft.TextField(
        label="검색 (이름 / 전화번호)",
        prefix_icon=search_icon,
        on_change=lambda e: refresh_list()
    )

    contact_list = ft.Column()
    selected_name = {"value": None}


    # 리스트 갱신
    def refresh_list():
        keyword = search_field.value.lower() if search_field.value else ""
        contact_list.controls.clear()

        for p in pb.get_all():

            if keyword:
                if keyword not in p.name.lower() and keyword not in p.phone:
                    continue

            card = ft.Container(
                content=ft.Column([
                    ft.Text(p.name, size=18, weight="bold"),
                    ft.Text(p.phone),
                    ft.Text(p.email, size=12, color="grey"),
                    ft.Text(p.get_info(), size=12)  # 상속 메서드 활용
                ]),
                padding=10,
                border_radius=10,
                bgcolor=blue_color,
                on_click=lambda e, name=p.name: select_contact(name)
            )

            contact_list.controls.append(card)

        page.update()


    # 선택
    def select_contact(name_value):
        selected_name["value"] = name_value
        try:
            page.show_snack_bar(ft.SnackBar(ft.Text(f"{name_value} 선택됨")))
        except:
            pass


    # 추가 기능

    def add_contact(e):
        if not name.value:
            return

        # 👉 Person 대신 Worker 사용 (상속 객체)
        p = Worker(name.value, email.value, phone.value, job.value)
        pb.add(p)

        name.value = ""
        email.value = ""
        phone.value = ""
        job.value = ""

        refresh_list()


    # 삭제
    def delete_contact(e):
        if selected_name["value"]:
            pb.delete(selected_name["value"])
            selected_name["value"] = None
            refresh_list()


    # flet UI 구성 

    page.add(
        ft.Text("📒 전화번호부", size=24, weight="bold"),

        search_field,

        ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    name,
                    email,
                    phone,
                    job,
                    ft.ElevatedButton("➕ 추가", on_click=add_contact)
                ])
            )
        ),

        ft.Row([
            ft.ElevatedButton("🗑 선택 삭제", on_click=delete_contact)
        ]),

        ft.Divider(),

        ft.Text("연락처 목록", size=18, weight="bold"),
        contact_list
    )


# 실행
ft.app(target=main)