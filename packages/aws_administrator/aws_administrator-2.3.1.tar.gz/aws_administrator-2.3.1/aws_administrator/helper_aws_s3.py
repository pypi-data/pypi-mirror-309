#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Provide common AWS S3 multithreaded functions."""

import aws_crawler
import boto3


def get_buckets(
    account_id: str,
    items: dict
) -> dict:
    """
    List S3 buckets in an AWS account.

    The bucket name prefix and region can be provided to tind specific buckets.
    """
    try:
        # Get auth credentials for each account.
        credentials = aws_crawler.get_credentials(
            items['session'],
            f'arn:aws:iam::{account_id}:role/{items["assumed_role_name"]}',
            items['external_id']
        )

        # Create AWS S3 client.
        client = boto3.client(
            's3',
            aws_access_key_id=credentials['aws_access_key_id'],
            aws_secret_access_key=credentials['aws_secret_access_key'],
            aws_session_token=credentials['aws_session_token']
        )

        # Create the paginator and get the list of buckets.
        paginator = client.get_paginator('list_buckets')

        # Get data based on the prefix and region.
        if not items['s3_getbuckets_prefix'] and not items['region']:
            response_iterator = paginator.paginate()
        elif not items['s3_getbuckets_prefix']:
            response_iterator = paginator.paginate(
                BucketRegion=items['region']
            )
        elif not items['region']:
            response_iterator = paginator.paginate(
                Prefix=items['s3_getbuckets_prefix']
            )
        else:
            response_iterator = paginator.paginate(
                Prefix=items['s3_getbuckets_prefix'],
                BucketRegion=items['region']
            )

        # Read through pages of bucket details and get bucket names.
        buckets = []
        for page in response_iterator:
            for bucket in page['Buckets']:
                buckets.append(bucket['Name'])

    except Exception as e:
        buckets = [str(e)]

    return {
        'account_id': account_id,
        'buckets': buckets
    }


def main():
    """Execute main function."""
    pass


if __name__ == '__main__':
    main()
