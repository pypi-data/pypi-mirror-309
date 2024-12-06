#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""
List S3 buckets in AWS accounts.

The bucket name prefix and region can be provided to tind specific buckets.
"""

from . import helper_aws_s3
from . import helper_common
from . import helper_aws_entrypoint
from .helper_parameters import *  # NOQA
from multithreader import threads


def aws_s3_getbuckets():
    """Get S3 buckets."""
    # Enter AWS environment.
    session = helper_aws_entrypoint.auth(
        auth_method=auth_method,
        profile_name=profile_name,
        access_key_id=access_key_id,
        secret_access_key=secret_access_key,
        sso_url=sso_url,
        sso_role_name=sso_role_name,
        sso_account_id=sso_account_id
    )
    account_ids = helper_aws_entrypoint.crawler(
        session,
        accounts_list_src,
        accounts,
        ou,
        statuses
    )

    # Create items for multithreading.
    items = {
        'session': session,
        'assumed_role_name': assumed_role_name,
        'external_id': external_id,
        's3_getbuckets_prefix': s3_getbuckets_prefix,
        'region': region
    }

    # Execute task with multithreading.
    buckets = threads(
        helper_aws_s3.get_buckets,
        account_ids,
        items,
        thread_num=THREAD_NUM
    )

    # Write the list to JSON file.
    helper_common.write_json_obj(s3_getbuckets_output_file, buckets)


def main():
    """Execute main function."""
    aws_s3_getbuckets()


if __name__ == '__main__':
    main()
