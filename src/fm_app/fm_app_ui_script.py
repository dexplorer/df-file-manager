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
    aws_iam_user_name = args["aws_iam_user_name"]

    # Load the environment variables from .env file
    load_dotenv()

    # Fail if env variable is not set
    sc.load_config()

    script_name = os.path.splitext(os.path.basename(__file__))[0]
    ufl.config_logger(log_file_path_name=f"{sc.app_log_dir}/{script_name}.log")
    logging.info("Configs are set")
    logging.info(args)
    logging.info(os.environ)
    logging.info(sc.config)
    logging.info(vars(sc))

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
    logging.info(process.returncode)
    logging.info(process.stdout)
    logging.info(process.stderr)
    process.check_returncode()
