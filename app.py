import argparse
from src.uutistracker import Uutistracker

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--debug', action='store_true', help="Enable debug mode")
    args = parser.parse_args()
    if args.debug:
        tracker = Uutistracker(debug=True)
    else:
        tracker = Uutistracker()
    tracker.start()