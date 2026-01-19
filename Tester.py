import GameofCrownsBoardFetcher
import CoreSolver


def test():
    failed_challenges = []
    failed_challenges_rotated = []
    for challenge_id in range(1, 474):
        print(challenge_id, end=",")
        board = GameofCrownsBoardFetcher.gameofcrowns_get_board(challenge_id, rotate=False)
        solved = CoreSolver.solve(board, printSteps=False)
        if not solved:
            print(f"Failed to solve Challenge ID: {challenge_id}")
            failed_challenges.append(challenge_id)
            print("\n" + "="*40 + "\n")
        board = GameofCrownsBoardFetcher.gameofcrowns_get_board(challenge_id, rotate=True)
        solved = CoreSolver.solve(board, printSteps=False)
        if not solved:
            print(f"Failed to solve Challenge ID (Rotated): {challenge_id}")
            failed_challenges_rotated.append(challenge_id)
            print("\n" + "="*40 + "\n")
    print(len(failed_challenges), " Failed Challenges (Normal):", failed_challenges)
    print(len(failed_challenges_rotated), " Failed Challenges (Rotated):", failed_challenges_rotated)


if __name__ == "__main__":
    test()