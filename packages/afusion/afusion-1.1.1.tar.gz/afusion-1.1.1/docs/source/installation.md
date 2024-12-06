# Installation Guide

This section provides detailed instructions on how to install and set up AFusion and its prerequisites.

## Prerequisites

Before installing AFusion, ensure that you have the following components installed on your system:

### 1. 🐳 Docker Installed

- **Docker** is required to run AlphaFold 3.
- **Installation**: Download and install Docker from the [official website](https://www.docker.com/get-started/).
- **Post-Installation**:
  - Ensure Docker is running properly.
  - Verify that your user has permission to execute Docker commands.

### 2. 🧬 AlphaFold 3 Installed

- AFusion requires **AlphaFold 3** to be installed and set up on your system.
- **Installation Instructions**:
  - Follow the instructions provided in the [AlphaFold 3 GitHub Repository](https://github.com/google-deepmind/alphafold3) to install AlphaFold 3.
  - Make sure to download the model parameters and required databases.

### 3. 🐍 Python 3.10 or Higher

- AFusion is built with Python and requires **Python 3.10** or higher.
- **Installation**:
  - Download Python from the [official website](https://www.python.org/downloads/).
  - Alternatively, use a package manager like `apt`, `brew`, or `conda`.

## Installation and Running

Follow these steps to install and launch AFusion:

### 1. Install AFusion

Run the following command in your terminal to install AFusion:

```bash
pip install afusion
```

- **Note**: This command will install AFusion and all its dependencies, including Streamlit.

### 2. Run AFusion GUI

After installation, you can start AFusion by running:

```bash
afusion
```

- This command will launch the AFusion graphical user interface (GUI) in your default web browser.

---

**Important Notes:**

- **AlphaFold 3 Installation**: Ensure you have correctly installed AlphaFold 3, including model parameters and required databases, following the [AlphaFold 3 Installation Guide](https://github.com/google-deepmind/alphafold3/blob/main/docs/installation.md).
- **Docker Configuration**: After installing Docker, make sure it is running properly and that your user has permission to execute Docker commands.
- **Streamlit Dependency**: AFusion's installation will automatically install all required dependencies, including Streamlit. There's no need to install it separately.

---

## Troubleshooting

If you encounter any issues during installation or usage, consider the following steps:

- **Docker Issues**:
  - Ensure Docker is running.
  - On Linux, you might need to add your user to the `docker` group:

    ```bash
    sudo usermod -aG docker $USER
    ```

    - Log out and log back in for the changes to take effect.

- **Python Version**:
  - Verify your Python version:

    ```bash
    python --version
    ```

  - If it's below 3.10, install the correct version.

- **AlphaFold 3 Setup**:
  - Double-check that all paths and environment variables required by AlphaFold 3 are correctly set.

- **Dependencies**:
  - If you have conflicting packages, consider using a virtual environment:

    ```bash
    python -m venv afusion_env
    source afusion_env/bin/activate
    ```

    - Then install AFusion within this environment.

---

For further assistance, please refer to the official documentation or [open an issue](https://github.com/your-repo/issues) on the GitHub repository.

---

**Next Steps**:

- Proceed to the [Usage Guide](index.md#usage) to learn how to use AFusion.
- Explore the [API Documentation](api.md) for information on batch predictions (coming soon).

---

**Happy Folding! 🧬**
