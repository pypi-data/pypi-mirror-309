#!/usr/bin/env python3
# -*- coding: latin-1 -*-
"""Get AWS actions for services."""

from . import helper_aws_iam
from . import helper_common
from . import helper_aws_entrypoint
from .helper_parameters import *  # NOQA
from pprint import pprint as pp


def aws_actions_get():
    """Get AWS actions for services."""
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

    # Get actions.
    actions = helper_aws_iam.get_actions(
        session,
        actions_get_service
    )

    # Write policies to JSON file.
    helper_common.write_json_obj(
        actions_get_output_file,
        actions
    )

    # Filter actions by keyword.
    if actions_get_filter:
        filtered_actions = helper_aws_iam.filter_actions_keyword(
            actions,
            actions_get_filter
        )
        pp(filtered_actions)


def main():
    """Execute main function."""
    aws_actions_get()


if __name__ == '__main__':
    main()
