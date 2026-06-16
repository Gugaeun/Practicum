# 🐍 Python Practicum

Python을 활용한 실습 과제 모음입니다.  
기초 프로그램부터 자료구조 구현, Flet을 이용한 UI 개발까지 포함합니다.

---

## 📌 기초 프로그램 실습

### 🎳 볼링 점수 계산 프로그램
- 랜덤 게임 생성 및 점수 계산 구현
- 스트라이크 / 스페어 처리 로직 구현
- 프레임별 점수 출력 기능
- 결과 화면 예시
  - <img width="706" height="282" alt="볼링 결과" src="https://github.com/user-attachments/assets/e6f19c2d-1b04-4268-aa72-f499719d1fe8" />
- [예시 코드](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/bowling_flet.py)

### 🛒 장바구니 프로그램
- UI 기반 상품 추가/삭제 기능
- 총 금액 자동 계산

### 📞 전화번호부 프로그램
- 클래스 기반 설계
- 데이터 저장 및 조회 기능 구현

### ✊ 가위바위보 프로그램

### 🧮 계산기 프로그램
- 결과 화면 예시
  - <img width="353" height="312" alt="계산기 결과" src="https://github.com/user-attachments/assets/fa65c8c3-0d3f-48f8-af9e-34b61a07a957" />
- [예시 코드](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/Cal.py)

---

## 📌 자료구조 실습 1 (Flet UI 포함)

Python을 이용한 자료구조 중 List, Set, Stack의 예제와 Flet을 사용하여 UI 생성

### 📋 List (배열, 연결된 구조 포함)
- [ArrayList.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/ArrayList.py)
- <img width="300" height="261" alt="List 예시" src="https://github.com/user-attachments/assets/ce25a8cf-a37c-4308-b49e-a9b771a26ef3" />

### 🔢 Set (배열, 연결된 구조 포함)
- [ArraySet.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/ArraySet.py)
- <img width="300" height="383" alt="Set 예시" src="https://github.com/user-attachments/assets/750f82d8-2e70-4ea7-86dc-fa92-d2b89cad" />

### 📚 Stack (배열, 연결된 구조 포함)
- [ArrayStack.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/ArrayStack.py)
- <img width="392" height="800" alt="Stack 예시" src="https://github.com/user-attachments/assets/42ec0420-ce9e-4cb3-bfee-385d7eb89eed" />

### 🧮 괄호 포함 수식 계산기
- [ExprCalc.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/ExprCalc.py)
- <img width="800" height="450" alt="수식 계산기" src="https://github.com/user-attachments/assets/0703c030-3394-4720-b947-f4987c57c33a" />

### ✏️ 라인편집기
- [LineEdit.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/LineEdit.py)
- <img width="800" height="450" alt="라인편집기" src="https://github.com/user-attachments/assets/668e3da6-e084-4666-b98b-21cdc10df95d" />

### 🌀 미로 탐색 (깊이 우선 탐색)
- [MazeSimul.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/MazeSimul.py)
- 출구 찾기 실패
  - <img width="800" height="500" alt="미로 실패" src="https://github.com/user-attachments/assets/f7dbeae0-1d9e-411b-8e88-9c3ee309338c" />
- 출구 찾기 성공
  - <img width="800" height="500" alt="미로 성공" src="https://github.com/user-attachments/assets/e3cec584-0395-4191-b40d-a89c06abb9b2" />

---

## 📌 자료구조 실습 2 - Queue & Deque

Queue / Deque 계열 자료구조 구현 및 응용 프로그램

### 🗂 Queue (선형 큐)
- 배열 기반 선형 큐 구현
- [ArrayQueue.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/SecondPython/ArrayQueue.py)
- <img width="274" height="343" alt="스크린샷 2026-06-16 124415" src="https://github.com/user-attachments/assets/b55dec4d-67fd-442d-b707-bbc402151c74" />

### 🔄 CircularQueue (원형 큐)
- 선형 큐의 메모리 낭비 문제를 개선한 원형 구조
- [CircularQueue.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/SecondPython/CircularQueue.py)

### ↔️ Deque (양방향 큐)
- 앞/뒤 양방향 삽입·삭제가 가능한 구조
- [ArrayDeque.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/SecondPython/ArrayDeque.py)
- [CircularDeque.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/SecondPython/CircularDeque.py)

### ⭐ PriorityQueue (우선순위 큐)
- 값의 우선순위에 따라 순서가 결정되는 큐
- [PriorityQueue.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/SecondPython/PriorityQueue.py)

### 🌀 Queue를 활용한 미로 탐색 (너비 우선 탐색, BFS)
- Queue를 사용하여 미로의 모든 경로를 탐색
- [QueueMaze.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/SecondPython/QueueMaze.py)

### 🌀 우선순위 큐를 활용한 미로 탐색
- 우선순위 큐를 사용하여 최단 경로 탐색
- [PriorityQueueMaze.py](https://github.com/Gugaeun/Practicum/blob/main/py_Practicum/SecondPython/PriorityQueueMaze.py)

---

## 💡 배운 점

- 조건문과 반복문을 활용한 로직 설계 능력 향상
- Python을 활용한 프로그램 구조화 및 함수 분리 경험
- Flet을 이용한 간단한 UI 프로그램 개발 경험
- 자료구조(List, Set, Stack)를 직접 구현하며 동작 원리 이해
- Queue / Deque / 우선순위 큐를 직접 구현하며 동작 원리 이해
- DFS(깊이 우선)와 BFS(너비 우선) 탐색 알고리즘 비교 경험
