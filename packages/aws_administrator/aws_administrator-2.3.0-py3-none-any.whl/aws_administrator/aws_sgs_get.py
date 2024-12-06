#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Collect AWS Security Group details from multiple accounts."""

from . import helper_aws_ec2
from . import helper_common
from . import helper_aws_entrypoint
from .helper_parameters import *  # NOQA
from multithreader import threads


def aws_sgs_get():
    """Collect AWS Security Group details."""
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

    # Execute task with multithreading.
    items = {
        'session': session,
        'assumed_role_name': assumed_role_name,
        'external_id': external_id,
        'region': region
    }
    results = threads(
        helper_aws_ec2.get_sgs,
        account_ids,
        items,
        thread_num=THREAD_NUM
    )

    # Convert results to CSV data and write to file.
    csv_data = helper_common.dicts_to_csv(results)
    helper_common.export_csv(csv_data, sgs_get_output_file)


def main():
    """Execute main function."""
    aws_sgs_get()


if __name__ == '__main__':
    main()
