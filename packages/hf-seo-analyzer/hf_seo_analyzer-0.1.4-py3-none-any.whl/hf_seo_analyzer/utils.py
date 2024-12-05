import os

def read_markdown_file(file_path):
    """
    Reads a Markdown file and returns its content.

    :param file_path: Path to the Markdown file.
    :return: Markdown content as a string.
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()

def read_markdown_directory(directory_path):
    """
    Reads all Markdown files in a directory.

    :param directory_path: Path to the directory.
    :return: List of tuples (file_name, file_content).
    """
    markdown_files = [
        (file, read_markdown_file(os.path.join(directory_path, file)))
        for file in os.listdir(directory_path)
        if file.endswith(".md")
    ]
    return markdown_files

def string_to_markdown(content, file_path):
    """
    Save a string to a Markdown file.

    :param content: The string content to save.
    :param file_path: The path to save the Markdown file.
    """
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"Content saved to {file_path}")
