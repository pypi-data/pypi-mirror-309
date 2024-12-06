# GitDownloader

![GitDownloader-Logo](https://raw.githubusercontent.com/PtPrashantTripathi/GitDownloader/refs/heads/main/.github/GitDownloader-Logo.webp)

**GitDownloader** is a Python CLI tool for downloading files, directories, or entire repositories from GitHub, supporting recursive downloads for folders and the option to save files as a ZIP archive.

## Features

- Download individual files, directories, or entire repositories from GitHub.
- Recursively fetch files from a directory in a repository.
- Option to save files as individual files or compress them into a ZIP archive.
- Simple and user-friendly CLI interface.

## Installation

Ensure you have Python 3.7 or later installed. Then, install **GitDownloader** using `pip`:

```bash
pip install GitDownloader
```

Alternatively, clone the repository and install it directly:

```bash
git clone https://github.com/PtPrashantTripathi/GitDownloader.git
cd GitDownloader
pip install .
```

## Usage

### Command Line Interface (CLI)

Use the `GitDownloader` command to download GitHub files or directories:

```bash
GitDownloader <GitHub URL>
```

### Examples

1. **Download a single file**:
   ```bash
   GitDownloader https://github.com/user/repo/blob/main/path/to/file.txt
   ```

2. **Download an entire directory**:
   ```bash
   GitDownloader https://github.com/user/repo/tree/main/path/to/directory
   ```

3. **Download the whole repository**:
   ```bash
   GitDownloader https://github.com/user/repo
   ```

4. **Save files as a ZIP archive**:

   Add `-z` to zip the downloaded files.
   ```bash
   GitDownloader https://github.com/user/repo/tree/main/path/to/directory -z
   ```   

## License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT).

## Contribution

Contributions are welcome! Please fork the repository, create a feature branch, and submit a pull request.

## Contact

- **Author**: Prashant Tripathi  
- **Email**: [PtPrashantTripathi@outlook.com](mailto:PtPrashantTripathi@outlook.com)  
- **GitHub**: [PtPrashantTripathi](https://github.com/PtPrashantTripathi)

## Disclaimer

This tool interacts with GitHub's APIs and is subject to GitHub's rate limits and terms of service.

---

Made with ❤️ in Bharat
