#!/usr/bin/env pythonw
# -*- coding: utf-8 -*-
#
#  Git SERVICE FOR GENROPY
#  This service allows to perform connection between Git API and Genropy  
#
#  Created by Davide Paci on 2022-05-13
#  Copyright (c) 2022 Softwell. All rights reserved.
#

# --------------------------- BaseWebtool subclass ---------------------------

#Git OAuth: https://docs.github.com/en/rest/guides/basics-of-authentication

import requests, json
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbaseservice import GnrBaseService
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrbag import Bag 

api_url = 'https://api.github.com'
auth_api_url = 'https://github.com/login/oauth'

class GnrCustomWebPage(object):
    py_requires='gnrcomponents/externalcall:BaseRpc'

class Main(GnrBaseService):
    def __init__(self, parent, g_access_token=None, g_refresh_token=None, 
                    g_client_id=None, g_secret=None, **kwargs):
        """Defines initial parameters (g_access_token, g_client_id and g_secret) and 
        API call parameters"""
        self.parent = parent
        self.g_access_token = g_access_token
        self.g_client_id = g_client_id
        self.g_secret = g_secret

    @public_method
    def getWorkspaces(self):
        "Returns organization ID"
        headers = {'Authorization': f'Bearer {self.g_access_token}', 'Accept': 'application/json'}

        r = requests.get(f'{api_url}/user/orgs', headers=headers)

        if not r.ok:
            print("**Github** Error (getWorkspaces) / http code: " + str(r.status_code) + ", body message: " + str(r.content))
        else:
            #DP Sistemare con esempio concreto di org
            result = json.loads(r.text)
            #workspaces = Bag()
            #workspaces.fromJson(result)
            return result

    @public_method
    def getUser(self):
        "Returns user data"
        headers = {'Authorization': f'Bearer {self.g_access_token}', 'Accept': 'application/json'}

        r = requests.get(f'{api_url}/user', headers=headers)

        if not r.ok:
            print("**Github** Error (getUser) / http code: " + str(r.status_code) + ", body message: " + str(r.content))
        else:
            result = json.loads(r.text)
            user_data = Bag()
            user_data.fromJson(result)
            return user_data

    @public_method
    def getProjects(self, workspace_slug=None):
        "Get All Github repositories in a workspace"
        headers = {'Authorization': f'Bearer {self.g_access_token}', 'Accept': 'application/json'}
        #DP Sistemare con esempio concreto di org
        #if workspace_slug:
        #    workspace = f'orgs/{workspace_slug}'
        #else:
        #    workspace = 'user'

        r = requests.get(f'{api_url}/user/repos', headers=headers)

        if not r.ok:
            print("**Github** Error (getProjects) / http code: " + str(r.status_code) + ", body message: " + str(r.content))
        else:
            result = json.loads(r.text)
            projects = Bag()
            projects.fromJson(result)
            return projects
    

#Github SERVICE CONFIGURATION PAGE TO INSERT ACCESS TOKEN AND PAGE ID/SECRET
class ServiceParameters(BaseComponent):
    def service_parameters(self,pane,datapath=None,**kwargs):        
        top = pane.borderContainer(region='center')
        cp = top.contentPane(region='top')
        fb = cp.formbuilder(datapath=datapath)
        fb.textbox(value='^.g_client_id',lbl='Github Client ID')
        fb.textbox(value='^.g_secret',lbl='Github Client Secret')
        fb.textbox(value='^.g_redirect_uri',lbl='Github redirect uri', default='http://localhost:8080/git')
        fb.dataFormula('.token_url', "url+'/authorize?response_type=code&scope=user%20repo%20read:org&client_id='+client_id", 
                            url=auth_api_url, client_id='^.g_client_id')
        fb.a('Get Code', href='^.token_url', target='_blank')
        fb.div('Paste the part of the url after <code=>: "http://0.0.0.0:8080/...?code=****************"')
        fb.textbox('^.b_code', lbl='Github Code')
        fb.button('Get token').dataRpc('.g_access_token', self.getToken, code='=.b_code', 
                                    client_id='=.g_client_id', client_secret='=.g_secret')
        fb.div('^.g_access_token', lbl='Github Access Token')

    @public_method
    def getToken(self, code=None, client_id=None, client_secret=None):
        """Returns access token"""
        token_url=f'{auth_api_url}/access_token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Accept':'application/json'}
        data = {'grant_type':'authorization_code', 'code':f'{code}'}

        r = requests.post(token_url, headers=headers, data=data, auth=(f'{client_id}', f'{client_secret}'))

        if not r.ok:
            print("**Github** Error (getToken) / http code: " + str(r.status_code) + ", body message: " + str(r.content))
        else:
            g_access_token = json.loads(r.text)['access_token'] 
            return g_access_token