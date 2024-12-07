# Contributing

Contributions are welcome, and they are greatly appreciated! Every little bit
helps, and credit will always be given.

## Types of Contributions

### Report Bugs

If you find a bug, please report it. When doing so, include:

- Your operating system name and version.
- Details about your Python version and any other relevant package versions.
- Any specifics about your local setup that could aid troubleshooting.
- Step-by-step instructions to reproduce the issue.

### Fix Bugs

Check the [GitLab Issues](https://gitlab.com/psygraz/psychopy-bids/issues) for bugs. Issues tagged with `bug` and `help wanted` are open to anyone interested in resolving them.

### Implement Features

If you’d like to add new functionality, look for issues tagged with `enhancement` and `help wanted`. These are features the community has expressed interest in, and you’re welcome to tackle them.

### Write Documentation

Good documentation is vital! Contributions are welcome in all forms, including:

- Improving the official documentation.
- Adding or enhancing docstrings in the code.
- Writing tutorials, blog posts, or articles about using `psychopy-bids`.

### Submit Feedback

If you have ideas for new features or general feedback:

- Explain your idea in detail, including how it would work.
- Keep the scope narrow to make implementation easier.
- Remember, this is a community-driven project, and contributions are voluntary.

---

## Get Started!

Ready to contribute? Follow these steps to set up `psychopy-bids` for local development:

### 1. Clone the Repository

Clone the repository to your local machine:
```bash
git clone https://gitlab.com/psygraz/psychopy-bids.git
cd psychopy-bids
```

### 2. Set Up a Virtual Environment (Optional but Recommended)

For an isolated development environment, create a virtual environment:

- **Linux/macOS**:
  ```bash
  python3 -m venv env
  source env/bin/activate
  ```
- **Windows**:
  ```bash
  python -m venv env
  .\env\Scripts\activate
  ```

### 3. Install Dependencies

Install the package in editable mode:
```bash
pip install -e .
```

### 4. Create a Branch

Use Git (or similar) to create a branch for your work:
```bash
git checkout -b name-of-your-bugfix-or-feature
```

Replace `name-of-your-bugfix-or-feature` with something descriptive, like `fix-typo` or `add-new-feature`.

---

### Make Your Changes

Edit the code to fix bugs, implement features, or improve documentation. Ensure that:

- Your code follows the project’s style guide (e.g., PEP 8 for Python).
- You’ve added or updated tests to cover your changes.
- Documentation is updated, if applicable.

---

### Test Your Changes

Before submitting your changes, ensure everything works as expected:

1. **Run Tests**
   Use `pytest` to test your changes:
   ```bash
   pytest tests/
   ```

   > **Windows Users**: If `pytest` isn’t directly executable, use:
   ```bash
   python -m pytest
   ```

2. **Check Code Formatting**
   Use tools like `black` and `flake8` to maintain code consistency:
   ```bash
   black .
   flake8
   ```

   If these tools are not installed, add them:
   ```bash
   pip install black flake8
   ```

---

### Commit and Push Your Changes

1. **Stage Your Changes**
   Add the modified files to the staging area:
   ```bash
   git add .
   ```

2. **Commit Your Changes**
   Write a descriptive commit message:
   ```bash
   git commit -m "Fix: Correct typo in README"
   ```

3. **Push Your Changes**
   Push your branch to your fork:
   ```bash
   git push origin name-of-your-bugfix-or-feature
   ```

---

### Submit a merge Request

1. Go to the [original repository](https://gitlab.com/psygraz/psychopy-bids/merge_requests) on GitLab.
2. Click **New Merge Request** and select the branch from your fork.
3. Provide:
   - A concise title for the merge request.
   - A detailed description of your changes.
   - References to any related issues.

4. Submit the merge request!

---

## Merge Request Guidelines

To ensure smooth collaboration, make sure your merge request:

1. Includes tests for any new functionality or bug fixes.
2. Updates relevant documentation (if necessary).

---

## Code of Conduct

This project is released with a Code of Conduct. By contributing, you agree to abide by its terms, ensuring a respectful and inclusive community.