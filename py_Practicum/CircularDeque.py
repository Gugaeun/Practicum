# 원형 덱

def is_full_check(front, rear, max_size):
    return (rear + 1) % max_size == front

def is_empty_check(front, rear):
    return front == rear

def calc_size(front, rear, max_size):
    return (rear - front + max_size) % max_size

def display_deque(data, front, rear, max_size):
    print(f"\n  [ 덱 시각화 - 최대 저장: {max_size - 1}개 ]")
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

    # 실제 저장 데이터 순서 출력
    items = []
    if not is_empty_check(front, rear):
        idx = (front + 1) % max_size
        while True:
            items.append(data[idx])
            if idx == rear:
                break
            idx = (idx + 1) % max_size
    print(f"  저장 순서 (front→rear) : {items}")
    print(f"  front={front}, rear={rear}, size={calc_size(front, rear, max_size)}")


# CircularQueue 클래스 (부모)
class CircularQueue:
    def __init__(self, max_size=8):
        self._max_size = max_size
        self._data = [None] * max_size
        self._front = 0
        self._rear = 0

    def enqueue(self, e):
        if self.is_full():
            raise OverflowError("큐가 가득 찼습니다")
        self._rear = (self._rear + 1) % self._max_size
        self._data[self._rear] = e

    def dequeue(self):
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다")
        self._front = (self._front + 1) % self._max_size
        item = self._data[self._front]
        self._data[self._front] = None
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다")
        return self._data[(self._front + 1) % self._max_size]

    def is_full(self):
        return is_full_check(self._front, self._rear, self._max_size)

    def is_empty(self):
        return is_empty_check(self._front, self._rear)

    def size(self):
        return calc_size(self._front, self._rear, self._max_size)

    def clear(self):
        self._data = [None] * self._max_size
        self._front = 0
        self._rear = 0

    def display(self):
        display_deque(self._data, self._front, self._rear, self._max_size)



# Deque 클래스(원형 큐 상속 받기)
class Deque(CircularQueue):
    def __init__(self, max_size=8):
        super().__init__(max_size)

    # IsFull: 덱이 가득 찼는지 검사 (부모 재사용)
    def is_full(self):
        return super().is_full()

    # isEmpty: 덱이 비어있는지 검사(상속 사용)
    def is_empty(self):
        return super().is_empty()

    # AddFront: 맨 앞(전단)에 새로운 요소 e를 추가
    def add_front(self, e):
        if self.is_full():
            raise OverflowError("덱이 가득 찼습니다")
        self._data[self._front] = e
        self._front = (self._front - 1 + self._max_size) % self._max_size
        print(f"  AddFront({e}) 완료 → front={self._front}")

    # DeleteFront: 맨 앞(전단)의 요소 e를 꺼내서 반환
    def delete_front(self):
        if self.is_empty():
            raise IndexError("덱이 비어 있습니다")
        item = super().dequeue()
        print(f"  DeleteFront() → {item}")
        return item

    # getFront: 맨 앞(전단)의 요소 e를 꺼내지 않고 반환
    def get_front(self):
        if self.is_empty():
            raise IndexError("덱이 비어 있습니다")
        item = super().peek()
        print(f"  getFront() → {item}")
        return item

    # AddRear: 맨 뒤(후단)에 새로운 요소 e를 추가
    def add_rear(self, e):
        if self.is_full():
            raise OverflowError("덱이 가득 찼습니다")
        super().enqueue(e)
        print(f"  AddRear({e}) 완료 → rear={self._rear}")

    # DeleteRear: 맨 뒤(후단)의 요소 e를 꺼내서 반환
    def delete_rear(self):
        if self.is_empty():
            raise IndexError("덱이 비어 있습니다")
        item = self._data[self._rear]
        self._data[self._rear] = None
        self._rear = (self._rear - 1 + self._max_size) % self._max_size
        print(f"  DeleteRear() → {item}")
        return item

    # getRear: 맨 뒤(후단)의 요소 e를 꺼내지 않고 반환
    def get_rear(self):
        if self.is_empty():
            raise IndexError("덱이 비어 있습니다")
        item = self._data[self._rear]
        print(f"  getRear() → {item}")
        return item

    # Size: 덱의 모든 항목들의 개수를 반환 (부모 재사용)
    def size(self):
        s = super().size()
        print(f"  Size() → {s}")
        return s

    # Clear: 덱을 공백상태로 만든다 (부모 재사용)
    def clear(self):
        super().clear()
        print("  Clear() 완료 → 덱 공백상태")

    # Display: 외부 함수 활용 (부모 재사용)
    def display(self):
        super().display()


print("=" * 60)
print("         Deque ADT 테스트 (원형 큐 상속)")
print("=" * 60)

dq = Deque(max_size=8)   # 실제 저장 가능: 7개

# AddRear 테스트
print("\n▶ AddRear 테스트 (뒤에 삽입)")
dq.add_rear(10)
dq.add_rear(20)
dq.add_rear(30)
dq.display()

# AddFront 테스트
print("\n▶ AddFront 테스트 (앞에 삽입)")
dq.add_front(5)
dq.add_front(1)
dq.display()

# getFront / getRear 테스트
print("\n▶ getFront / getRear 테스트 (삭제 없이 확인)")
dq.get_front()                                     # 1  (삭제 X)
dq.get_rear()                                      # 30 (삭제 X)
dq.display()                                       # 그대로

# DeleteFront 테스트
print("\n▶ DeleteFront 테스트 (앞에서 삭제)")
dq.delete_front()                                  # 1
dq.delete_front()                                  # 5
dq.display()

# DeleteRear 테스트
print("\n▶ DeleteRear 테스트 (뒤에서 삭제)")
dq.delete_rear()                                   # 30
dq.delete_rear()                                   # 20
dq.display()

# Size 테스트
print("\n▶ Size 테스트")
dq.size()                                          # 1

# isEmpty / isFull 테스트
print("\n▶ isEmpty / isFull 테스트")
print(f"  isEmpty : {dq.is_empty()}")              # False
print(f"  isFull  : {dq.is_full()}")               # False

# isFull 확인
print("\n▶ isFull 확인 (max_size=8, 저장가능=7)")
dq.add_rear(100)
dq.add_rear(200)
dq.add_rear(300)
dq.add_front(50)
dq.add_front(40)
dq.add_front(30)
print(f"  isFull  : {dq.is_full()}")               # True
dq.display()
try:
    dq.add_rear(999)
except OverflowError as e:
    print(f"  [AddRear 오류]  → {e}")
try:
    dq.add_front(999)
except OverflowError as e:
    print(f"  [AddFront 오류] → {e}")

# Clear 테스트
print("\n▶ Clear 테스트")
dq.clear()
dq.display()
print(f"  isEmpty : {dq.is_empty()}")              # True

# 예외 처리 테스트
print("\n▶ 예외 처리 테스트")
for desc, fn in [
    ("빈 덱 DeleteFront", lambda: dq.delete_front()),
    ("빈 덱 DeleteRear",  lambda: dq.delete_rear()),
    ("빈 덱 getFront",    lambda: dq.get_front()),
    ("빈 덱 getRear",     lambda: dq.get_rear()),
]:
    try:
        fn()
    except IndexError as e:
        print(f"  [{desc}] → {e}")