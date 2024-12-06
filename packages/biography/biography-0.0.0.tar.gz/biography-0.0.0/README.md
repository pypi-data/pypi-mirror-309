# GitStory

GitStory is a Python tool designed to extract and process git commit history from a repository. It generates a structured summary of commits, allowing for custom processing of changes using functions like LLM summarizers. This facilitates deeper insights into the development process by capturing not just what changed, but also the intent, mistakes, and context behind each commit.

## Features

- **Extract Commit Information**: Retrieves commit date, message, and changes per file.
- **Custom Processing**: Integrates with custom functions (e.g., LLM summarizers) to process commit diffs.
- **Structured Output**: Generates dictionaries with fields like `date`, `message`, `change_summary`, `aim`, `mistakes`, and `project_context`.
- **Extensible**: Easily modify or extend to include additional commit metadata.
- **No Branch Complexity**: Assumes all commits are merged into the main branch, simplifying the commit history.



## Installation

1. **Clone the Repository**

   ```
   git clone https://github.com/yourusername/gitstory.git
   ```

2. **Navigate to the Directory**

   ```
   cd gitstory
   ```

3. **Install Dependencies**

   GitStory uses Python's standard library modules, but if your custom processing functions require additional packages, install them using:

   ```bash
   pip install -r requirements.txt
   ```

   *Note: Ensure you have Python 3.6 or higher installed.*

## Usage

### Basic Usage

Run the script in the root directory of the git repository you want to analyze:

```bash
python gitstory.py
```

This will generate a `commits.json` file containing the extracted commit data with the following structure:

```json
[
  {
    "date": "2023-10-01 12:34:56 +0000",
    "message": "Initial commit",
    "change_summary": "Changes in README.md",
    "aim": "",
    "mistakes": "",
    "project_context": ""
  },
  {
    "date": "2023-10-02 14:20:10 +0000",
    "message": "Added new feature",
    "change_summary": "Changes in feature.py",
    "aim": "",
    "mistakes": "",
    "project_context": ""
  }
]
```

### Customizing Processing Functions

To integrate your custom processing logic (e.g., LLM summarizer), modify the `process_changes` function in `gitstory.py`:

```
def process_changes(commit_hash, changed_files):
    change_summaries = []
    for file in changed_files:
        diff = get_diff_for_file(commit_hash, file)
        # Integrate your custom function here
        summary = your_custom_function(diff)
        change_summaries.append(summary)
    return ' '.join(change_summaries)
```

Replace `your_custom_function` with your actual processing function.

## Configuration

- **Custom Functions**: Replace placeholders with your own logic for processing diffs.
- **Output Format**: Modify the commit dictionary structure in `gitstory.py` to include additional fields if needed.
- **Data Storage**: By default, the output is saved to `commits.json`. Change the filename or storage mechanism as desired.

## Examples

### Running with Default Settings

```bash
python gitstory.py
```

### Integrating an LLM Summarizer

```
def process_changes(commit_hash, changed_files):
    change_summaries = []
    for file in changed_files:
        diff = get_diff_for_file(commit_hash, file)
        # Example integration with an LLM summarizer
        summary = llm_summarizer.summarize(diff)
        change_summaries.append(summary)
    return ' '.join(change_summaries)
```

### Sample Output

After running the script with your custom processing, `commits.json` might look like:

```
[
  
    "date": "2023-10-01 12:34:56 +0000",
    "message": "Initial commit",
    "change_summary": "Set up project structure and added initial files.",
    "aim": "Establish the foundation for the project.",
    "mistakes": "Forgot to include .gitignore.",
    "project_context": "Starting the GitStory project to track commit histories."
  
  
]
```

## Contributing

Contributions are welcome! Please follow these steps:

1. **Fork the Repository**
2. **Create a Feature Branch**

   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Commit Your Changes**

   ```bash
   git commit -m "Description of your feature"
   ```

4. **Push to Your Fork**

   ```bash
   git push origin feature/your-feature-name
   ```

5. **Open a Pull Request**

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Contact

For questions or support, please open an issue on the [GitHub repository](https://github.com/yourusername/gitstory) or contact the maintainer:

- **Email**: your.email@example.com
- **GitHub**: [yourusername](https://github.com/yourusername)

---

*GitStory helps you narrate the evolution of your codebase by enriching commit history with meaningful summaries and insights.*
