#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Convert human-readable SSO data to AWS IDs."""

from . import helper_aws_sso
from . import helper_common
from . import helper_aws_entrypoint
from .helper_parameters import *  # NOQA
from multithreader import threads


def aws_sso_json():
    """Convert human-readable SSO data to AWS IDs."""
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
    sso_admin = session.client(
        'sso-admin',
        region_name=region
    )
    identity_store = session.client(
        'identitystore',
        region_name=region
    )

    # List all Permission Sets in the organization.
    permission_sets = helper_aws_sso.get_all_permission_set_arns(
        sso_admin,
        sso_instance_arn
    )

    # Read JSON file.
    data = helper_common.read_json(sso_json_input_file)
    details = [item['details'] for item in data]

    # Read Permission Sets and principals from dictionary.
    permission_set_names = helper_aws_sso.read_permission_sets(details)
    users = helper_aws_sso.read_users(details)
    groups = helper_aws_sso.read_groups(details)

    # Execute tasks with multithreading.
    items = {
        'identity_store': identity_store,
        'identity_store_id': identity_store_id,
        'sso_admin': sso_admin,
        'sso_instance_arn': sso_instance_arn,
        'permission_sets': permission_sets
    }
    user_ids = threads(
        helper_aws_sso.get_user_id,
        users,
        items,
        thread_num=THREAD_NUM
    )
    group_ids = threads(
        helper_aws_sso.get_group_id,
        groups,
        items,
        thread_num=THREAD_NUM
    )
    permission_set_arns = threads(
        helper_aws_sso.get_permission_set_arn,
        permission_set_names,
        items,
        thread_num=THREAD_NUM
    )

    # Process JSON file.
    processed = helper_aws_sso.process_json(
        sso_json_input_file,
        user_ids,
        group_ids,
        permission_set_arns
    )

    # Write results to file.
    helper_common.write_json_str(
        sso_json_output_file,
        processed
    )


def main():
    """Execute main function."""
    aws_sso_json()


if __name__ == '__main__':
    main()
