# 우선순위 큐

def is_full_check(data, max_size):
    if max_size is None:
        return False
    return len(data) >= max_size

def is_empty_check(data):
    return len(data) == 0

def find_highest_priority(data):
    if not data:
        return -1
    best = 0
    for i in range(1, len(data)):
        if _get_priority(data[i]) < _get_priority(data[best]):
            best = i
    return best

def _get_priority(item):
    return item[0] if isinstance(item, tuple) else item

def display_pqueue(data):
    if not data:
        print("  [ 비어있는 우선순위 큐 ]")
        return

    print("\n  [ 우선순위 큐 현황 ]")
    print("  ┌────────┬──────────────┐")
    print("  │ 우선순위│    값        │")
    print("  ├────────┼──────────────┤")

    # 정렬해서 출력 (시각적 표현용, 내부 데이터 변경 X)
    sorted_data = sorted(data, key=lambda x: _get_priority(x))
    for i, item in enumerate(sorted_data):
        if isinstance(item, tuple):
            pri, val = item[0], item[1]
        else:
            pri, val = item, item
        marker = " ← 최우선" if i == 0 else ""
        print(f"  │   {str(pri):<5}│  {str(val):<12}│{marker}")
    print("  └────────┴──────────────┘")
    print(f"  저장된 요소 수: {len(data)}")


# PriorityQueue 클래스
class PriorityQueue:
    def __init__(self, max_size=None):
        self.__data = []
        self.__max_size = max_size

    # Enqueue: 우선순위를 가진 요소 e를 추가
    def enqueue(self, e):
        if self.is_full():
            raise OverflowError("우선순위 큐가 가득 찼습니다")
        self.__data.append(e)
        if isinstance(e, tuple):
            print(f"  Enqueue({e}) → 우선순위:{e[0]}, 값:{e[1]}")
        else:
            print(f"  Enqueue({e}) → 우선순위:{e}")

    # Dequeue: 가장 우선순위가 높은 요소를 꺼내 반환
    def dequeue(self):
        if self.is_empty():
            raise IndexError("우선순위 큐가 비어 있습니다")
        idx = find_highest_priority(self.__data)   # 외부 함수 활용
        item = self.__data.pop(idx)
        if isinstance(item, tuple):
            print(f"  Dequeue() → 우선순위:{item[0]}, 값:{item[1]}")
        else:
            print(f"  Dequeue() → {item}")
        return item

    # IsFull: 외부 함수 활용
    def is_full(self):
        return is_full_check(self.__data, self.__max_size)

    # isEmpty: 외부 함수 활용
    def is_empty(self):
        return is_empty_check(self.__data)

    # Peek: 가장 우선순위 높은 요소를 삭제하지 않고 반환
    def peek(self):
        if self.is_empty():
            raise IndexError("우선순위 큐가 비어 있습니다")
        idx = find_highest_priority(self.__data)   # 외부 함수 활용
        item = self.__data[idx]
        if isinstance(item, tuple):
            print(f"  Peek() → 우선순위:{item[0]}, 값:{item[1]}")
        else:
            print(f"  Peek() → {item}")
        return item

    # Size: 모든 항목들의 개수 반환
    def size(self):
        s = len(self.__data)
        print(f"  Size() → {s}")
        return s

    # Clear: 큐를 공백상태로 만든다
    def clear(self):
        self.__data.clear()
        print("  Clear() → 우선순위 큐 공백상태")

    # Display: 외부 함수 활용
    def display(self):
        display_pqueue(self.__data)

    def __str__(self):
        return str(self.__data)



# 1. 숫자 단독 테스트
print("=" * 60)
print("       우선순위 큐 테스트 1 - 숫자 단독")
print("  (숫자가 작을수록 우선순위 높음)")
print("=" * 60)

pq = PriorityQueue(max_size=7)

print("\n▶ Enqueue 테스트")
pq.enqueue(30)
pq.enqueue(10)
pq.enqueue(50)
pq.enqueue(20)
pq.enqueue(40)
pq.display()

print("\n▶ Peek 테스트 (삭제 없이 확인)")
pq.peek()                                          # 10 (삭제 X)
pq.display()                                       # 그대로

print("\n▶ Dequeue 테스트 (우선순위 순으로 나옴)")
pq.dequeue()                                       # 10
pq.dequeue()                                       # 20
pq.display()

print("\n▶ Size / isEmpty / isFull")
pq.size()                                          # 3
print(f"  isEmpty : {pq.is_empty()}")              # False
print(f"  isFull  : {pq.is_full()}")               # False


# 2. 튜플 (우선순위, 값) 테스트
print("\n\n" + "=" * 60)
print("       우선순위 큐 테스트 2 - 튜플 (우선순위, 값)")
print("  (튜플 첫 번째 값이 작을수록 우선순위 높음)")
print("=" * 60)

pq2 = PriorityQueue()

print("\n▶ Enqueue 테스트")
pq2.enqueue((3, "일반 업무"))
pq2.enqueue((1, "긴급 업무"))
pq2.enqueue((5, "낮은 업무"))
pq2.enqueue((2, "중요 업무"))
pq2.enqueue((4, "보통 업무"))
pq2.display()

print("\n▶ Peek 테스트")
pq2.peek()                                         # (1, 긴급 업무)

print("\n▶ Dequeue 테스트 (우선순위 순으로 나옴)")
pq2.dequeue()                                      # (1, 긴급 업무)
pq2.dequeue()                                      # (2, 중요 업무)
pq2.dequeue()                                      # (3, 일반 업무)
pq2.display()

print("\n▶ Size 테스트")
pq2.size()                                         # 2

print("\n▶ Clear 테스트")
pq2.clear()
pq2.display()
print(f"  isEmpty : {pq2.is_empty()}")             # True

print("\n▶ isFull 테스트 (max_size=3)")
small = PriorityQueue(max_size=3)
small.enqueue((1, "A"))
small.enqueue((2, "B"))
small.enqueue((3, "C"))
print(f"  isFull : {small.is_full()}")             # True
try:
    small.enqueue((4, "D"))
except OverflowError as e:
    print(f"  [Enqueue 오류] → {e}")
