from . import awsConfig
from botocore.exceptions import ClientError, ParamValidationError
import boto3
import botocore


class CognitoApi:
    def __init__(self):
        self.__regionName = awsConfig.regionName
        self.__aws_access_key_id = awsConfig.aws_access_key_id
        self.__aws_secret_access_key = awsConfig.aws_secret_access_key
        self.__clientId = awsConfig.clientId
        self.__userPoolId = awsConfig.userPoolId
        self.__client = boto3.client(
            'cognito-idp',
            region_name=self.__regionName,
            aws_access_key_id=self.__aws_access_key_id,
            aws_secret_access_key=self.__aws_secret_access_key
        )
    
    def signUpUser(self, daoData):
        try:
            response = self.__client.sign_up(
                ClientId=self.__clientId,
                Username=daoData['userData']['username'],
                Password=daoData['userData']['password'],
                UserAttributes=[
                    {
                        'Name': 'email',
                        'Value': daoData['userData']['email']
                    },
                    {
                        'Name': 'name',
                        'Value': daoData['userData']['name']
                    },
                    {
                        'Name': 'custom:role',
                        'Value': daoData['userData']['custom:role']
                    },
                ],
                ValidationData=[
                    {
                        'Name': 'email',
                        'Value': daoData['userData']['email']
                    }
                ],
            )
            
            return {'statusCode': 200, 'body': response}
        
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}
    
    def confirmUserEmail(self, daoData):
        try:
            response = self.__client.confirm_sign_up(
                ClientId=self.__clientId,
                Username=daoData['userData']['username'],
                ConfirmationCode=daoData['userData']['confirmationCode'],
                ForceAliasCreation=False
            )
            
            return {'statusCode': 200, 'body': response}
        
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}
    
    def addToAgentGroup(self, daoData):
        try:
            response = self.__client.admin_add_user_to_group(
                UserPoolId=self.__userPoolId,
                Username=daoData['userData']['username'],
                GroupName=daoData['metaData']['agent']
            )
            
            return {'statusCode': 200, 'body': response}
        
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}
    
    def retrieveUsers(self, daoData, fliter, attributesRetrieveList):
        try:
            response = self.__client.list_users(
                UserPoolId=self.__userPoolId,
                AttributesToGet=attributesRetrieveList,
                Filter=fliter + "=" + "\"" + daoData['userData'][fliter] + "\""
            )
            
            return {'statusCode': 200, 'body': response}
            
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}
    
    def retrieveUserGroup(self, daoData):
        try:
            response = client.admin_list_groups_for_user(
                Username=daoData['userData']['username'],
                UserPoolId=self.__userPoolId
            )
            
            return {'statusCode': 200, 'body': response}
            
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}
    
    def updateUserAttributes(self, daoData, attributesUpdateList):
        try:
            userAttributes = []
            for attribute in attributesUpdateList:
                if 'id' in daoData and attribute in daoData['id']:
                    userAttributes.append({'Name': attribute, 'Value': daoData['id'][attribute]})
                else:
                    userAttributes.append({'Name': attribute, 'Value': daoData['userData'][attribute]})
        
            response = self.__client.admin_update_user_attributes(
                UserPoolId=self.__userPoolId,
                Username=daoData['userData']['username'],
                UserAttributes=userAttributes
            )
            
            return {'statusCode': 200, 'body': response}
        
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}
    
    def deleteUser(self, daoData):
        try:
            response = self.__client.admin_delete_user(
                UserPoolId=self.__userPoolId,
                Username=daoData['userData']['username']
            )

            return {'statusCode': 200, 'body': response}
            
        except ClientError as error:
            print(error.response)
            return {'statusCode': 500, 'body': error.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}