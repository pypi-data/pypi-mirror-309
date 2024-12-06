from .downloader import GitDownloader
import argparse

def main():
    """
    CLI entry point for the script.
    """
    parser = argparse.ArgumentParser(description="Download files from GitHub.")
    parser.add_argument("url", help="GitHub URL (file, directory, or repository).")
    parser.add_argument("-z", "--zip", action="store_true", help="Zip the downloaded files.")
    args = parser.parse_args()

    downloader = GitDownloader(args.url, save_as_zip=args.zip)
    downloader.download()

if __name__ == "__main__":
    main()

