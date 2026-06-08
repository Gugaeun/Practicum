import ctypes

def is_full_check(size, max_size):
    if max_size is None:
        return False
    return size >= max_size

def is_empty_check(size):
    return size == 0

def display_stack(items):
    """items: 아래→위 순서의 리스트"""
    if not items:
        print("  [ 비어있는 스택 ]")
        return
    print("  ┌─────────┐")
    for item in reversed(items):
        print(f"  │  {str(item):<7}│  ← TOP" if item == items[-1] else f"  │  {str(item):<7}│")
    print("  └─────────┘")


#  ArrayStack 클래스 (배열 기반)
class ArrayStack:
    DEFAULT_MAX = 64

    def __init__(self, max_size=None):
        self.__max_size = max_size if max_size is not None else self.DEFAULT_MAX
        self.__size = 0
        self.__array = (self.__max_size * ctypes.py_object)()  # 고정 크기 C 배열

    def push(self, e):
        if self.is_full():
            raise OverflowError("스택이 가득 찼습니다")
        self.__array[self.__size] = e
        self.__size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("스택이 비어 있습니다")
        self.__size -= 1
        return self.__array[self.__size]

    def peek(self):
        if self.is_empty():
            raise IndexError("스택이 비어 있습니다")
        return self.__array[self.__size - 1]

    def is_full(self):
        return is_full_check(self.__size, self.__max_size)

    def is_empty(self):
        return is_empty_check(self.__size)

    def size(self):
        return self.__size

    def clear(self):
        self.__size = 0
        self.__array = (self.__max_size * ctypes.py_object)()

    def to_list(self):
        return [self.__array[i] for i in range(self.__size)]

    def display(self):
        display_stack(self.to_list())


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # 아래 노드를 가리키는 포인터


#  LinkedStack 클래스 (연결된 구조 기반)
class LinkedStack:
    def __init__(self, max_size=None):
        self.__top = None   # TOP 노드
        self.__size = 0
        self.__max_size = max_size

    def push(self, e):
        if self.is_full():
            raise OverflowError("스택이 가득 찼습니다")
        node = Node(e)
        node.next = self.__top  # 새 노드가 기존 TOP을 가리킴
        self.__top = node       # 새 노드가 TOP이 됨
        self.__size += 1

    def pop(self):
        if self.is_empty():
            raise IndexError("스택이 비어 있습니다")
        data = self.__top.data
        self.__top = self.__top.next  # TOP을 아래 노드로 이동
        self.__size -= 1
        return data

    def peek(self):
        if self.is_empty():
            raise IndexError("스택이 비어 있습니다")
        return self.__top.data

    def is_full(self):
        return is_full_check(self.__size, self.__max_size)

    def is_empty(self):
        return is_empty_check(self.__size)

    def size(self):
        return self.__size

    def clear(self):
        self.__top = None
        self.__size = 0

    def to_list(self):
        result, node = [], self.__top
        while node:
            result.append(node.data)
            node = node.next
        return list(reversed(result))  # 아래→위 순서로 반환

    def display(self):
        display_stack(self.to_list())


print("=" * 50)
print("    ArrayStack / LinkedStack ADT 테스트")
print("=" * 50)

as_ = ArrayStack(max_size=5)
ls_ = LinkedStack(max_size=5)

print("\n▶ push(10/20/30/40)")
for v in [10, 20, 30, 40]:
    as_.push(v); ls_.push(v)
as_.display(); ls_.display()

print("\n▶ peek")
print(f"  AS peek : {as_.peek()}")
print(f"  LS peek : {ls_.peek()}")

print("\n▶ pop x2")
print(f"  AS pop : {as_.pop()} / {as_.pop()}")
print(f"  LS pop : {ls_.pop()} / {ls_.pop()}")
as_.display(); ls_.display()

print("\n▶ isEmpty / isFull / size")
print(f"  AS : {as_.is_empty()} / {as_.is_full()} / {as_.size()}")
print(f"  LS : {ls_.is_empty()} / {ls_.is_full()} / {ls_.size()}")

print("\n▶ push(30/40/50) → isFull")
for v in [30, 40, 50]:
    as_.push(v); ls_.push(v)
print(f"  AS isFull : {as_.is_full()}")
print(f"  LS isFull : {ls_.is_full()}")
as_.display(); ls_.display()

print("\n▶ clear")
as_.clear(); ls_.clear()
as_.display(); ls_.display()
print(f"  AS isEmpty : {as_.is_empty()}")
print(f"  LS isEmpty : {ls_.is_empty()}")