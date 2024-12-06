import os
import requests
import zipfile
from urllib.parse import urlparse


class GitDownloader:
    """Class to handle downloading files and directories from a GitHub repository."""

    def __init__(self, url, save_as_zip=False):
        """
        Initializes the downloader with the given URL and output directory.
        :param url: GitHub URL to download from.
        :param save_as_zip: If True, save as a ZIP file; otherwise, save as individual files.
        """
        self.url = url
        self.save_as_zip = save_as_zip
        self.repo_info = self._parse_info()

    def _parse_info(self):
        """
        Parses the GitHub URL to extract repository information.
        """
        repo_path = urlparse(self.url).path.strip("/")
        split_path = repo_path.split("/")
        if len(split_path) < 2:
            raise ValueError("Invalid GitHub URL format.")

        info = {
            "author": split_path[0],
            "repository": split_path[1],
            "branch": split_path[3] if len(split_path) > 3 else "main",
            "root_name": split_path[-1],
            "res_path": "/".join(split_path[4:]) if len(split_path) > 4 else "",
        }
        info["url_prefix"] = (
            f"https://api.github.com/repos/{info['author']}/{info['repository']}/contents/"
        )
        info["url_postfix"] = f"?ref={info['branch']}"
        return info

    def _download_file(self, file_name, download_url):
        """
        Downloads a single file from GitHub.
        """
        print(f"Downloading file: {file_name}")
        response = requests.get(download_url, timeout=120)
        if response.status_code != 200:
            raise Exception(f"Failed to download file: {file_name}")
        return response.content

    def _download_dir(self, res_path):
        """
        Recursively downloads all files from a directory in the GitHub repository.
        """
        files = []
        dir_queue = [res_path]
        while dir_queue:
            current_path = dir_queue.pop(0)
            response = requests.get(
                f"{self.repo_info['url_prefix']}{current_path}{self.repo_info['url_postfix']}"
            )
            if response.status_code != 200:
                raise Exception(f"Failed to fetch directory listing: {current_path}")

            for item in response.json():
                if item["type"] == "file":
                    files.append((item["path"], item["download_url"]))
                elif item["type"] == "dir":
                    dir_queue.append(item["path"])

        return files

    def _save_files(self, files):
        """
        Saves downloaded files either as individual files or as a ZIP archive.
        :param files: List of tuples containing file paths and file content.
        """
        if self.save_as_zip:
            zip_file_path = f"{self.repo_info['root_name']}.zip"
            with zipfile.ZipFile(zip_file_path, "w") as zipf:
                for file_path, file_data in files:
                    zipf.writestr(file_path, file_data)
            print(f"ZIP file created: {zip_file_path}")
        else:
            for file_path, file_data in files:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(file_path, "wb") as file:
                    file.write(file_data)
            print("Files saved")

    def download(self):
        """
        Main function to download a repository, directory, or file.
        """
        print(f"Processing GitHub URL: {self.url}")
        if not self.repo_info["res_path"]:
            # Download the whole repository as a ZIP
            repo_zip_url = f"https://github.com/{self.repo_info['author']}/{self.repo_info['repository']}/archive/{self.repo_info['branch']}.zip"
            print(f"Downloading repository ZIP: {repo_zip_url}")
            response = requests.get(repo_zip_url)
            if response.status_code != 200:
                raise Exception("Failed to download repository ZIP.")

            zip_file_path = f"{self.repo_info['repository']}.zip"
            with open(zip_file_path, "wb") as zip_file:
                zip_file.write(response.content)
            print(f"Repository ZIP saved at: {zip_file_path}")
        else:
            # Determine if the resource is a file or a directory
            api_url = f"{self.repo_info['url_prefix']}{self.repo_info['res_path']}{self.repo_info['url_postfix']}"
            response = requests.get(api_url)
            if response.status_code != 200:
                raise Exception("Failed to fetch resource information.")

            resource_data = response.json()
            if isinstance(resource_data, list):
                # Resource is a directory
                print(f"Downloading directory: {self.repo_info['res_path']}")
                files = self._download_dir(self.repo_info["res_path"])
                downloaded_files = [
                    (file_path, self._download_file(file_path, download_url))
                    for file_path, download_url in files
                ]

                self._save_files(downloaded_files)
            elif "download_url" in resource_data:
                # Resource is a file
                print(f"Downloading file: {self.repo_info['res_path']}")
                file_data = self._download_file(
                    self.repo_info["res_path"], resource_data["download_url"]
                )

                self._save_files([(self.repo_info["res_path"], file_data)])
            else:
                raise Exception("Unexpected response data from GitHub API.")
