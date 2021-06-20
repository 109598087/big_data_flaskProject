from . import DynamoDBApi
from . import agentConfig


class ConfigController:
    def __init__(self):
        self.__agent = agentConfig.agent
        self.__dynamodbApi = DynamoDBApi.DynamoDBApi()

    def updateAiConfig(self,aiConfigData):
        aiDynamoDbConfigData = {
            "agent":self.__agent,
            "aiApp":aiConfigData['aiApp'],
            "key":aiConfigData['key'],
            "value":aiConfigData['value']
        }

        self.__dynamodbApi.updateAiDynamoDbConfig(aiDynamoDbConfigData)

    def retrieveAiConfig(self,aiApp):
        aiConfigData = self.__dynamodbApi.retrieveAiConfig(self.__agent, aiApp)
        return aiConfigData