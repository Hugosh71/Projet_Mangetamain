# Git Workflow

## Branching Strategy

* **main**: Production-ready code
* **develop**: Integration branch for features
* **feature/\***: Feature development branches
* **hotfix/\***: Critical bug fixes

## Commit Guidelines

Use conventional commit messages:

```bash
feat: add new data visualization feature
fix: resolve memory leak in data processing
docs: update installation guide
test: add unit tests for core module
refactor: improve code organization
```

## Pull Request Process

1. **Create a feature branch:**

```bash
git checkout -b feature/new-feature
```

1. **Make your changes and commit:**

```bash
git add .
git commit -m "feat: add new feature"
```

1. **Push the branch:**

```bash
git push origin feature/new-feature
```

1. **Create a pull request** with:
   \* Clear description of changes
   \* Reference to related issues
   \* Screenshots for UI changes
   \* Test results
