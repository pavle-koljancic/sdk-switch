# Openfiber workers and workflows

## 1. Prerequisites

- Python 3.14.6
- [Poetry](https://python-poetry.org/docs/#installing-with-the-official-installer) version 2.0.0 or newer
    - You may install Poetry using: `curl -sSL https://install.python-poetry.org | python3 -`

## 2. Setting Up the Project with Poetry

1. Navigate to the project directory:
   ```sh
   cd openfb
   ```

2. Configure Poetry to use the correct Python 3 path (Python 3.11):
   ```sh
   poetry env use python3.14.6
   ```

3. Activate the created environment. For IDE users, verify that the installed environment is detected. If not, manually
   configure the environment in the IDE settings to ensure proper integration.

## 3. Installing project dependencies

To install only the necessary production dependencies, run the following command:

```sh
poetry install
```

If you need all dependencies, including those for development and testing, run:

```sh
poetry install --with dev,test
```

## 4. Running main for local development

1. Change [config/.env.template] to `config/.env` and
   fill in required variables (DB and NSO values, CSV paths, etc.).
2. Make sure you have access to external services.
3. Use `poetry run python main.py` to start the main script.

That’s all - your local environment is now ready and running!


## Port forwarding

> **Note:** You need to have active VPN connection. Make sure to replace `<username>` value with the correct one.
> Password will be requested afterward.

```sh
ssh -L 5432:10.246.129.2:5432 -L 8080:10.246.128.126:8080 <username>@10.246.128.54
```


## Running pre-commit hooks, static Analysis, and type checking

We utilize **Ruff** for linting and formatting, and **Mypy** for type checking.
A GitHub Action is configured to automatically run these checks on pull requests, ensuring all changes meet the
required code quality and type-checking standards.

All of these checks are integrated into the pre-commit hooks, which can be executed with the following command:

```sh
poetry run pre-commit run --all-files
```

Run the following command from the root project folder to start the execution of unit tests:

```sh
poetry run pytest
```

While not needed, you can also run each tool separately:

* Run `ruff` linter:

   ```sh
   poetry run ruff check .
   ```

* Automatically fix issues related to `ruff` linting:

   ```sh
   poetry run ruff check . --fix
   ```

* Run `ruff` formatter:

   ```sh
   poetry run ruff format
   ```

* Run `mypy` for type checking:

   ```sh
   poetry run mypy .
   ```
## Generate documentation with AI assistant (Cursor)
### Prompt
```
You are a senior technical writer and system analyst.
Your task is to:
1. Analyze the entire project workflows:
* Go through all workflow definitions, automation scripts, and process logic.
* Identify the current, real state of how workflows function (not just intended design).
* Detect inconsistencies, deprecated steps, missing links, or outdated logic.
2. Build an accurate mental model of the system:
* Understand how different workflows connect.
* Identify inputs, outputs, dependencies, and triggers.
* Note any recent changes reflected in the code but not in documentation.
3. Update documentation in the `/docs` folder:
* Go through ALL `.md` files.
* Update content so it matches the CURRENT behavior of workflows.
* Do NOT invent features that do not exist in the code.
4. Preserve formatting strictly:
* Keep the existing structure, headings, and layout.
* Do NOT change styling, tone, or file organization.
* Only modify the textual content where necessary.
* Keep markdown formatting intact (lists, tables, code blocks, anchors, etc.).
5. Improve clarity without altering structure:
* Rewrite unclear or outdated explanations.
* Ensure terminology is consistent across all files.
* Remove obsolete references.
6. Consistency rules:
* Same terms must be used everywhere for the same concepts.
* Workflow names must match exactly with implementation.
* Step ordering must reflect real execution order.
7. Output format:
* Return updated versions of each modified `.md` file.
* Clearly indicate file paths.
* Do NOT include explanations outside the files.
Important constraints:
* Do NOT redesign documentation.
* Do NOT summarize—fully update content.
* Do NOT skip any file in `/docs`.
* If something is unclear, infer only from existing code and workflows.
Goal:
Make documentation 100% aligned with the actual system behavior while keeping the exact visual and structural format unchanged.
```
