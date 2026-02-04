import requests

URL = "https://gameofcrowns.sanish.me/api/goc"
CHALLENGE_ID = 222

def fetch_board(challenge_id: int):
    params = {"challengeId": challenge_id}

    headers = {
        "accept": "*/*",
        "referer": f"https://gameofcrowns.sanish.me/challenges/{challenge_id}",
        "user-agent": "Mozilla/5.0",
    }

    resp = requests.get(URL, params=params, headers=headers, timeout=10)
    resp.raise_for_status()
    return resp.json()["board"]

def map_board_to_regions(raw_board):
    """
    Maps:
      0 -> C1
      1 -> C2
      2 -> C3
      ...
    """
    return [
        [f"C{cell + 1}" for cell in row]
        for row in raw_board
    ]

def gameofcrowns_get_board(challenge_id: int = CHALLENGE_ID, rotate: bool = False):
    raw_board = fetch_board(challenge_id)
    if rotate:
            raw_board = rotate_board(raw_board)
    return map_board_to_regions(raw_board)

def rotate_board(board):
    """Rotates the board 90 degrees"""
    return [list(reversed(col)) for col in zip(*board)]

if __name__ == "__main__":
    raw_board = fetch_board(CHALLENGE_ID)
    board = map_board_to_regions(raw_board)

    for row in board:
        print(row)
