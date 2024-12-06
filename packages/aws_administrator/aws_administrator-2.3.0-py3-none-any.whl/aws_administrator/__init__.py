#!/usr/bin/env python3
# -*- coding: latin-1 -*-

"""
Run AWS administrative scripts.

Prerequisite steps:
1. Copy the extras/parameters.ini file to your current working directory.
2. Update the file with the necessary values.

Example usage:
```python
from aws_administrator import aws_sso_get
aws_sso_get.aws_sso_get()
```
"""


__version__ = '2.3.0'
__author__ = 'Ahmad Ferdaus Abd Razak'
__status__ = 'Production'
__all__ = [
    'aws_actions_get',
    'aws_sqs_get',
    'aws_sso_assign',
    'aws_sso_get',
    'aws_sso_json',
    'aws_sso_mappings',
    'aws_sso_memberships',
    'aws_sso_update',
    'aws_s3_getbuckets'
]
