# main.py
from smokey import SmokeyController


def main():
    smokey = SmokeyController("config/env1.json")
    smokey.run()


if __name__ == "__main__":
    print("Started main")
    main()
    # execute only if run as a script

