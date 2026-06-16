# 선형 큐
# 선형 큐

def is_full_check(data, max_size):
    """가득 찼는지 검사"""
    if max_size is None:
        return False
    return len(data) >= max_size

def is_empty_check(data):
    """비어 있는지 검사"""
    return len(data) == 0

def display_queue(data):
    """큐 내용을 시각적으로 출력"""
    if not data:
        print("  [ 비어있는 큐 ]")
        return
    print("  앞(Front)                    뒤(Rear)")
    print("  ┌─────" + "──────" * (len(data) - 1) + "─────┐")
    print("  │ ", end="")
    for i, item in enumerate(data):
        if i < len(data) - 1:
            print(f"{str(item):<5}│ ", end="")
        else:
            print(f"{str(item):<5}", end="")
    print(" │")
    print("  └─────" + "──────" * (len(data) - 1) + "─────┘")
    print("    ↑                              ↑")
    print(f"  dequeue                       enqueue")


# ArrayQueue 클래스

class ArrayQueue:
    def __init__(self, max_size=None):
        self.__data = []
        self.__max_size = max_size

    # Enqueue: 요소 e를 큐의 맨 뒤에 추가
    def enqueue(self, e):
        if self.is_full():
            raise OverflowError("큐가 가득 찼습니다")
        self.__data.append(e)
        print(f"  enqueue({e}) 완료")

    # Dequeue: 큐의 맨 앞에 있는 요소를 꺼내 반환
    def dequeue(self):
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다")
        item = self.__data.pop(0)
        print(f"  dequeue() → {item}")
        return item

    # IsFull: 외부 함수 활용
    def is_full(self):
        return is_full_check(self.__data, self.__max_size)

    # isEmpty: 외부 함수 활용
    def is_empty(self):
        return is_empty_check(self.__data)

    # Peek: 맨 앞 요소를 삭제하지 않고 반환
    def peek(self):
        if self.is_empty():
            raise IndexError("큐가 비어 있습니다")
        return self.__data[0]

    # Size: 모든 항목들의 개수 반환
    def size(self):
        return len(self.__data)

    # Clear: 큐를 공백상태로 만든다
    def clear(self):
        self.__data.clear()
        print("  큐 초기화 완료")

    # Display: 외부 함수 활용해 출력
    def display(self):
        display_queue(self.__data)

    def __str__(self):
        return str(self.__data)



# 출력해보기
print("=" * 55)
print("           ArrayQueue ADT 테스트")
print("=" * 55)

queue = ArrayQueue(max_size=6)

# enqueue
print("\n▶ enqueue 테스트")
queue.enqueue(10)
queue.enqueue(20)
queue.enqueue(30)
queue.enqueue(40)
queue.display()

# peek
print("\n▶ peek 테스트")
print(f"  peek() → {queue.peek()}")              # 10 (삭제 안됨)
queue.display()                                   # 그대로

# dequeue
print("\n▶ dequeue 테스트")
queue.dequeue()                                   # 10
queue.dequeue()                                   # 20
queue.display()

# isEmpty / isFull / size
print("\n▶ 상태 확인")
print(f"  isEmpty : {queue.is_empty()}")          # False
print(f"  isFull  : {queue.is_full()}")           # False
print(f"  size    : {queue.size()}")              # 2

# isFull 테스트
print("\n▶ isFull 테스트 (max_size=6)")
queue.enqueue(50)
queue.enqueue(60)
queue.enqueue(70)
queue.enqueue(80)
print(f"  isFull  : {queue.is_full()}")           # True
queue.display()

# clear
print("\n▶ clear 테스트")
queue.clear()
queue.display()
print(f"  isEmpty : {queue.is_empty()}")          # True

# 예외 처리 테스트
print("\n▶ 예외 처리 테스트")
try:
    queue.dequeue()
except IndexError as e:
    print(f"  [dequeue 오류] → {e}")

try:
    queue.peek()
except IndexError as e:
    print(f"  [peek 오류] → {e}")

full_queue = ArrayQueue(max_size=2)
full_queue.enqueue(1)
full_queue.enqueue(2)
try:
    full_queue.enqueue(3)
except OverflowError as e:
    print(f"  [enqueue 오류] → {e}")