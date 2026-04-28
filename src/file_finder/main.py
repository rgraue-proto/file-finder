import argparse
import sys
from loader import load_folder
from finder import find_files

def main():
    parser = argparse.ArgumentParser(description="File Finder.")
    
    parser.add_argument(
        '-f', 
        '--find',
        type=str,
        help="Description of what file to find."
    )
    parser.add_argument(
        '-l',
        '--load',
        type=str,
        help='Path to load into file finder system.'
    )
    parser.add_argument(
        '-v',
        '--verbose',
        action='store_true'
    )
    parser.add_argument(
        '-c',
        '--confidence',
        type=float,
        help='confidence threshold when finding files'
    )

    args = parser.parse_args()
    if args.load:
        load_folder(args.load, args.verbose)

    if args.find:
        find_files(args.find, args.verbose, args.confidence)


if __name__ == "__main__":
    main()
