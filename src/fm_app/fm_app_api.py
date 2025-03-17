import os
import logging
from dotenv import load_dotenv
from config.settings import ConfigParms as sc
from fm_app import fm_app_core as fmc
from utils import logger as ufl
from pydantic import BaseModel
from fastapi import FastAPI
import uvicorn
from fastapi import (
    UploadFile,
    Depends,
    File,
)
from fastapi.middleware.cors import (
    CORSMiddleware,
)


class UserFile(BaseModel):
    aws_iam_user_name: str
    data_file: UploadFile = File(...)


app = FastAPI()

origins = [
    "http://localhost:8501",
    "https://studious-fiesta-6j4pjrpv47fx555-8501.app.github.dev",
    "http://ec2-13-233-72-225.ap-south-1.compute.amazonaws.com:8501",
]

# Add CORS middleware to handle Cross-Origin Resource Sharing
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=False,  # Allow sending credentials (e.g., cookies)
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all HTTP headers
)


@app.get("/")
async def root():
    """
    Default route

    Args:
        none

    Returns:
        A default message.
    """

    return {"message": "File Manager App"}


@app.post("/upload-file")
async def upload_file(user_file: UserFile = Depends()):
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

    logging.info("Start uploading the file %s", user_file.data_file.filename)
    response = await fmc.upload_file_to_s3(
        data_file=user_file.data_file,
        aws_iam_user_name=user_file.aws_iam_user_name,
    )
    logging.info("Finished uploading the file %s", user_file.data_file.filename)

    return response


def main():
    # Load the environment variables from .env file
    load_dotenv()

    # Fail if env variable is not set
    sc.load_config()

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.app_log_dir}/{script_name}.log")
    logging.info("Configs are set")
    logging.info(os.environ)
    logging.info(sc.config)
    logging.info(vars(sc))

    logging.info("Starting the API service")

    uvicorn.run(
        app,
        port=8080,
        host="0.0.0.0",
        log_config=f"{sc.app_config_dir}/api_log.ini",
    )

    logging.info("Stopping the API service")


if __name__ == "__main__":
    main()
