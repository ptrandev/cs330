import random

def Chocolate(arr):
    N = len(arr) - 1  # Length of array
    C = {}  # memoization table

    def OPT(start, end):
        # Base case; no elements left
        if end < start:
            return 0

        # recursive case
        if (start, end) not in C:
            # determine if it's the opponent's turn
            is_opponent_turn = (end - start + 1) % 2 == N % 2

            # opponent's turn, choose worst move for me (best move for opponent)
            if is_opponent_turn:
                they_chose_left = OPT(start + 1, end)
                they_chose_right = OPT(start, end - 1)

                C[(start, end)] = min(they_chose_left, they_chose_right)
            # my turn, choose best move for me
            else:
                we_chose_left = OPT(start + 1, end) + arr[start]
                we_chose_right = OPT(start, end - 1) + arr[end]

                C[(start, end)] = max(we_chose_left, we_chose_right)

        return C[(start, end)]  # Return result from memoization table

    def FindSolution(start, end):

        S = [] # solution set of moves
        player_one_turn = True

        while start >= 0 and end >= start:
            choose_left = C[(start+1, end)] if (start+1, end) in C else 0
            choose_right = C[(start,end-1)] if (start,end-1) in C else 0

            if player_one_turn:
                choose_left = choose_left + arr[start]
                choose_right = choose_right + arr[end]

                if choose_left > choose_right:
                    S.append(start)
                    start += 1
                else:
                    S.append(end)
                    end -= 1
            else:
                if choose_left <= choose_right:
                    start += 1
                else:
                    end -= 1

            player_one_turn = not player_one_turn

        return S # return the set of moves we should make

    total_chocolate = OPT(0, N) # amount of chocolate we can expect to win
    moves = FindSolution(0, N) # the list of moves we should take

    return total_chocolate, moves


print(Chocolate([20, 15, 5, 8]))  # 28
# opt moves: p1 = [20, 8], p2 = [15, 5]
# opt moves index = [0,3]

# print(Chocolate([20, 40, 5, 8]))  # 48

# print(Chocolate([8, 1, 5, 6, 100, 2, 3]))  # 17
# print(Chocolate([8, 1, 5, 100, 6, 2, 3]))  # 21
# print(Chocolate([1, 2, 11, 6, 7, 10, 3]))  # 19

def test(num = 100, size=10):
    for i in range(num):
        arr = [random.randint(1,size) for i in range(random.randint(1,size))]
        try:
            Chocolate(arr)
        except Exception as err:
            print(f"ERROR: {err}")
            print(arr)
            quit()

# test(100, 100)
