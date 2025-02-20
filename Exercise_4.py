import logging
import string
from collections import Counter

lyrics = """\
… So, so you think you can tell heaven from hell?
Blue skies from pain?
Can you tell a green field from a cold steel rail?
A smile from a veil?
Do you think you can tell?
… Did they get you to trade your heroes for ghosts?
Hot ashes for trees?
Hot air for a cool breeze?
Cold comfort for change?
Did you exchange a walk on part in the war
For a lead role in a cage?
… How I wish, how I wish you were here
We're just two lost souls swimming in a fish bowl
Year after year
Running over the same old ground, what have we found?
The same old fears, wish you were here\
"""

def configure_logging():
    # Configure logging
    # = way to track events that happen when some software runs, recording data about execution of program
    # basicConfig - ensures all logs are directed to both the console and the execution_log.txt file
    # utf-8 = Unicode Transformation Format-8-bit, character encoding system, represents text in computers etc.
    logging.basicConfig(level=logging.INFO, format='%(message)s', handlers=[
        logging.FileHandler("execution_log.txt", mode='w', encoding='utf-8'),
        # writes log messages to file "execution_log.txt"
        logging.StreamHandler()  # writes log messages to console
    ])


def save_lyrics_to_file(filename: str, lyrics: str):
    # Write the lyrics to a file named 'song.txt' with UTF-8 encoding
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(lyrics)


def read_file_contents(filename):
    # Read and display the contents of 'song.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


def analyze_letter_frequency(content):
    content_lower = content.lower()
    # Count character frequencies
    unique_char_counts = len(set(content_lower))
    # Count letter frequencies (case-insensitive)
    letters = [char for char in content_lower if char.isalpha()]
    letter_counts = Counter(letters)
    # Count non-alphabet characters
    non_alpha_char = [char for char in content_lower if not char.isalpha()]
    non_alpha_char_counts = Counter(non_alpha_char)

    logging.info("\n===== Letter Frequency Results =====")
    for letter, count in sorted(letter_counts.items()):
        logging.info(f"{letter}: {count}")
    logging.info(f"\n===== Non-alphabet characters =====")
    logging.info(f"Total: {len(non_alpha_char)}")
    for char, count in non_alpha_char_counts.items():
        logging.info(f"{repr(char)}: {count}")

    return letter_counts, unique_char_counts, Counter(content_lower)


def analyze_character_usage(char_counts: Counter):
    # Most and least frequently used characters
    top_5 = char_counts.most_common(5)
    least_5 = char_counts.most_common()[:-6:-1]
    unused_letters = [char for char in string.ascii_lowercase if char not in char_counts]
    # string.ascii_lowercase - built-in, contains string of all lowercase letters in English alphabet

    logging.info("\n===== Top 5 Most Frequently Used Characters =====")
    for char, count in top_5:
        logging.info(f"{char}: {count}")

    logging.info("\n===== Top 5 Least Frequently Used Characters =====")
    for char, count in least_5:
        logging.info(f"{char}: {count}")

    logging.info("\n===== Unused Alphabet Characters =====")
    logging.info(", ".join(unused_letters))


def analyze_word_frequency(content):
    # Word frequency analysis
    # Remove punctuation, convert to lowercase, and split into words
    words = [word.strip(string.punctuation).lower() for word in content.split() if any(char.isalpha() for char in word)]
    word_counts = Counter(words)
    total_words = sum(word_counts.values())
    # analyzing WORD FREQUENCY: --> strip(string.punctuation) to exclude "..." (not a word)

    logging.info("\n===== Word Frequency Results =====")
    for word, count in word_counts.items():
        logging.info(f"'{word}': {count}")
    logging.info(f"\n===== Total unique words found in the lyrics: {len(word_counts)} =====")

    return word_counts, total_words

def log_word_percentages(word_counts, total_words):
    # Word percentage
    logging.info("\n===== Word Percentages =====")
    # formatting of columns
    logging.info(f"{'Word':<15} {'Occurrences':<12} {'Percentage (%)':<12}")
    logging.info("-" * 40)
    for word, count in word_counts.items():
        percentage = (count / total_words) * 100
        logging.info(
            f"{word:<15} {count:<12} {percentage:<12.2f}")  # f for floating point number, displays with exactly 2 decimal spaces

def log_top_10_words(word_counts, total_words):
    # Identify top 10 most frequent words
    top_10_words = word_counts.most_common(10)
    top_10_total = sum(count for _, count in top_10_words)

    logging.info("\n===== Top 10 Most Frequently Used Words =====")
    for word, count in top_10_words:
        logging.info(f"'{word}': {count}")

    top_10_percentage = (top_10_total / total_words) * 100
    logging.info(f"\nTop 10 words account for {top_10_percentage:.2f}% of the total words in the song.")

def reverse_content(content, output_filename):
    # Reverse the lyrics content
    reversed_content = content[::-1]
    # Save the reversed content to a new file
    with open(output_filename, 'w', encoding='utf-8') as file:
        file.write(reversed_content)
    # Print the reversed content to verify correctness
    logging.info("\n===== Reversed Content of 'song.txt' =====")
    logging.info(reversed_content)


def main():
    configure_logging()
    save_lyrics_to_file('song.txt', lyrics)
    content = read_file_contents('song.txt')

    logging.info("\n===== Contents of 'song.txt' =====")
    logging.info(content)

    letter_counts, unique_char_counts, char_counts = analyze_letter_frequency(content)
    analyze_character_usage(char_counts)

    word_counts, total_words = analyze_word_frequency(content)
    log_word_percentages(word_counts, total_words)
    log_top_10_words(word_counts, total_words)

    reverse_content(content, 'reversed.txt')

    logging.info("\nAnalysis complete. Results logged to execution_log.txt.")


# ensures that main functions runs only when script is directly executed
if __name__ == "__main__":
    main()