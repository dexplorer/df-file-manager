import requests
import streamlit as st
import argparse
import os
import tempfile
import logging
from dotenv import load_dotenv
from config.settings import ConfigParms as sc
from utils import logger as ufl


def upload_file(file_path: str, aws_iam_user_name: str, api_endpoint: str):
    """
    Uploads a file to a specified API endpoint.

    Args:
        file_path (str): The path to the file to be uploaded.

    Returns:
        str: The file path returned by the API.
    """
    logging.info("Temp file path %s", file_path)

    # Extract the file_name from the file path
    file_name = file_path.split("\\")[-1]

    # Prepare payload for the file upload request
    payload = {"aws_iam_user_name": aws_iam_user_name}
    files = {
        "data_file": (file_name, open(file_path, "rb")),
    }

    # Set headers for the file upload request
    headers = {"Accept": "application/json"}

    # Make a POST request to upload the file
    response = requests.post(
        url=api_endpoint,
        headers=headers,
        params=payload,
        files=files,
        timeout=2,
    )
    print("POST request response status code", response.status_code)

    if not response.ok:
        logging.info("Type: %s", response.headers["Content-Type"])
        # logging.info("Text: %s", str(response.text))
        # logging.info("JSON: %s", response.json())
        logging.info("Content: %s", response.content)
        response.raise_for_status()

    # Check if the file upload was successful (status code 200)
    if response.status_code == 200:
        # Print the API response for debugging
        print(response.json())
        # Return the file path returned by the API
        return response.json()["file_path"]


def main():
    parser = argparse.ArgumentParser(description="File Manager Application")
    parser.add_argument(
        "--aws_iam_user_name",
        help="Run as AWS IAM user",
        required=False,
    )

    # Get the arguments
    args = vars(parser.parse_args())
    logging.info(args)
    aws_iam_user_name = args["aws_iam_user_name"]

    # Load the environment variables from .env file
    load_dotenv()
    logging.info(os.environ)

    # Fail if env variable is not set
    sc.env = os.environ["ENV"]
    sc.app_root_dir = os.environ["APP_ROOT_DIR"]
    sc.load_config()

    BACKEND_URL = os.environ["BACKEND_URL"]
    # API endpoint for file upload
    api_endpoint = BACKEND_URL + "/upload-file"
    print("api end point", api_endpoint)

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    logging.info("Starting the UI")

    # Set page configuration for the Streamlit app
    st.set_page_config(page_title="File Manager", page_icon="📕", layout="wide")
    st.title("File Manager")

    # Select the AWS IAM user name if not provided as a command line argument
    if not aws_iam_user_name:
        aws_iam_user_names = [
            "ds_user_product",
            "ds_user_demographic",
            "ds_user_book_keeping",
        ]
        aws_iam_user_name = st.selectbox(
            "Select the AWS IAM user name", aws_iam_user_names
        )
        st.divider()

    # Allow user to upload a file
    uploaded_file = st.file_uploader(
        label="Input file", accept_multiple_files=False, type=["csv", "dat", "recon"]
    )
    st.divider()

    # Process the uploaded file if available
    if uploaded_file is not None:
        with tempfile.TemporaryDirectory() as td:
            logging.info("Temporary directory: %s", td)
            logging.info(os.listdir(td))

            if os.path.exists(td):
                file_path = os.path.join(td, uploaded_file.name)
                with open(file_path, "wb") as f:
                    f.write(uploaded_file.getbuffer())

                if os.path.exists(file_path):
                    logging.info("Temp file %s is created.", file_path)
                    # Upload the file to a specified API endpoint
                    s3_upload_url = upload_file(
                        file_path=file_path,
                        aws_iam_user_name=aws_iam_user_name,
                        api_endpoint=api_endpoint,
                    )
                    if s3_upload_url:
                        st.markdown("File is uploaded successfully.")
                        st.markdown(s3_upload_url)
                    else:
                        raise RuntimeError("File is not uploaded.")
                else:
                    raise RuntimeError("Unable to create the temp file.")
                return file_path
            else:
                raise RuntimeError("Temp file directory does not exist.")

    # from pathlib import Path

    # files = [file for file in Path("/workspaces/df-file-manager/data/in/").glob("*.csv")]
    # file = st.selectbox("Select a file", files)
    # st.divider()

    # # Process the uploaded file if available
    # if file is not None:
    #     # Save the file temporarily
    #     # Upload the file to a specified API endpoint
    #     s3_upload_url = upload_file(file_path=str(file), aws_iam_user_name=aws_iam_user_name)
    #     # s3_upload_url = s3_upload_url.split("/")[-1]

    #     st.markdown("File is uploaded successfully.")
    #     st.markdown(s3_upload_url)


if __name__ == "__main__":
    main()
