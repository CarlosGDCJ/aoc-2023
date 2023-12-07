import requests
import os
import sys
from dotenv import load_dotenv


def main():

    # Create folder for day
    day = int(sys.argv[1])
    assert 0 < day < 26, f"Invalid day {day}"
    day = str(day)

    day_dir = os.path.join(__file__.rsplit(sep=os.sep, maxsplit=1)[0], f"day{day}")
    if not os.path.isdir(day_dir):
        os.mkdir(day_dir)

    # Download input
    load_dotenv()

    cookies = {"session": os.getenv("AOC_SESSION")}

    base_url = "https://adventofcode.com/2023/day"

    res = requests.get(url=f"{base_url}/{day}/input", cookies=cookies)

    if not res.ok:
        raise RuntimeError(
            f"Request failed, code: {res.status_code}, message: {res.content}"
        )

    with open(os.path.join(day_dir, "input.txt"), "w") as f:
        f.write(res.text)


if __name__ == "__main__":
    main()
