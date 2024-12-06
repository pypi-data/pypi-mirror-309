from unittest.mock import patch, mock_open

import pytest

from collection.unique_char_count import get_unique_character_count, _cached_count_unique_characters, main


# Testing the main functionality
@pytest.mark.parametrize("input_text, expected", [
    ("", 0),  # Empty string
    ("abcdefg", 7),  # All characters are unique
    ("aaaaa", 0),  # All characters are the same
    ("aabbcde", 3),  # Mixed unique and repeated
    ("aA", 2),  # Case sensitivity
    ("a!@#$%^a", 6),  # Special characters
    ("a bca", 3),  # Spaces
])
def test_get_unique_character_count( input_text, expected ):
    assert get_unique_character_count(input_text) == expected \
 \
        # Testing edge cases


@pytest.mark.parametrize("invalid_input", [
    123,  # Int
    None,  # None
    ["a", "b", "c"],  # List
    {"key": "value"},  # Dict
    12.34,  # Float
])
def test_invalid_input( invalid_input ):
    with pytest.raises(ValueError, match="Expected a string"):
        get_unique_character_count(invalid_input)


# Testing cache functionality
@pytest.mark.parametrize("input_text, expected", [
    ("aabbcc", 0),
    ("abcdef", 6),
    ("aabbcde", 3),
])
def test_cache_functionality( input_text, expected ):
    # Clear cache before testing
    _cached_count_unique_characters.cache_clear()

    # First call (should compute result)
    first_result = get_unique_character_count(input_text)
    assert first_result == expected

    # Second call (should use cache)
    second_result = get_unique_character_count(input_text)
    assert second_result == first_result

    # Verify cache stats
    cache_info = _cached_count_unique_characters.cache_info()
    assert cache_info.hits == 1  # Only one cache hit for the second call
    assert cache_info.misses == 1  # One cache miss for the first call


@pytest.mark.parametrize("args, mock_file_content, expected_output", [
    (["--string", "abcdefg"], None, "Number of unique characters: 7"),
    (["--file", "mock_file.txt"], "aabbcde", "Number of unique characters: 3"),
    (["--string", "aabbcde", "--file", "mock_file.txt"], "abcdef", "Number of unique characters: 6"),
    (["--file", "non_existent_file.txt"], None, "Error: File 'non_existent_file.txt' not found."),
    ([], None, "Error: No input provided. Use --string or --file."),
    (["--file", "mock_file.txt"], "", "Number of unique characters: 0"),
    (["--string", "a" * 10000], None, "Number of unique characters: 0"),
    (["--file", "mock_file.txt"], "a" * 10000, "Number of unique characters: 0"),

])
def test_cli(args, mock_file_content, expected_output, capsys):
    """
    Test the CLI functionality by invoking the main() function directly.
    """
    with patch("builtins.open", mock_open(read_data=mock_file_content)) if mock_file_content is not None else patch("builtins.open") as mock_file, \
         patch("os.path.isfile", return_value=mock_file_content is not None):

        # Mock sys.argv to simulate CLI arguments
        with patch("sys.argv", ["unique_char_count.py"] + args):
            main()  # Directly call the main function

        # Capture the printed output
        captured = capsys.readouterr()
        assert expected_output in captured.out

        # Verify file operations if a file was mocked
        if mock_file_content is not None:
            mock_file.assert_called_once_with("mock_file.txt", "r", encoding="utf-8")


@pytest.mark.parametrize("args, expected_error", [
    (["--unknown", "value"], "unrecognized arguments: --unknown"),
    (["--string", "abcdef", "--unknown", "value"], "unrecognized arguments: --unknown"),
])
def test_cli_invalid_arguments(args, expected_error, capsys):
    """
    Test the CLI functionality with invalid arguments.
    """
    # Mock sys.argv to simulate CLI arguments
    with patch("sys.argv", ["unique_char_count.py"] + args):
        with pytest.raises(SystemExit) as excinfo:
            main()  # Directly call the main function

        # Capture the printed output
        captured = capsys.readouterr()
        # Check if the error message contains the expected error text
        assert expected_error in captured.err
        assert excinfo.value.code == 2  # Ensure the exit code is for argument errors

