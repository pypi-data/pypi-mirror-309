# kypo-aws-lib

Python library that serves as AWS driver for the sandbox-service (the Django microservice).
It is meant to be an installable component, not stand-alone library.

It implements the
[KypoCloudClientBase](https://gitlab.ics.muni.cz/muni-kypo-crp/backend-python/kypo-python-commons/-/blob/master/kypo/cloud_commons/cloud_client_base.py?ref_type=heads)
interface. The interface allows seemless integration to the KYPO CRP environment.

## Communication with AWS API
The library utilizes Boto3 library for communication with AWS API. Boto3 implements multiple clients,
each serving its own AWS Service.

## Contents
This library contains:
 * **kypo/aws_driver** -- the implementation of the library
 * **pyproject.toml** -- metadata of the library
