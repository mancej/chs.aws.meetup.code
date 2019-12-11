from botocore.exceptions import ClientError
from typing import List, Optional, Dict


class ParameterStoreService:
    """
    Should be used for all queries to SSM, has built in pagination, etc.
    """
    max_results = 50  # This is the max according to api docs.

    def __init__(self, boto_ssm_client):
        self._ssm = boto_ssm_client

    def get_all_parameters(self, prefixes: List[str], option: str = 'Recursive', page: str = None) -> List[dict]:
        """
        Returns all parameters under prefix. Automatically pages recursively then returns full result set
        Args:
            prefixes: List of prefixes to query. E.G. [ '/shared', '/data', '/app' ]
            existing_params: Used in recursive calls to build a total result set
            page: Used in recursive calls if more pages exist.
            option: Must be 'Recursive' or 'OneLevel' - Indiates # of levels below the prefix to recurse.
        Returns: List[dict] -> Parameter details as returned from AWS API

        """
        filters = {
                      'Key': 'Path',
                      'Option': f'{option}',
                      'Values': prefixes
                  },
        total_params = []
        if page:
            params = self._ssm.describe_parameters(ParameterFilters=filters, NextToken=page,
                                                   MaxResults=self.max_results)
        else:
            params = self._ssm.describe_parameters(ParameterFilters=filters, MaxResults=self.max_results)

        total_params = total_params + params['Parameters']

        if params and 'NextToken' in params:
            total_params = total_params + self.get_all_parameters(prefixes, option=option, page=params['NextToken'])

        return total_params

    def get_parameter_details(self, name) -> Dict:
        """
        Get the parameter details for a single parameter.
        :param name: The name of the parameter
        :return: Dict -> Parameter details as returned from AWS API
        """

        filters = {
            'Key': 'Name',
            'Values': [name]
        }

        result = self._ssm.describe_parameters(Filters=[filters])
        return result['Parameters'].pop() if len(result['Parameters']) > 0 else None

    def delete_parameter(self, key) -> None:
        """
        Deletes a parameter from PS
        Args:
            key: The PS Name - E.G. /app/demo-time/parameter/abc123

        Returns:

        """
        response = self._ssm.delete_parameter(Name=key)
        assert response and response['ResponseMetadata'] and response['ResponseMetadata']['HTTPStatusCode'] \
            and response['ResponseMetadata']['HTTPStatusCode'] == 200, \
            f"Error deleting key: [{key}] from PS. Please try again."

    def get_parameter(self, key):
        """
        Gets a parameter, returns None if parameter doesn't exist.
        Args:
            key: The PS Name - E.G. /app/demo-time/parameter/abc123

        Returns: str -> Parameter's value

        """
        try:
            parameter = self._ssm.get_parameter(Name=key, WithDecryption=True)
            return parameter['Parameter']['Value']
        except ClientError as e:
            if "ParameterNotFound" == e.response['Error']['Code']:
                return None
            else:
                raise

    def get_parameter_encrypted_by_version(self, key: str, ps_version: int) -> Optional[str]:
        try:
            parameter_history = self._ssm.get_parameter_history(
                Name=key,
                WithDecryption=False,
                MaxResults=10,
            )
            if len(parameter_history["Parameters"]) > 0:
                parameter = list(filter(lambda x: x["Version"] == ps_version, parameter_history["Parameters"]))
                if parameter:
                    return parameter[0]["Value"]
            else:
                return None
        except ClientError as e:
            if "ParameterNotFound" == e.response['Error']['Code']:
                return None
            else:
                raise

    def get_parameter_encrypted(self, key):
        """
            Returns the parameter without decrypting the value. If parameter isn't encrypted, it returns the value.
        Args:
            key: The PS Name - E.G. /app/demo-time/parameter/abc123

        Returns: str -> encrypted string value of an encrypted parameter.

        """
        try:
            parameter = self._ssm.get_parameter(Name=key, WithDecryption=False)
            return parameter['Parameter']['Value']
        except ClientError as e:
            if "ParameterNotFound" == e.response['Error']['Code']:
                return None
            else:
                raise

    def set_parameter(self, key, value, desc, type, key_id=None) -> None:
        """
        Sets a parameter in PS.
        Args:
            key: The PS Name - E.G. /app/demo-time/parameter/abc123
            value: Value to set
            desc: Description
            type: SecureString or String
            key_id: KMS Key Id to use for encryption if SecureString
        """
        # print(f"Inputting parameter {key} with value: {value} and DESC {desc} and type {type}")
        if key_id:
            self._ssm.put_parameter(
                Name=key,
                Description=desc,
                Value=value,
                Overwrite=True,
                Type=type,
                KeyId=key_id
            )
        else:
            self._ssm.put_parameter(
                Name=key,
                Description=desc,
                Value=value,
                Overwrite=True,
                Type=type
            )
