from . import awsConfig
import boto3
from botocore.exceptions import ClientError, ParamValidationError


class IamApi:
    def __init__(self):
        self.__regionName = awsConfig.regionName
        self.__aws_access_key_id = awsConfig.aws_access_key_id
        self.__aws_secret_access_key = awsConfig.aws_secret_access_key
        self.__client = boto3.client(
            'iam',
            region_name=self.__regionName,
            aws_access_key_id=self.__aws_access_key_id,
            aws_secret_access_key=self.__aws_secret_access_key
        )
    
    def createIamUser(self, daoData):
        try:
            response = self.__client.create_user(
                UserName=daoData['userData']['username']
            )
            
            return {'statusCode': 200, 'body': response}
        
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}
    
    def addToRoleGroup(self, daoData):
        try:
            response = self.__client.add_user_to_group(
                GroupName=daoData['userData']['custom:role'] + '_' + daoData['metaData']['agent'],
                UserName=daoData['userData']['username']
            )
            
            return {'statusCode': 200, 'body': response}
            
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}