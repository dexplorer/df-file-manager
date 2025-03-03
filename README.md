# df-file-manager

This application allows the human and application users to upload data files to AWS S3 bucket. 

Human (e.g. business) users can use the Streamlit UI to upload the files from their local machine to the AWS S3 bucket folder which is mapped to their user name. 

Application (e.g. batch/system) users can upload the files by invoking the FastAPI endpoint directly.

### Define the environment variables

Create a .env file with the following variables.

```
ENV=dev
APP_ROOT_DIR=
BACKEND_URL=
IAM_USER_ACCESS_KEY_DS_USER_PRODUCT=
IAM_USER_SECRET_DS_USER_PRODUCT=
IAM_USER_ACCESS_KEY_DS_USER_DEMOGRAPHIC=
IAM_USER_SECRET_DS_USER_DEMOGRAPHIC=
IAM_USER_ACCESS_KEY_DS_USER_BOOK_KEEPING=
IAM_USER_SECRET_DS_USER_BOOK_KEEPING=

```

### Install

- **Install via Makefile and pip**:
  ```
    make install
  ```

### Usage Examples

- **Upload a file to AWS S3 bucket via CLI**:
  ```sh
    fm-app-ui
  ```

- **Catalog a file to AWS S3 bucket via CLI with IAM user name**:
  ```sh
    fm-app-ui --aws_iam_user_name ds_user_product
  ```

- **Upload a file to AWS S3 bucket via API**:
  ##### Start the API server
  ```sh
    fm-app-api
  ```

  Note: Currently, the demo API endpoint is not configured to handle client authorization. So, change the port visibility from 'Private' to 'Public' for testing purposes. On the other hand, you could enhance the application to handle client authorization. See FastAPI documentation for reference. 

  ##### Invoke the API from Swagger Docs interface
  ```sh
    https://<host name with port number>/docs

  ```

  ##### AWS IAM User Config

Data sources would be assigned a folder in the AWS S3 bucket. AWS IAM user name is used to determine the bucket folder where the file is uploaded.

```
AWS_USER_CONFIG:
  DS_USER_PRODUCT:
    S3_PREFIX: "ds_user_product" # AWS S3 prefix or folder
    S3_BUCKET: "df-data-in"  # AWS S3 bucket name
    S3_REGION: "ap-south-1"  # AWS S3 region
  DS_USER_DEMOGRAPHIC:
    S3_PREFIX: "ds_user_demographic"
    S3_BUCKET: "df-data-in"
    S3_REGION: "ap-south-1"
  DS_USER_BOOK_KEEPING:
    S3_PREFIX: "ds_user_book_keeping"
    S3_BUCKET: "df-data-in"
    S3_REGION: "ap-south-1"

```
