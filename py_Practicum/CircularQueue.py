# 원형 큐
# 원형 큐

def is_full_check(front, rear, max_size):
    """원형 큐가 가득 찼는지 검사"""
    return (rear + 1) % max_size == front

def is_empty_check(front, rear):
    """원형 큐가 비어 있는지 검사"""
    return front == rear

def display_circular_queue(data, front, rear, max_size):
    """원형 큐를 시각적으로 출력"""
    print(f"\n  [ 원형 큐 시각화 - 크기: {max_size} ]")
    print("  ┌" + "──────┬" * (max_size - 1) + "──────┐")

    # 인덱스 행
    print("  │", end="")
    for i in range(max_size):
        print(f"  [{i}] │", end="")
    print()

    print("  ├" + "──────┼" * (max_size - 1) + "──────┤")

    # 데이터 행
    print("  │", end="")
    for i in range(max_size):
        val = str(data[i]) if data[i] is not None else " "
        print(f"  {val:<4}│", end="")
    print()

    print("  └" + "──────┴" * (max_size - 1) + "──────┘")

    # Front / Rear 표시
    marker = ["      "] * max_size
    if front == rear:
        marker[front] = " F=R  "
    else:
        marker[front] = "  F   "
        marker[rear]  = "  R   "
    print("   " + " ".join(marker))

    # 실제 데이터 출력
    items = []
    idx = (front + 1) % max_size
    while idx != (rear + 1) % max_size and not is_empty_check(front, rear):
        if idx == (rear + 1) % max_size:
            break
        items.append(data[idx])
        if idx == rear:
            break
        idx = (idx + 1) % max_size

    print(f"  저장된 데이터 (front→rear) : {items}")
    print(f"  front={front}, rear={rear}")


class CircularQueue:
    def __init__(self, max_size=8):
        """
        원형 큐 초기화
        - 실제 저장 가능 크기는 max_size - 1 (한 칸은 front/rear 구분용)
        - front: 첫 번째 데이터 바로 앞 인덱스
        - rear : 마지막 데이터 인덱스
        """
        self.__max_size = max_size
        self.__data = [None] * max_size
        self.__front = 0
        self.__rear = 0

    # Enqueue: 요소 e를 큐의 맨 뒤에 추가
    def enqueue(self, e):
        if self.is_full():
            raise OverflowError("원형 큐가 가득 찼습니다")
        # rear를 한 칸 앞으로 이동 (원형)
        self.__rear = (self.__rear + 1) % self.__max_size
        self.__data[self.__rear] = e
        print(f"  enqueue({e}) → rear={self.__rear}")

    # Dequeue: 큐의 맨 앞 요소를 꺼내 반환
    def dequeue(self):
        if self.is_empty():
            raise IndexError("원형 큐가 비어 있습니다")
        # front를 한 칸 앞으로 이동 (원형)
        self.__front = (self.__front + 1) % self.__max_size
        item = self.__data[self.__front]
        self.__data[self.__front] = None   # 꺼낸 자리 None 처리
        print(f"  dequeue() → {item}  (front={self.__front})")
        return item

    # IsFull: 외부 함수 활용
    def is_full(self):
        return is_full_check(self.__front, self.__rear, self.__max_size)

    # isEmpty: 외부 함수 활용
    def is_empty(self):
        return is_empty_check(self.__front, self.__rear)

    # Peek: 맨 앞 요소를 삭제하지 않고 반환
    def peek(self):
        if self.is_empty():
            raise IndexError("원형 큐가 비어 있습니다")
        return self.__data[(self.__front + 1) % self.__max_size]

    # Size: 저장된 항목 수 반환
    def size(self):
        return (self.__rear - self.__front + self.__max_size) % self.__max_size

    # Clear: 큐를 공백상태로 만든다
    def clear(self):
        self.__data = [None] * self.__max_size
        self.__front = 0
        self.__rear = 0
        print("  원형 큐 초기화 완료")

    # Display: 외부 함수 활용해 출력
    def display(self):
        display_circular_queue(
            self.__data, self.__front, self.__rear, self.__max_size
        )

    def __str__(self):
        items = []
        idx = (self.__front + 1) % self.__max_size
        count = self.size()
        for _ in range(count):
            items.append(self.__data[idx])
            idx = (idx + 1) % self.__max_size
        return str(items)


# 출력해보기
print("=" * 60)
print("           CircularQueue ADT 테스트")
print("=" * 60)

cq = CircularQueue(max_size=6)  # 실제 저장 가능: 5개

# enqueue
print("\n▶ enqueue 테스트")
cq.enqueue(10)
cq.enqueue(20)
cq.enqueue(30)
cq.enqueue(40)
cq.display()

# peek
print("\n▶ peek 테스트")
print(f"  peek() → {cq.peek()}")                 # 10

# dequeue
print("\n▶ dequeue 테스트")
cq.dequeue()                                      # 10
cq.dequeue()                                      # 20
cq.display()

# 상태 확인
print("\n▶ 상태 확인")
print(f"  isEmpty : {cq.is_empty()}")             # False
print(f"  isFull  : {cq.is_full()}")              # False
print(f"  size    : {cq.size()}")                 # 2

# 원형 특성 확인 - dequeue 후 빈 앞자리에 다시 enqueue
print("\n▶ 원형 특성 테스트 (앞자리 재사용)")
cq.enqueue(50)
cq.enqueue(60)
cq.enqueue(70)                                    # 앞에서 빠진 자리 재사용
cq.display()

# isFull 테스트
print("\n▶ isFull 테스트")
print(f"  isFull  : {cq.is_full()}")              # True
try:
    cq.enqueue(99)
except OverflowError as e:
    print(f"  [enqueue 오류] → {e}")

# clear
print("\n▶ clear 테스트")
cq.clear()
cq.display()
print(f"  isEmpty : {cq.is_empty()}")             # True
