import ctypes


# ──────────────────────────────────────────────
#  헬퍼 함수
# ──────────────────────────────────────────────

def union_sets(a, b):
    """합집합 반환"""
    return list(set(a) | set(b))

def intersect_sets(a, b):
    """교집합 반환"""
    return list(set(a) & set(b))

def difference_sets(a, b):
    """차집합 반환"""
    return list(set(a) - set(b))

def equals_sets(a, b):
    return set(a) == set(b)

def display_set(label, data):
    print(f"  [{label}] → {sorted(data)}")


# ──────────────────────────────────────────────
#  ArraySet 클래스 (배열 기반)
# ──────────────────────────────────────────────

class ArraySet:
    DEFAULT_MAX = 64

    def __init__(self, max_size=None):
        self.__max_size = max_size if max_size is not None else self.DEFAULT_MAX
        self.__size = 0
        self.__array = (self.__max_size * ctypes.py_object)()  # 고정 크기 C 배열

    def contain(self, e):
        for i in range(self.__size):
            if self.__array[i] == e:
                return True
        return False

    def insert(self, e):
        if self.is_full():
            raise OverflowError("집합이 가득 찼습니다")
        if self.contain(e):
            print(f"  [중복] '{e}'는 이미 존재합니다 → 삽입 무시")
            return
        self.__array[self.__size] = e
        self.__size += 1

    def delete(self, e):
        for i in range(self.__size):
            if self.__array[i] == e:
                # 삭제 후 뒤 요소들을 앞으로 이동
                for j in range(i, self.__size - 1):
                    self.__array[j] = self.__array[j + 1]
                self.__size -= 1
                return e
        raise ValueError(f"'{e}'는 집합에 없습니다")

    def is_full(self):
        return self.__size >= self.__max_size

    def is_empty(self):
        return self.__size == 0

    def size(self):
        return self.__size

    def to_list(self):
        return [self.__array[i] for i in range(self.__size)]

    def union(self, other):
        result = ArraySet()
        for v in union_sets(self.to_list(), other.to_list()):
            result.insert(v)
        return result

    def intersect(self, other):
        result = ArraySet()
        for v in intersect_sets(self.to_list(), other.to_list()):
            result.insert(v)
        return result

    def difference(self, other):
        result = ArraySet()
        for v in difference_sets(self.to_list(), other.to_list()):
            result.insert(v)
        return result

    def equals(self, other):
        return equals_sets(self.to_list(), other.to_list())

    def display(self, label="ArraySet"):
        display_set(label, self.to_list())


# ──────────────────────────────────────────────
#  Node 클래스
# ──────────────────────────────────────────────

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None  # 다음 노드를 가리키는 포인터


# ──────────────────────────────────────────────
#  LinkedSet 클래스 (연결 기반)
# ──────────────────────────────────────────────

class LinkedSet:
    def __init__(self, max_size=None):
        self.__head = None
        self.__size = 0
        self.__max_size = max_size

    def contain(self, e):
        node = self.__head
        while node:
            if node.data == e:
                return True
            node = node.next
        return False

    def insert(self, e):
        if self.is_full():
            raise OverflowError("집합이 가득 찼습니다")
        if self.contain(e):
            print(f"  [중복] '{e}'는 이미 존재합니다 → 삽입 무시")
            return
        new_node = Node(e)
        new_node.next = self.__head
        self.__head = new_node
        self.__size += 1

    def delete(self, e):
        prev, node = None, self.__head
        while node:
            if node.data == e:
                if prev:
                    prev.next = node.next
                else:
                    self.__head = node.next
                self.__size -= 1
                return e
            prev, node = node, node.next
        raise ValueError(f"'{e}'는 집합에 없습니다")

    def is_full(self):
        if self.__max_size is None:
            return False
        return self.__size >= self.__max_size

    def is_empty(self):
        return self.__size == 0

    def size(self):
        return self.__size

    def to_list(self):
        result, node = [], self.__head
        while node:
            result.append(node.data)
            node = node.next
        return result

    def union(self, other):
        result = LinkedSet()
        for v in union_sets(self.to_list(), other.to_list()):
            result.insert(v)
        return result

    def intersect(self, other):
        result = LinkedSet()
        for v in intersect_sets(self.to_list(), other.to_list()):
            result.insert(v)
        return result

    def difference(self, other):
        result = LinkedSet()
        for v in difference_sets(self.to_list(), other.to_list()):
            result.insert(v)
        return result

    def equals(self, other):
        return equals_sets(self.to_list(), other.to_list())

    def display(self, label="LinkedSet"):
        display_set(label, self.to_list())


# ──────────────────────────────────────────────
#  테스트
# ──────────────────────────────────────────────

print("=" * 50)
print("     ArraySet / LinkedSet ADT 테스트")
print("=" * 50)

as1 = ArraySet();  ls1 = LinkedSet()
for v in [1, 2, 3, 4, 5]:
    as1.insert(v); ls1.insert(v)
as1.display("AS s1");  ls1.display("LS s1")         # [1,2,3,4,5]

as1.insert(3);  ls1.insert(3)                       # 중복 → 무시

as2 = ArraySet();  ls2 = LinkedSet()
for v in [4, 5, 6, 7, 8]:
    as2.insert(v); ls2.insert(v)
as2.display("AS s2");  ls2.display("LS s2")         # [4,5,6,7,8]

print(f"\n  AS contain(3/9) : {as1.contain(3)} / {as1.contain(9)}")
print(f"  LS contain(3/9) : {ls1.contain(3)} / {ls1.contain(9)}")

print(f"\n  AS del(2): {as1.delete(2)}")
print(f"  LS del(2): {ls1.delete(2)}")
as1.display("AS s1 del(2)");  ls1.display("LS s1 del(2)")

print(f"\n  AS empty/size : {as1.is_empty()} / {as1.size()}")
print(f"  LS empty/size : {ls1.is_empty()} / {ls1.size()}")

as1.union(as2).display("AS s1∪s2");        ls1.union(ls2).display("LS s1∪s2")
as1.intersect(as2).display("AS s1∩s2");    ls1.intersect(ls2).display("LS s1∩s2")
as1.difference(as2).display("AS s1-s2");   ls1.difference(ls2).display("LS s1-s2")

as3 = ArraySet();  ls3 = LinkedSet()
for v in [1, 3, 4, 5]:
    as3.insert(v); ls3.insert(v)
print(f"\n  AS s1==s3 / s1==s2 : {as1.equals(as3)} / {as1.equals(as2)}")
print(f"  LS s1==s3 / s1==s2 : {ls1.equals(ls3)} / {ls1.equals(ls2)}")
