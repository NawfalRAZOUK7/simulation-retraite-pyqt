# 🤝 Contributing Guide

Thank you for considering a contribution to this project!  
Your help makes it more robust, complete, and useful for everyone. 🎉

---

## 🚀 What Can You Contribute?

- 🧠 **Code**: new features, bug fixes, refactoring
- 📝 **Documentation**: README, tutorials, docstrings, examples
- 🧪 **Tests**: unit, integration, UI tests

> Whether you're fixing a typo or adding a major feature, **your contribution is welcome**!

---

## 📝 Workflow

1. **Fork** this repository and clone your fork:
    ```bash
    git clone https://github.com/your-username/simulation-retraite-pyqt
    cd simulation-retraite-pyqt
    ```

2. **Create a branch** for your changes:
    ```bash
    git checkout -b feature/my-new-feature
    ```

3. **Write code** following [PEP8](https://peps.python.org/pep-0008/)  
   ➤ Use the **central logger** (`utils/logger.py`) – do not use `print()`.

4. **Add or update tests** to ensure correctness:
    ```bash
    pytest tests/
    ```

5. **Commit** with clear messages in **English**:
    ```bash
    git commit -m "Fix: handle empty dataframe in CSV export"
    ```

6. **Push your branch** and open a **Pull Request** (PR) on GitHub.

---

## 💡 Coding Standards

- Follow **PEP8** guidelines
- Use the **central logger** for all logs
- Write **modular, well-documented** code (docstrings encouraged)
- Keep one feature/fix per PR for clarity

---

## 🧪 Testing

- All features and bug fixes **must include tests**
- Run tests before pushing:
    ```bash
    pytest tests/
    ```
- If you add dependencies, update `requirements.txt`

---

## 📁 Sensitive Data & Files

- Do **not** commit `.env` files, passwords, or any sensitive data
- Ignore personal datasets, configs, or logs not meant to be public
- Provide sample config files like `config.example.json` when relevant

---

## 🛠️ Issues & Pull Requests

- Open **issues** for bugs, features, or questions
- Pull Requests are welcome from everyone – no strict template required  
  ➤ Just explain **what your PR does** and how to **test it or reproduce the change**

---

## 📄 License

This project is licensed under the **MIT License**.  
You are free to use, modify, and distribute it.

---

**Thank you for helping improve this project! 🎉**