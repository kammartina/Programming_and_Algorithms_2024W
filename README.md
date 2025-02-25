# Programming_and_Algorithms_2024W
This repository contains code that is part of programming assignments in **Programming and Algorithms for Language Technologies in 2024W** (FH Campus Wien).

***ASSIGNMENTS OVERVIEW:***
<br><br>
**Exercise 1: Statistics**
<br>
This exercise focuses on processing and analyzing book metadata stored in JSON format. The goal is to practice working with dictionaries, lists, and sets while handling structured data efficiently. It involves implementing two functions:
- get_statistics(books: list) -> dict – Computes statistics for each author, including total pages, average chapters, book titles, and publication period.
- get_genres(books: list) -> list – Returns a unique list of genres from the dataset.
<br><br>

**Exercise 2: Finding Path with BFS**
<br>
This exercise focuses on implementing breadth-first search (BFS) to find a path in a labyrinth. Key concepts include queues, sets, tuple handling, and pathfinding algorithms, helping to reinforce Python skills for handling structured data and search problems. It involves:
- Displaying the labyrinth with row and column labels.
- Prompting the user for start and end locations.
- Implementing BFS to find the shortest path from start to end.
- Marking and displaying the found path within the labyrinth.
<br><br>

**Exercise 3: Python Recap – Object-Oriented Refactoring**
<br>
This exercise focuses on refactoring a procedural drawing application into an object-oriented design. The first assignment involves creating a Canvas class, encapsulating drawing functions, and introducing a Point class for better structure. The second assignment extends this by implementing a Shape class with geometric properties, such as calculating centroids and comparing shapes based on their distance from the origin. The exercise reinforces OOP principles, type hints, and packing/unpacking concepts in Python.
<br><br>

**Exercise 4: Text Analysis and Manipulation on Song Lyrics**
<br>
This exercise involves building a Python program to analyze song lyrics by processing text data, calculating frequencies, and reversing content. This exercise reinforces file handling, string manipulation, data processing, and logging techniques in Python. The program is:
- Storing lyrics in a file (song.txt).
- Reading and displaying the lyrics.
- Analyzing letter and word frequencies.
- Identifying frequently and infrequently used characters.
- Counting unique words and calculating their occurrence percentages.
- Reversing the lyrics and saving them in reversed.txt.
- Loging all results to execution_log.txt.
<br><br>

**Exercise 5: Shakespearean Sonnet Search Engine**
<br>
This project implements a search engine for Shakespearean sonnets, showcasing essential techniques in text processing and information retrieval that are critical for building robust language models. The goal is to demonstrate how to fetch, preprocess, index, and efficiently retrieve text data in response to user queries—an approach that underpins many modern NLP and search systems.
<br>
This exercise is important for language models because it illustrates fundamental principles of text normalization, indexing, and retrieval, all of which are vital for handling and interpreting large-scale language data. The conclusion is a fully functional search engine that deepens our understanding of text retrieval systems and reinforces techniques essential for advanced NLP applications.
<br><br>
Key accomplishments of the project include:
<br>
- API Integration: Fetches Shakespeare’s sonnets from the PoetryDB API and converts the data into object-oriented representations.
- Inverted Index Construction: Builds an inverted index to map words to the sonnets they appear in, facilitating rapid and efficient query processing.
- Text Processing & Stemming: Implements tokenization and applies Porter's stemming algorithm to normalize words, thereby improving search accuracy by treating different forms of words as equivalent.
- Boolean Retrieval: Supports complex multi-keyword queries through boolean retrieval, allowing users to effectively search and filter relevant sonnets.
<br><br>

**Exercise 6: Tree Traversal**
<br>
This exercise challenges to implement depth-first tree traversal techniques. It reinforces key concepts in recursion, iteration, tree data structures, and object-oriented design. It involves:
- Creating a TreeNode class to represent tree nodes.
- Implementing both recursive and iterative in-order traversal functions.
- Extending the TreeNode class with object-oriented traversal methods for in-order, pre-order, and post-order traversals using a visitor function.
