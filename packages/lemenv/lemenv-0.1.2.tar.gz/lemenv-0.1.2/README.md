<div align="center">
  
# 🍋 LemEnv

<!-- These comments help GitHub generate better social previews -->
<!-- Title -->
<h1 align="center">LemEnv - Virtual Environment Manager</h1>

<!-- Description -->
<p align="center">
  A Citrus-Flavored Virtual Environment Manager that makes managing Python environments a breeze! 🍋✨
</p>

<!-- Badges -->
<p align="center">
  <a href="https://pypi.org/project/lemenv/">
    <img src="https://badge.fury.io/py/lemenv.svg" alt="PyPI version">
  </a>
  <a href="https://github.com/jakerains/lemenv/blob/main/LICENSE">
    <img src="https://img.shields.io/github/license/jakerains/lemenv" alt="License">
  </a>
</p>

</div>

A Citrus-Flavored Virtual Environment Manager - A friendly CLI tool that makes managing Python virtual environments a breeze!

## 📦 Installation

It's as simple as:

```bash
pip install lemenv
```

## 🚀 Quick Start

Simply run:

```bash
lemenv
```

<p align="center">
  <img src="screenshot.png" alt="LemEnv Menu" width="600"/>
</p>

That's it! Use the interactive menu to:
- 🔨 Create virtual environments (venv or conda)
- 📋 List your environments
- 🚀 Activate environments with clear instructions
- 🗑️ Delete environments safely
- 🔄 Recreate environments
- 📦 Install dependencies from requirements.txt
- ℹ️ View environment details

### Command Line Interface

```bash
# Create a new virtual environment
lemenv create [name]

# Activate a virtual environment
lemenv activate [name]

# List all virtual environments
lemenv list

# Delete a virtual environment
lemenv delete [name]

# Recreate a virtual environment
lemenv recreate [name]

# Install requirements
lemenv install [name] [requirements_file]

# Show environment info
lemenv info [name]
```

## Examples 📝

1. Create and activate a new environment:
   ```bash
   lemenv create myproject
   lemenv activate myproject
   ```

2. Install requirements:
   ```bash
   lemenv install myproject requirements.txt
   ```

3. Recreate an environment:
   ```bash
   lemenv recreate myproject
   ```

## Contributing 🤝

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments 🙏

- Thanks to all contributors who have helped shape LemEnv
- Built with Python, Click, and Inquirer

## Support 💬

If you have any questions or run into issues, please open an issue on the GitHub repository.

## 👤 Author

Created by GenAI Jake (@jakerains)

## ⭐ Show your support

Give a ⭐️ if this project helped you! 