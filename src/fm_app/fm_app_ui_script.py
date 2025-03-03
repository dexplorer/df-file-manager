import subprocess
import argparse
import os
import logging
from dotenv import load_dotenv
from config.settings import ConfigParms as sc
from utils import logger as ufl


def main():
    parser = argparse.ArgumentParser(description="File Manager Application")
    parser.add_argument(
        "--aws_iam_user_name",
        help="Run as AWS IAM user",
        const="",
        nargs="?",
        default="",
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

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.log_file_path}/{script_name}.log")
    logging.info("Configs are set")

    process = subprocess.run(
        [
            "streamlit",
            "run",
            "src/fm_app/fm_app_ui.py",
            "--",
            "--aws_iam_user_name",
            aws_iam_user_name,
        ],
        check=True,
    )
    print(process.returncode)
    print(process.stdout)
    print(process.stderr)
    process.check_returncode()
