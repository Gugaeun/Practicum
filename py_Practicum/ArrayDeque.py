# 선형 큐
class Deque:

    def __init__(self):
        self.__data = []

    # 덱이 가득 차 있는지 검사 (리스트 기반이므로 항상 False)
    def IsFull(self):
        return False

    # 덱이 비어있는지 검사
    def isEmpty(self):
        return len(self.__data) == 0

    # 맨 앞(전단)에 새로운 요소 e를 추가
    def AddFront(self, e):
        self.__data.insert(0, e)

    # 맨 앞(전단)의 요소를 꺼내서 반환
    def DeleteFront(self):
        if self.isEmpty():
            raise IndexError("덱이 비어 있습니다.")
        return self.__data.pop(0)

    # 맨 앞(전단)의 요소를 꺼내지 않고 반환
    def getFront(self):
        if self.isEmpty():
            raise IndexError("덱이 비어 있습니다.")
        return self.__data[0]

    # 맨 뒤(후단)에 새로운 요소 e를 추가
    def AddRear(self, e):
        self.__data.append(e)

    # 맨 뒤(후단)의 요소를 꺼내서 반환
    def DeleteRear(self):
        if self.isEmpty():
            raise IndexError("덱이 비어 있습니다.")
        return self.__data.pop()

    # 맨 뒤(후단)의 요소를 꺼내지 않고 반환
    def getRear(self):
        if self.isEmpty():
            raise IndexError("덱이 비어 있습니다.")
        return self.__data[-1]

    # 덱의 모든 항목들의 개수를 반환
    def Size(self):
        return len(self.__data)

    # 덱을 공백 상태로 만든다
    def Clear(self):
        self.__data = []

    def __str__(self):
        return f"전단 {self.__data} 후단"

if __name__ == "__main__":
    dq = Deque()

    print("=== 후단에 요소 추가 (AddRear) ===")
    dq.AddRear(10)
    dq.AddRear(20)
    dq.AddRear(30)
    print(dq)                         # 전단 [10, 20, 30] 후단

    print("\n=== 전단에 요소 추가 (AddFront) ===")
    dq.AddFront(5)
    print(dq)                         # 전단 [5, 10, 20, 30] 후단

    print(f"\n크기: {dq.Size()}")       # 4
    print(f"전단 확인: {dq.getFront()}")  # 5
    print(f"후단 확인: {dq.getRear()}")  # 30

    print("\n=== 전단 삭제 (DeleteFront) ===")
    print(f"꺼낸 값: {dq.DeleteFront()}")  # 5
    print(dq)                              # 전단 [10, 20, 30] 후단

    print("\n=== 후단 삭제 (DeleteRear) ===")
    print(f"꺼낸 값: {dq.DeleteRear()}")   # 30
    print(dq)                              # 전단 [10, 20] 후단

    print("\n=== 덱 비우기 (Clear) ===")
    dq.Clear()
    print(f"비어있나요? {dq.isEmpty()}")   # True