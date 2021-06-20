from . import awsConfig,agentConfig
from botocore.exceptions import ClientError, ParamValidationError
import boto3
import base64
import time
import json



class S3Api:
    def __init__(self):
        self.__regionName = awsConfig.regionName
        self.__aws_access_key_id = awsConfig.aws_access_key_id
        self.__aws_secret_access_key = awsConfig.aws_secret_access_key
        self.__bucketName = awsConfig.bucketName
        self.__faceImageFolderName = awsConfig.faceImageFolderName
        self.__agent = agentConfig.agent
        self.__client = boto3.client(
            's3',
            region_name=self.__regionName,
            aws_access_key_id=self.__aws_access_key_id,
            aws_secret_access_key=self.__aws_secret_access_key
        )
    
    def storeImage(self, daoData):
        try:
            self.__client.put_object(
                ACL='public-read',
                Body=base64.b64decode(daoData['userData']['picture']),
                Bucket=self.__bucketName,
                Key= self.__faceImageFolderName + '/' + daoData['userData']['username'] + '_' + daoData['id']['custom:faceId'],
                ContentEncoding='base64',
                ContentType='image/jpeg',
            )
            daoData['userData']['picture'] = 'https://' + self.__bucketName + '.s3-' + self.__regionName + '.amazonaws.com/'  + self.__faceImageFolderName + '/' + daoData['userData']['username'] + '_' + daoData['id']['custom:faceId']
            
            imageData = {
                'uid': daoData['id']['sub'],
                'faceId': daoData['id']['custom:faceId'],
                'name': daoData['userData']['username'],
                'faceImgUrl': daoData['userData']['picture'],
                'timestamp': time.time()
            }
            

            
            return {'statusCode': 200, 'body': daoData}
        
        except ClientError as e:
            print(e.response)
            return {'statusCode': 500, 'body': e.response['Error']['Message']}
        
        except ParamValidationError as error:
            print(error.kwargs['report'])
            return {'statusCode': 500, 'body': error.kwargs['report']}