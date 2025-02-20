import json                       # Standard Python library for parsing and generating JSON data
import requests                   # Third-party library (installed via pip) to make HTTP requests (for fetching sonnets)
from nltk.stem.porter import PorterStemmer  # From the NLTK library, the Porter stemmer is used to reduce words to their stem

# --------------------------------------------------------------------------------
# PART 1: FETCH DATA FROM THE POETRYDB API AND SAVE IT LOCALLY
# --------------------------------------------------------------------------------

# The endpoint for Shakespeare's sonnets in JSON format
url = "https://poetrydb.org/author,title/Shakespeare;Sonnet"

# Make a GET request to the specified URL to retrieve the data
response = requests.get(url)

# We'll store the downloaded sonnets here in an empty initialized list
sonnets_data = []

# Check if the HTTP request was successful (status code 200 indicates success)
if response.status_code == 200:
    # If successful, parse the response content as JSON
    sonnets_data = response.json()

    # Open or create a file named 'shakespeare_sonnets.json' for writing
    with open("shakespeare_sonnets.json", "w") as file:
        # Write the sonnets data in nicely formatted JSON (indent=4 for readability)
        # pretty-print the resulting JSON with an indentation of 4 spaces for each nested level
        json.dump(sonnets_data, file, indent=4)

    # Print how many sonnets were successfully fetched
    print(f"Fetched and stored {len(sonnets_data)} sonnets.")
else:
    # If the HTTP request was not successful, display an error message with the status code
    print(f"Failed to fetch sonnets. Status code: {response.status_code}")

# --------------------------------------------------------------------------------
# PART 2: DOCUMENT BASE CLASS
# --------------------------------------------------------------------------------

class Document:
    """
    A base class representing any text 'document':
      - Stores lines of text
      - Can tokenize them (lowercase, remove certain punctuation, split, stem)
    Both Sonnet and Query classes will inherit this functionality.
    """

    def __init__(self, lines: list[str]):
        """
        :param lines: a list of strings (each string is one 'line' of the document)
        """
        self.lines = lines                   # Store the lines of text for further processing
        self.stemmer = PorterStemmer()       # Create a PorterStemmer object to handle word stemming

    def tokenize(self) -> list[str]:
        """
        Transforms the lines in this document into a list of tokens, applying:
          - Lowercasing
          - Removal of specific punctuation
          - Splitting on whitespace
          - Stemming each word
        :return: A list of processed tokens (strings)
        """
        # Characters to remove from the lines before splitting
        chars_to_remove = ".,':;!?"

        # empty list will hold all the final tokens produced from the document
        tokens = []

        # Iterate over each line in the document
        for line in self.lines:
            # Convert the entire line to lowercase to normalize text
            line = line.lower()

            # Remove specific punctuation marks by replacing them with an empty string
            for c in chars_to_remove:
                line = line.replace(c, "")

            # Split the cleaned line into separate words/tokens by whitespace
            words = line.split()

            # Apply the Porter stemmer to each token to reduce it to its stem
            stemmed_words = [self.stemmer.stem(word) for word in words]

            # Extend our token list with these newly processed tokens
            tokens.extend(stemmed_words)

        return tokens  # Return the final list of processed tokens

# --------------------------------------------------------------------------------
# PART 3: SONNET CLASS
# --------------------------------------------------------------------------------

class Sonnet(Document):
    """
    Represents a single Shakespeare sonnet.
    Inherits tokenization behavior from class Document.
    """

    def __init__(self, sonnet_dict: dict):
        """
        :param sonnet_dict: A dictionary typically containing keys like
                            {'title': 'Sonnet 18: Shall I compare...', 'lines': [...14 lines...]}

        We extract:
          - The 'id' (integer number) of the sonnet from the 'title' (e.g., 'Sonnet 18' => id=18)
          - The 'title' (remainder after removing 'Sonnet 18: ')
          - The 'lines' of the sonnet (passed to Document.__init__)
        """
        # full_title might be something like "Sonnet 32: If thou survive my well-contented day"
        full_title = sonnet_dict['title']

        # Split at the first occurrence of ": " to separate "Sonnet 32" and "If thou survive..."
        parts = full_title.split(": ", 1)

        # Remove the text "Sonnet " from the first part (e.g., "Sonnet 32" -> "32")
        sonnet_number_str = parts[0].replace("Sonnet ", "")

        # Convert the extracted string to an integer (e.g., "32" -> 32)
        self.id = int(sonnet_number_str)

        # If there's text after the colon, treat it as the sonnet's 'title'
        # Otherwise, just use an empty string
        self.title = parts[1] if len(parts) > 1 else ""

        # Sonnet lines are stored under sonnet_dict['lines'] (usually 14 lines),
        # and we pass them to our parent Document's __init__ to handle them
        super().__init__(sonnet_dict['lines'])

    def __str__(self):
        """
        Allows printing a Sonnet object with a nice textual representation:
        'Sonnet <id>: <title>'
         followed by each line of the sonnet.
        """
        header = f"Sonnet {self.id}: {self.title}\n"
        full_text = "\n".join(self.lines)  # Join the lines with newline characters
        return header + full_text

    def __repr__(self):
        """
        Used for programmers when the object is represented in a debugger.
        """
        return f"Sonnet(id={self.id}, title={self.title!r}, lines={len(self.lines)})"

# --------------------------------------------------------------------------------
# PART 4: CREATE SONNET INSTANCES
# --------------------------------------------------------------------------------

# Convert each dictionary from the fetched data into a Sonnet object
sonnet_instances = [Sonnet(s) for s in sonnets_data]

# Print a brief overview: the ID and title of each Sonnet
for s in sonnet_instances:
    print(f"Sonnet {s.id}: {s.title}")

# --------------------------------------------------------------------------------
# PART 5: INVERTED INDEX CLASS (with 'add' method)
# --------------------------------------------------------------------------------

class Index(dict[str, set[int]]):
    """
    Represents an inverted index, which is a dictionary where:
      - key: token (a string, e.g. 'love')
      - value: set of document IDs where that token appears

    This class inherits from Python's built-in 'dict' but we store sets of ints as values.
    """

    def __init__(self, documents: list[Sonnet]):
        """
        :param documents: A list of Sonnet objects. We'll build an inverted index from them.
        """
        super().__init__()            # Initialize the parent 'dict' structure
        self.documents = documents    # Keep a reference to the original list of Sonnets

        # Add each Sonnet object to the index by calling our 'add' method below
        for document in documents:
            self.add(document)

    def add(self, document: Sonnet):
        """
        Processes a single Sonnet, tokenizes it, and updates the inverted index.

        For each token in the Sonnet, we add 'document.id' to the set of IDs mapped by that token.
        """
        # Use the inherited tokenize() method (from Document, used by Sonnet) to get the tokens
        tokens = document.tokenize()

        # Go through each token in this Sonnet
        for token in tokens:
            # If the token is not already a key in our dictionary, create an empty set for it
            if token not in self:
                self[token] = set()

            # Add this Sonnet's ID to the set of IDs for this token
            self[token].add(document.id)

# --------------------------------------------------------------------------------
# REDEFINE INDEX CLASS TO INCLUDE 'search' METHOD
# (just adding new function to the class instaed of redefining - prevents conflicts)
# --------------------------------------------------------------------------------

    def search(self, query: "Query") -> list[Sonnet]:
        """
        Return all Sonnets that contain EVERY token in the given Query object.

        Steps:
          1. Tokenize the query (same process as with Sonnets)
          2. For each token in the query, find the set of document IDs in the index
          3. Intersect those sets (because we want docs that contain ALL tokens)
          4. Convert the final set of document IDs back to Sonnet objects
          5. Return that list of matching Sonnet objects
        """
        # Convert the query into tokens
        query_tokens = query.tokenize()

        # If the query is empty (no tokens), there can be no matches
        if not query_tokens:
            return []

        # We start with the set of IDs from the first token
        first_token = query_tokens[0]
        if first_token not in self:
            # If the first token doesn't exist in the index at all, no documents will match
            return []

        # Initialize 'matching_ids' to the set of doc IDs where the first token appears
        matching_ids = set(self[first_token])

        # Go through the remaining tokens in the query
        for token in query_tokens[1:]:
            if token not in self:
                # If any token doesn't exist, there can be no matches for that token
                return []
            # Intersect the current matching IDs with the set of IDs for this token
            matching_ids = matching_ids.intersection(self[token])

            # If at any point the intersection is empty, no documents can match all tokens
            if not matching_ids:
                return []

        # Convert the set of matching IDs to Sonnet objects (by looking them up in 'self.documents')
        matched_sonnets = []
        for doc_id in sorted(matching_ids):
            for sonnet in self.documents:
                if sonnet.id == doc_id:
                    matched_sonnets.append(sonnet)
                    break  # Break once we found the matching Sonnet for this ID

        # Return the final list of matched Sonnet objects
        return matched_sonnets

# --------------------------------------------------------------------------------
# PART 6: QUERY CLASS
# --------------------------------------------------------------------------------

class Query(Document):
    """
    A single-line input from the user, treated like a Document so we can reuse
    the same tokenization process.
    """

    def __init__(self, query: str):
        """
        :param query: The user's search input, e.g. "love hate"
        We pass it to Document as a one-element list of lines so that the
        Document.tokenize() method can be used the same way as with sonnets.
        """
        super().__init__([query])

# --------------------------------------------------------------------------------
# PART 7: BUILD THE FINAL INDEX USING ALL SONNETS
# --------------------------------------------------------------------------------

# Create the inverted index from our list of Sonnet objects
index = Index(sonnet_instances)

# --------------------------------------------------------------------------------
# PART 8: USER INTERFACE (INTERACTIVE LOOP)
# --------------------------------------------------------------------------------

def main():
    """
    Provides an interactive console-based interface where a user can:
      - Type a search query
      - See which sonnets match
      - Type '0' to quit
    """

    print("\nWelcome to Shakespeare Sonnets Search!")
    print("Type '0' to quit.\n")

    # We already built 'index' outside main(), but some might prefer doing it inside.
    # We'll use the global 'index' here.

    # Infinite loop to repeatedly ask for user queries
    while True:
        # Prompt user for input
        user_input = input("Search for sonnets ('0' to quit)> ").strip()

        # If user types '0', exit the loop
        if user_input.lower() == '0':
            print("Goodbye!")
            break

        # Convert the user input to a Query object, ensuring it goes through the same tokenization
        query = Query(user_input)

        # Use the 'search' method of our index to find matching Sonnets
        results = index.search(query)

        # If we found no matching sonnets, notify the user
        if not results:
            print(f"--> No results for '{user_input}'.\n")
        else:
            # Print some quick stats: how many matched, and which IDs
            print(f"--> Found {len(results)} sonnets for '{user_input}': "
                  f"{', '.join(str(s.id) for s in results)}\n")

            # Print the full text of each matching Sonnet
            for sonnet in results:
                print(sonnet, "\n")

# This ensures the user interface only runs if this script is the 'main' file being executed
if __name__ == "__main__":
    main()
