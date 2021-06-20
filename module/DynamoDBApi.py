from . import awsConfig
import boto3


class DynamoDBApi:
    def __init__(self):
        self.__regionName = awsConfig.regionName
        self.__aws_access_key_id = awsConfig.aws_access_key_id
        self.__aws_secret_access_key = awsConfig.aws_secret_access_key
        self.__dynamoDbResource = boto3.resource(
            'dynamodb', 
            aws_access_key_id=self.__aws_access_key_id, 
            aws_secret_access_key=self.__aws_secret_access_key,
            region_name=self.__regionName
        )
        self.__table = self.__dynamoDbResource.Table(awsConfig.table)

    def updateAiDynamoDbConfig(self,aiDynamoDbConfigData):
        self.__table.update_item(
            Key={
                'agent':aiDynamoDbConfigData['agent'],

            },
            UpdateExpression='SET aiApps.' + aiDynamoDbConfigData['aiApp'] + '.' + aiDynamoDbConfigData['key'] + ' = :value',
            ExpressionAttributeValues={
                ':value': aiDynamoDbConfigData['value']
            }
        )

    def retrieveAiConfig(self, agent, aiApp):
        response = self.__table.get_item(
            Key={
                'agent': agent,
            }
        )

        item = response['Item']
        aiConfigData = item['aiApps'][aiApp]
        print(aiConfigData)

        return aiConfigData

    def insertConfig(self,config):
        self.__table.put_item(
           Item = config
        )