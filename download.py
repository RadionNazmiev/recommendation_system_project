import gdown


def download_file_from_google_drive(id, destination):
    url = f"https://drive.google.com/uc?id={id}"
    gdown.download(url, destination, quiet=False)


if __name__ == "__main__":
    file_id = "1-6h5f5UJ3o3Jr2Vn9qZ5Z3K1Q2w0J0Xb"
    destination = "model.pkl"
    download_file_from_google_drive(file_id, destination)