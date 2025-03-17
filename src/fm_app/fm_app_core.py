from config.settings import ConfigParms as sc

import os
import logging

from fastapi import (
    UploadFile,
    HTTPException,
)
from fastapi.responses import (
    JSONResponse,
)
import awswrangler as wr
import boto3


async def upload_file_to_s3(data_file: UploadFile, aws_iam_user_name: str) -> list:
    """
    Uploads a file to Amazon S3 storage.

    This route allows users to upload a file, which is saved temporarily, uploaded to Amazon S3,
    and then removed from the local file system. It returns the filename and S3 file path
    in the response JSON.

    Args:
        data_file (UploadFile): The file to be uploaded.

    Returns:
        JSONResponse: A JSON response containing the filename and S3 file path.

    Raises:
        HTTPException: If the file specified in `data_file` is not found (HTTP status code 404).
    """

    sc.load_aws_config(aws_iam_user_name=aws_iam_user_name)

    # Retrieve and assign environment variables to variables
    IAM_USER_ACCESS_KEY = os.environ.get(
        f"IAM_USER_ACCESS_KEY_{aws_iam_user_name.upper()}"
    )  # AWS IAM user access key
    IAM_USER_SECRET = os.environ.get(
        f"IAM_USER_SECRET_{aws_iam_user_name.upper()}"
    )  # AWS IAM user access key secret
    S3_PREFIX = sc.s3_prefix  # AWS S3 bucket prefix or folder name
    S3_BUCKET = sc.s3_bucket  # AWS S3 bucket name
    S3_REGION = sc.s3_region  # AWS S3 bucket name

    if IAM_USER_ACCESS_KEY and IAM_USER_SECRET and S3_REGION:
        # Create an AWS S3 session with provided access credentials
        aws_s3 = boto3.Session(
            aws_access_key_id=IAM_USER_ACCESS_KEY,  # Set the AWS access key ID
            aws_secret_access_key=IAM_USER_SECRET,  # Set the AWS secret access key
            region_name=S3_REGION,  # Set the AWS region
        )
    else:
        raise RuntimeError("Unable to create AWS S3 session.")

    file_name = data_file.filename.split("/")[-1]
    # print("Data file name", file_name)
    try:
        with open(f"{data_file.filename}", "wb") as out_file:
            content = await data_file.read()  # async read
            out_file.write(content)  # async write
        wr.s3.upload(
            local_file=data_file.filename,
            path=f"s3://{S3_BUCKET}/{S3_PREFIX}/{file_name}",
            boto3_session=aws_s3,
        )
        logging.info("Removing local file %s after uploading", data_file.filename)
        os.remove(data_file.filename)
        response = {
            "filename": file_name,
            "file_path": f"s3://{S3_BUCKET}/{S3_PREFIX}/{file_name}",
        }

    except FileNotFoundError as error:
        raise HTTPException(status_code=404, detail="Item not found") from error

    return JSONResponse(content=response)
