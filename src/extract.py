"""
extract.py

Extract source data and
store raw files in AWS S3 Bronze Layer.
"""

import boto3
import pandas as pd

from botocore.exceptions import (
    ClientError
)

from config.config import Config

from src.logger import logger


# =====================================================
# S3 HELPERS
# =====================================================

def create_s3_client():

    return boto3.client(
        "s3",
        aws_access_key_id=(
            Config.AWS_ACCESS_KEY_ID
        ),
        aws_secret_access_key=(
            Config.AWS_SECRET_ACCESS_KEY
        ),
        region_name=(
            Config.AWS_REGION
        )
    )


def bucket_exists(s3):

    try:

        s3.head_bucket(
            Bucket=Config.S3_BUCKET_NAME
        )

        return True

    except ClientError:

        return False


def create_bucket_if_not_exists():

    s3 = create_s3_client()

    if bucket_exists(s3):

        logger.info(
            f"Bucket exists: "
            f"{Config.S3_BUCKET_NAME}"
        )

        return

    try:

        if Config.AWS_REGION == "us-east-1":

            s3.create_bucket(
                Bucket=(
                    Config.S3_BUCKET_NAME
                )
            )

        else:

            s3.create_bucket(

                Bucket=(
                    Config.S3_BUCKET_NAME
                ),

                CreateBucketConfiguration={
                    "LocationConstraint":
                    Config.AWS_REGION
                }
            )

        logger.info(
            f"Bucket created: "
            f"{Config.S3_BUCKET_NAME}"
        )

    except Exception as error:

        logger.error(
            f"Bucket creation failed: "
            f"{error}"
        )

        raise


# =====================================================
# BRONZE LAYER
# =====================================================

def upload_to_s3():

    """
    Upload raw source files
    to Bronze Layer.
    """

    create_bucket_if_not_exists()

    s3 = create_s3_client()

    source_files = [

        Config.DEPARTMENTS_FILE,

        Config.EMPLOYEES_FILE,

        Config.ATTENDANCE_FILE
    ]

    for file_path in source_files:

        try:

            s3.upload_file(

                str(file_path),

                Config.S3_BUCKET_NAME,

                file_path.name
            )

            logger.info(
                f"Uploaded: "
                f"{file_path.name}"
            )

        except Exception as error:

            logger.error(
                f"Upload failed for "
                f"{file_path.name}: "
                f"{error}"
            )

            raise


# =====================================================
# DATA EXTRACTION
# =====================================================

def extract_departments(etl):

    df = pd.read_csv(
        Config.DEPARTMENTS_FILE
    )

    etl.departments_df = df

    etl.total_departments_extracted = (
        len(df)
    )

    logger.info(
        f"Departments extracted: "
        f"{len(df)}"
    )


def extract_employees(etl):

    df = pd.read_csv(
        Config.EMPLOYEES_FILE
    )

    etl.employees_df = df

    etl.total_employees_extracted = (
        len(df)
    )

    logger.info(
        f"Employees extracted: "
        f"{len(df)}"
    )


def extract_attendance(etl):

    df = pd.read_csv(
        Config.ATTENDANCE_FILE
    )

    etl.attendance_df = df

    etl.total_attendance_extracted = (
        len(df)
    )

    logger.info(
        f"Attendance extracted: "
        f"{len(df)}"
    )


# =====================================================
# MASTER EXTRACTION
# =====================================================

def run_extraction(etl):

    upload_to_s3()

    extract_departments(
        etl
    )

    extract_employees(
        etl
    )

    extract_attendance(
        etl
    )

    logger.info(
        "Extraction completed."
    )