import ctypes # C 스타일 배열을 사용하기 위한 모듈, 배열임을 보여주기 위함

def is_valid_pos(data, pos, size):
    """유효한 인덱스인지 검사"""
    return 0 <= pos < size

def sort_items(data, size, key=None, reverse=False):
    """정렬 후 리스트 반환"""
    return sorted([data[i] for i in range(size)], key=key, reverse=reverse)


#  ArrayList 클래스 (배열 기반)
class ArrayList:
    DEFAULT_MAX = 64

    def __init__(self, max_size=None):
        self.__max_size = max_size if max_size is not None else self.DEFAULT_MAX
        self.__size = 0
        self.__array = (self.__max_size * ctypes.py_object)()  # 고정 크기 C 배열

    def insert(self, pos, e):
        """pos 위치에 요소 e 삽입"""
        if self.is_full():
            raise OverflowError("리스트가 가득 찼습니다")
        if not is_valid_pos(self.__array, pos, self.__size) and pos != self.__size:
            raise IndexError(f"유효하지 않은 위치: {pos}")
        for i in range(self.__size, pos, -1):
            self.__array[i] = self.__array[i - 1]
        self.__array[pos] = e
        self.__size += 1

    def delete(self, pos):
        """pos 위치 요소 삭제 후 반환"""
        if not is_valid_pos(self.__array, pos, self.__size):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        removed = self.__array[pos]
        for i in range(pos, self.__size - 1):
            self.__array[i] = self.__array[i + 1]
        self.__size -= 1
        return removed

    def append(self, e):
        """맨 뒤에 요소 추가"""
        if self.is_full():
            raise OverflowError("리스트가 가득 찼습니다")
        self.__array[self.__size] = e
        self.__size += 1

    def is_empty(self):
        """비어 있으면 True"""
        return self.__size == 0

    def is_full(self):
        """가득 찼으면 True"""
        return self.__size >= self.__max_size

    def get_entry(self, pos):
        if not is_valid_pos(self.__array, pos, self.__size):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        return self.__array[pos]

    def size(self):
        return self.__size

    def clear(self):
        self.__size = 0
        self.__array = (self.__max_size * ctypes.py_object)()

    def find(self, item):
        for i in range(self.__size):
            if self.__array[i] == item:
                return i
        return -1

    def replace(self, pos, item):
        if not is_valid_pos(self.__array, pos, self.__size):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        self.__array[pos] = item

    def sort(self, key=None, reverse=False):
        sorted_data = sort_items(self.__array, self.__size, key=key, reverse=reverse)
        for i, v in enumerate(sorted_data):
            self.__array[i] = v

    def to_list(self):
        return [self.__array[i] for i in range(self.__size)]

    def display(self, label="ArrayList"):
        print(f"[{label}] → {self.to_list()}")

    def display_with_lineno(self):
        for i in range(self.__size):
            print(f"  {i+1}: {self.__array[i]}")

    def __len__(self):
        return self.__size

    def __str__(self):
        return str(self.to_list())


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # 다음 노드를 가리키는 포인터


#  LinkedList 클래스 (연결된 구조 기반)
class LinkedList:
    def __init__(self, max_size=None):
        self.__head = None       # 첫 번째 노드
        self.__size = 0
        self.__max_size = max_size

    def __get_node(self, pos):
        """pos 위치의 노드 반환 (내부용)"""
        node = self.__head
        for _ in range(pos):
            node = node.next
        return node

    def insert(self, pos, e):
        """pos 위치에 요소 e 삽입"""
        if self.is_full():
            raise OverflowError("리스트가 가득 찼습니다")
        if not (0 <= pos <= self.__size):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        new_node = Node(e)
        if pos == 0:
            new_node.next = self.__head
            self.__head = new_node
        else:
            prev = self.__get_node(pos - 1)
            new_node.next = prev.next
            prev.next = new_node
        self.__size += 1

    def delete(self, pos):
        """pos 위치 요소 삭제 후 반환"""
        if not (0 <= pos < self.__size):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        if pos == 0:
            removed = self.__head.data
            self.__head = self.__head.next
        else:
            prev = self.__get_node(pos - 1)
            removed = prev.next.data
            prev.next = prev.next.next
        self.__size -= 1
        return removed

    def append(self, e):
        """맨 뒤에 요소 추가"""
        if self.is_full():
            raise OverflowError("리스트가 가득 찼습니다")
        new_node = Node(e)
        if self.__head is None:
            self.__head = new_node
        else:
            self.__get_node(self.__size - 1).next = new_node
        self.__size += 1

    def is_empty(self):
        """비어 있으면 True"""
        return self.__size == 0

    def is_full(self):
        """가득 찼으면 True"""
        if self.__max_size is None:
            return False
        return self.__size >= self.__max_size

    def get_entry(self, pos):
        if not (0 <= pos < self.__size):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        return self.__get_node(pos).data

    def size(self):
        return self.__size

    def clear(self):
        self.__head = None
        self.__size = 0

    def find(self, item):
        node = self.__head
        for i in range(self.__size):
            if node.data == item:
                return i
            node = node.next
        return -1

    def replace(self, pos, item):
        if not (0 <= pos < self.__size):
            raise IndexError(f"유효하지 않은 위치: {pos}")
        self.__get_node(pos).data = item

    def sort(self, key=None, reverse=False):
        sorted_data = sorted(self.to_list(), key=key, reverse=reverse)
        node = self.__head
        for v in sorted_data:
            node.data = v
            node = node.next

    def to_list(self):
        result = []
        node = self.__head
        while node:
            result.append(node.data)
            node = node.next
        return result

    def display(self, label="LinkedList"):
        print(f"[{label}] → {self.to_list()}")

    def display_with_lineno(self):
        node = self.__head
        i = 1
        while node:
            print(f"  {i}: {node.data}")
            node = node.next
            i += 1

    def __len__(self):
        return self.__size

    def __str__(self):
        return str(self.to_list())



print("       ArrayList / LinkedList ADT 테스트")
print("=" * 50)

al = ArrayList(max_size=10)
al.append(10); al.append(30); al.append(50)
al.display("AL append")                 # [10, 30, 50]

ll = LinkedList(max_size=10)
ll.append(10); ll.append(30); ll.append(50)
ll.display("LL append")                 # [10, 30, 50]

al.insert(1, 20);  al.display("AL insert(1,20)")   # [10, 20, 30, 50]
ll.insert(1, 20);  ll.display("LL insert(1,20)")   # [10, 20, 30, 50]

al.delete(2);      al.display("AL delete(2)")       # [10, 20, 50]
ll.delete(2);      ll.display("LL delete(2)")       # [10, 20, 50]

print(f"  AL isEmpty/isFull/size : {al.is_empty()} / {al.is_full()} / {al.size()}")
print(f"  LL isEmpty/isFull/size : {ll.is_empty()} / {ll.is_full()} / {ll.size()}")

print(f"  AL getEntry(1) : {al.get_entry(1)}")         # 20
print(f"  LL getEntry(1) : {ll.get_entry(1)}")         # 20

print(f"  AL find(50)    : {al.find(50)}")                # 2
print(f"  LL find(50)    : {ll.find(50)}")                # 2

al.replace(0, 99); al.display("AL replace(0,99)")  # [99, 20, 50]
ll.replace(0, 99); ll.display("LL replace(0,99)")  # [99, 20, 50]

al.sort();         al.display("AL sort")          # [20, 50, 99]
ll.sort();         ll.display("LL sort")          # [20, 50, 99]

al.clear();        al.display("AL clear")         # []
ll.clear();        ll.display("LL clear")         # []