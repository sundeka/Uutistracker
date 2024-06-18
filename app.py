import argparse
from colorama import Back
from src.uutistracker import Uutistracker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    if args.debug:
        c = Back.RED   
        print(c + "DEBUG MODE")
        c = Back.RESET
        tracker = Uutistracker(debug=True)
    else:
        tracker = Uutistracker()
    tracker.start()