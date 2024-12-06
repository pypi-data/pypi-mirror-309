#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Get AWS SSO membership details from mappings data."""

from . import helper_aws_sso
from . import helper_common
from . import helper_aws_entrypoint
from .helper_parameters import *  # NOQA
from multithreader import threads


def aws_sso_memberships():
    """Get AWS SSO membership details from mappings data."""
    # Read JSON data from file.
    data = helper_common.read_json(sso_memberships_input_file)
    groups = helper_aws_sso.read_groups(data)

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
    identity_store = session.client(
        'identitystore',
        region_name=region
    )

    # Execute task with multithreading.
    items = {
        'identity_store': identity_store,
        'identity_store_id': identity_store_id
    }
    group_memberships = threads(
        helper_aws_sso.get_group_memberships,
        groups,
        items,
        thread_num=THREAD_NUM
    )

    # Write Groups JSON data to file.
    helper_common.write_json_obj(
        sso_memberships_output_file,
        {
            'groups': groups,
            'group_memberships': group_memberships
        }
    )


def main():
    """Execute main function."""
    aws_sso_memberships()


if __name__ == '__main__':
    main()
