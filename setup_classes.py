import requests
from requests.auth import HTTPBasicAuth
import json

####################################
##################SCIM
####################################
class SCIM(object):
    def __init__(self, db_admin_username, db_admin_token, db_url):
        self.db_admin_username = db_admin_username
        self.auth = HTTPBasicAuth(db_admin_username, db_admin_token)
        self.db_url = db_url
        self.ServicePrincipal = self._ServicePrincipal(self)

    class _ServicePrincipal(object):
        def __init__(self, scim):
            self.scim = scim
            None
            
        def add(self, sp_application_id, sp_display_name):
            add_sp_json = {
                "schemas": [ "urn:ietf:params:scim:schemas:core:2.0:ServicePrincipal" ],
                "applicationId": sp_application_id,
                "displayName": sp_display_name
            }

            response = requests.post(f"{self.scim.db_url}/api/2.0/preview/scim/v2/ServicePrincipals",
                                    headers = {'Content-type': 'application/scim+json'},
                                    auth=self.scim.auth,
                                    data=json.dumps(add_sp_json))
            return response.json()
        
        def list(self):
            response = requests.get(f"{self.scim.db_url}/api/2.0/preview/scim/v2/ServicePrincipals",
                            headers = {'Content-type': 'application/scim+json'},
                            auth=self.scim.auth)
            return response.json()
        
        #GET ID
        def _get_sp_id(self, key, value):
            list_response = self.list()
            
            resources = list_response['Resources']

            for resource in resources:
                if resource[key] == value:
                    return resource['id']
            return False
            
        #DELETE
        def delete_by_application_id(sp_application_id):
            sp_id = self._get_sp_id('applicationId', sp_application_id)
            
            self.delete_by_id(sp_id)

        def delete_by_display_name(self, sp_display_name):
            sp_id = self._get_sp_id('displayName', sp_display_name)
            
            self.delete_by_id(sp_id)
            
        def delete_by_id(self, sp_id):
            response = requests.delete(f"{self.scim.db_url}/api/2.0/preview/scim/v2/ServicePrincipals/{sp_id}",
                               auth=self.scim.auth)
        
        #EXISTS
        def _exists(self, key, value):
            return self._get_sp_id(key, value)
        
        def exists_by_application_id(self, sp_application_id):
            sp_application_id = str(sp_application_id)
            
            return self._exists('applicationId', sp_application_id)

        def exists_by_display_name(self, sp_display_name):            
            return self._exists('displayName', sp_display_name)

        def exists_by_id(self, sp_id):    
            sp_id = str(sp_id)
            return self._exists('id', sp_id)

####################################
##################DatabricksAPI
####################################
class AADDatabricksAPI(object):
    def __init__(self, sp_tenant_id, sp_application_id, sp_client_secret, db_url):
        self.sp_tenant_id = sp_tenant_id
        self.sp_application_id = sp_application_id
        self.__sp_client_secret = sp_client_secret
        self.__access_token = self._get_access_token()
        self.db_url = db_url
        
    def _get_access_token(self):
        url = f"https://login.microsoftonline.com/{self.sp_tenant_id}/oauth2/token"
        payload=f'grant_type=client_credentials&client_id={self.sp_application_id}&client_secret={self.__sp_client_secret}&resource=2ff814a6-3304-4ab8-85cb-cd0e6f879c1d'
        headers = {
          'Content-Type': 'application/x-www-form-urlencoded',
          #'Cookie': 'fpc=AtJwuSM45ppNkRv77cLSY3RJnSnsAQAAACCLE9kOAAAAbOnoaQEAAACDixPZDgAAAA; stsservicecookie=estsfd; x-ms-gateway-slice=estsfd'
        }

        response = requests.request("POST", url, headers=headers, data=payload)

        access_token = response.json().get("access_token")
        
        return access_token
    
    def create_token(self, pat_token_comment, pat_token_lifetime_seconds="-1"):
        pat_token_lifetime_seconds = str(pat_token_lifetime_seconds)
        
        payload = {
            "comment": pat_token_comment,
            "lifetime_seconds": pat_token_lifetime_seconds
        }

        response = requests.post(
            f"{self.db_url}/api/2.0/token/create",
            headers={"Authorization": f"Bearer {self.__access_token}"},
            data=json.dumps(payload)
        )
        
        return response.json()
        
    def list_tokens(self):
        response = requests.get(
            f"{self.db_url}/api/2.0/token/list",
            headers={"Authorization": f"Bearer {self.__access_token}"}
        )
        
        return response.json()
    
    def revoke_token(self, token_id):
        payload = {
            "token_id": token_id
        }

        response = requests.post(
            f"{self.db_url}/api/2.0/token/delete",
            headers={"Authorization": f"Bearer {self.__access_token}"},
            data=json.dumps(payload)
        )
        
        return response.json()

####################################
##################DatabricksPermissionsAPI
####################################
class DatabricksPermissionsAPI(object):
    def __init__(self, db_admin_username, db_admin_token, db_url):
        self.db_admin_username = db_admin_username
        self.auth = HTTPBasicAuth(db_admin_username, db_admin_token)
        self.db_url = db_url

    def list_token_permissions(self):
        url = f"{self.db_url}/api/2.0/permissions/authorization/tokens"
        response = requests.get(url,
                                headers = {'Content-type': 'application/json'},
                                auth=self.auth)
        return response.json()

    def update_token_permissions(self, sp_application_id, permission_level="CAN_USE"):
        url = f"{self.db_url}/api/2.0/permissions/authorization/tokens"

        payload = {
          "access_control_list": [
            {
              "user_name": sp_application_id,
              "permission_level": permission_level
            }
          ]
        }

        response = requests.patch(url,
                                  headers = {'Content-type': 'application/json'},
                                  auth=self.auth,
                                  data=json.dumps(payload))
        return response.json()