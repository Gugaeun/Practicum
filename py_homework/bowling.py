import random as rand

def bowling_random_game():
    result = []

    for frame in range(1, 11):

        # 1~9 프레임
        if frame < 10:
            if rand.random() < 0.3:
                result.append(10)
            else:
                first = rand.randint(0, 9)
                second = rand.randint(0, 10 - first)

                result.append(first)
                result.append(second)

        # 10 프레임
        else:
            first = rand.randint(0, 10)
            result.append(first)

            if first == 10:
                second = rand.randint(0, 10)
                result.append(second)

                if second == 10:
                    third = rand.randint(0, 10)
                else:
                    third = rand.randint(0, 10 - second)

                result.append(third)

            else:
                second = rand.randint(0, 10 - first)
                result.append(second)

                if first + second == 10:
                    third = rand.randint(0, 10)
                    result.append(third)

    return result


# 점수 계산
def score_bowling_random_game(result):
    score = 0
    i = 0
    frame_scores = []

    for frame in range(10):
        # 스트라이크
        if result[i] == 10:
            score = score + 10 + result[i+1] + result[i+2]
            frame_scores.append(score)
            i = i + 1

        # 스페어
        elif result[i] + result[i+1] == 10:
            score += 10 + result[i+2]
            frame_scores.append(score)
            i = i + 2

        # 오픈
        else:
            score += result[i] + result[i+1]
            frame_scores.append(score)
            i = i + 2

    return frame_scores

# 투구의 결과를 문자열로 만들어주는 함수
def score_Cal(Now_pin, Next_pin=None) :
    if Now_pin == 10 :
        return "X"
    elif Next_pin is not None and Now_pin + Next_pin == 10 :
        return "/"
    elif Now_pin == 0 :
        return "-"
    else :
        return str(Now_pin)


# 점수 출력
def print_score(result, frame_scores) :
    index = 0

    print("\n === 프레임별 결과 === \n ")
    for frame in range(10) :
        print(f"\n{frame+1} 프레임")

        if frame == 9 :
            last_frame_result = result[index :]
            output = []
            # enumerate 로  last_frame_result 내 인덱스와 값을 쌍으로 생성
            for inx, b in enumerate(last_frame_result) :
                if index > 0 :
                    Np = last_frame_result[inx-1]
                else :
                    Np = None
                output.append(score_Cal(b, Np))
                    
            while len(output) < 3 :
                output.append(" ")
            
            print(f"[ {output[0]}, {output[1]}, {output[2]} ]")
            print(f"점수 : {frame_scores[frame]}")
            break

        if result[index] == 10:
            print("[ X,  ]")
            print(f"점수 : {frame_scores[frame]}")
            index = index + 1
        else :
            first = result[index]
            second = result[index +1]

            first_str = score_Cal(first)
            second_str = score_Cal(second, first)

            print(f"[ {first_str}, {second_str}]")
            print(f"점수 : {frame_scores[frame]}")
            index = index + 2

    print(f"\n최종 점수 : {frame_scores[-1]}")
        
# 화면 출력
final_game = bowling_random_game()
scores = score_bowling_random_game(final_game)
print_score(final_game, scores)
            

    


