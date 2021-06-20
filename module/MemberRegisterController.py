from . import CognitoApi, IamApi, S3Api
from . import agentConfig,thirdPartyServiceProviderConfig
import json
import requests

class MemberRegisterController:
    def __init__(self):
        self.__agent = agentConfig.agent
        self.__cognitoApi = CognitoApi.CognitoApi()
        self.__iamApi = IamApi.IamApi()
        self.__s3Api = S3Api.S3Api()
        self.__rekogntionTspUrl = thirdPartyServiceProviderConfig.rekogntionTspUrl
        self.__rekogntionTspApiKey = thirdPartyServiceProviderConfig.rekogntionTspApiKey

    
    def signUp(self, viewData):
        daoData = {
            'metaData': {
                'agent': self.__agent
            },
            'userData': viewData
        }
        
        result = self.__cognitoApi.signUpUser(daoData)

        return result
    
    def confirm(self, viewData):
        daoData = {
            'metaData': {
                'agent': self.__agent
            },
            'userData': viewData
        }

        result = self.__cognitoApi.confirmUserEmail(daoData)
        
        if result['statusCode'] == 200:
            #self.__cognitoApi.addToAgentGroup(daoData)
            #self.__cognitoApi.addToAgentGroup(daoData)
            self.__iamApi.createIamUser(daoData)
            self.__iamApi.addToRoleGroup(daoData)
        
        elif result['statusCode'] == 500:
            self.__cognitoApi.deleteUser(daoData)
        
        return result
    
    def fido(self, viewData):
        daoData = {
            'userData': viewData
        }

        attributesUpdateList = ['custom:publicKeyCred']
        result = self.__cognitoApi.updateUserAttributes(daoData, attributesUpdateList)
        return result
    
    def face(self, viewData):
        daoData = {
            'userData': viewData
        }

        attributesRetrieveList = ['sub']
        retrieveResult = self.__cognitoApi.retrieveUsers(daoData, 'username', attributesRetrieveList)
        daoData['id'] = {'sub': retrieveResult['body']['Users'][0]['Attributes'][0]['Value']}
    
        response = requests.put(self.__rekogntionTspUrl ,data = json.dumps(daoData),headers = {'x-api-key':self.__rekogntionTspApiKey})
        indexsFaceResult = json.loads(response.text)
        daoData['id']['custom:faceId'] = indexsFaceResult['body']['FaceRecords'][0]['Face']['FaceId']
        
        self.__s3Api.storeImage(daoData)
        attributesUpdateList = ['custom:faceId', 'picture']
        result = self.__cognitoApi.updateUserAttributes(daoData, attributesUpdateList)
        
        return result
    
    def line(self, daoData):
        attributesRetrieveList = []
        retrieveResult = self.__cognitoApi.retrieveUsers(daoData, 'name', attributesRetrieveList)
        daoData['userData']['username'] = retrieveResult['body']['Users'][0]['Username']
        attributesUpdateList = ['custom:lineId']
        self.__cognitoApi.updateUserAttributes(daoData, attributesUpdateList)
        return  verifyResult
        