from collections import Counter
from functools import lru_cache
import argparse, os


def get_unique_character_count( input_text: str ) -> int:
    """
    Calculate the number of unique characters in the input text, caching the result.

    Args:
        input_text (str): The input string to analyze.

    Returns:
        int: The number of unique characters that appear only once.

    Raises:
        ValueError: If the input is not a string.
    """
    if not isinstance(input_text, str):
        raise ValueError(f"Expected a string, got {type(input_text).__name__}")
    return _cached_count_unique_characters(input_text)


@lru_cache(maxsize=None)
def _cached_count_unique_characters( input_text: str ) -> int:
    """
    Internal function to calculate unique characters, optimized with caching.

    Args:
        input_text (str): The input string to analyze.

    Returns:
        int: The number of unique characters that appear only once.
    """
    return count_unique_characters(input_text)


def count_unique_characters( input_text: str ) -> int:
    """
    Count the number of characters in the input string that appear only once.

    Args:
        input_text (str): The input string to analyze.

    Returns:
        int: The total count of characters that occur exactly once in the input string.
    """
    counter = Counter(input_text)
    unique_counts = map(lambda count: 1 if count == 1 else 0, counter.values())
    return sum(unique_counts)


def main():
    """
    Entry point for CLI to process input and count unique characters.
    """
    args = parse_arguments()

    # Determine input source
    text = get_input_text(args)
    if text is None:
        return

    # Process the text and output the result
    process_text(text)


def parse_arguments():
    """
    Parse CLI arguments.

    Returns:
        argparse.Namespace: Parsed arguments with `--string` and `--file`.
    """
    parser = argparse.ArgumentParser(description="Count unique characters in a string or file.")
    parser.add_argument("--string", type=str, help="Input string to process.")
    parser.add_argument("--file", type=str, help="Path to a text file to process.")
    return parser.parse_args()


def get_input_text(args):
    """
    Determine the input source (file or string) and return its content.

    Args:
        args (argparse.Namespace): Parsed CLI arguments.

    Returns:
        str: The input text to process, or None if there was an error.
    """
    if args.file:
        if not os.path.isfile(args.file):
            print(f"Error: File '{args.file}' not found.")
            return None
        try:
            with open(args.file, "r", encoding="utf-8") as file:
                content = file.read()
                if not isinstance(content, str):
                    raise ValueError(f"Expected a string, got {type(content).__name__}")
                return content
        except Exception as e:
            print(f"Error while reading the file: {e}")
            return None
    elif args.string:
        return args.string
    else:
        print("Error: No input provided. Use --string or --file.")
        return None



def process_text(text):
    """
    Process the input text to count unique characters and output the result.

    Args:
        text (str): The input text to process.
    """
    try:
        unique_count = get_unique_character_count(text)
        print(f"Number of unique characters: {unique_count}")
    except ValueError as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()
