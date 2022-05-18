#!/usr/bin/env pythonw
# -*- coding: utf-8 -*-
#
#  Bitbucket SERVICE FOR GENROPY
#  This service allows to perform connection between Bitbucket Cloud API and Genropy  
#
#  Created by Davide Paci on 2022-05-02
#  Copyright (c) 2022 Softwell. All rights reserved.
#

# --------------------------- BaseWebtool subclass ---------------------------

#Create a Bitbucket OAuth consumer here: https://bitbucket.org/{your-user}/workspace/settings/api
#Bitbucket OAuth: https://developer.atlassian.com/cloud/bitbucket/rest/intro/#authentication

import requests, json
from gnr.core.gnrdecorator import public_method
from gnr.core.gnrbaseservice import GnrBaseService
from gnr.web.gnrbaseclasses import BaseComponent
from gnr.core.gnrbag import Bag 

api_url = 'https://api.bitbucket.org/2.0'
auth_api_url = 'https://bitbucket.org/site/oauth2'

class GnrCustomWebPage(object):
    py_requires='gnrcomponents/externalcall:BaseRpc'

class Main(GnrBaseService):
    def __init__(self, parent, token_parameters=None, b_client_id=None, b_secret=None, **kwargs):
        """Defines initial parameters (b_access_token, b_client_id and b_secret) and 
        API call parameters"""
        self.parent = parent
        self.b_access_token = token_parameters['b_access_token']
        self.b_refresh_token = token_parameters['b_refresh_token']
        self.b_client_id = b_client_id
        self.b_secret = b_secret
    
    @public_method
    def refreshToken(self):
        "Returns new access token if expired"
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = dict(grant_type='refresh_token', refresh_token=self.b_refresh_token)
        r = requests.post(f'{auth_api_url}/access_token', headers=headers, data=data, auth=(f'{self.b_client_id}', f'{self.b_secret}'))
        if not r.ok:
            print("**Bitbucket Client** Error (refreshToken) / http code: " + str(r.status_code) + ", body message: " + str(r.content))
        else:
            print('**Bitbucket Client** Token refreshed: ', r.text)
            b_token = json.loads(r.text)['access_token']
            return b_token    

    @public_method
    def getWorkspaces(self):
        "Returns workspace ID"
        b_token = self.refreshToken()
        headers = {'Authorization': f'Bearer {b_token}', 'Accept': 'application/json'}

        r = requests.get(f'{api_url}/user/permissions/workspaces', headers=headers)
        if not r.ok:
            print("**Bitbucket** Error (getWorkspaces) / http code: " + str(r.status_code) + ", body message: " + str(r.content))
        else:
            result = json.loads(r.text)['values']
            workspaces = Bag()
            workspaces.fromJson(result)
            return workspaces

    @public_method
    def getProjects(self, workspace_slug=None):
        "Get All Bitbucket projects in a workspace"
        b_token = self.refreshToken()
        headers = {'Authorization': f'Bearer {b_token}', 'Accept': 'application/json'}

        r = requests.get(f'{api_url}/repositories/{workspace_slug}', headers=headers)
        if not r.ok:
            print("**Bitbucket** Error (getProjects) / http code: " + str(r.status_code) + ", body message: " + str(r.content))
        else:
            result = json.loads(r.text)['values']
            projects = Bag()
            projects.fromJson(result)
            return projects

#Bitbucket Cloud SERVICE CONFIGURATION PAGE TO INSERT ACCESS TOKEN AND PAGE ID/SECRET
class ServiceParameters(BaseComponent):
    def service_parameters(self,pane,datapath=None,**kwargs):        
        top = pane.borderContainer(region='center')
        cp = top.contentPane(region='top')
        fb = cp.formbuilder(datapath=datapath)
        fb.textbox(value='^.b_client_id',lbl='Bitbucket Client ID')
        fb.textbox(value='^.b_secret',lbl='Bitbucket Client Secret')
        fb.textbox(value='^.b_redirect_uri',lbl='Bitbucket redirect uri', default='http://localhost:8080/bitbucket')
        fb.dataFormula('.token_url', "url+'/authorize?response_type=code&client_id='+client_id", 
                            url=auth_api_url, client_id='^.b_client_id')
        fb.a('Get Code', href='^.token_url', target='_blank')
        fb.div('Paste the part of the url after <code=>: "http://0.0.0.0:8080/...?code=****************"')
        fb.textbox('^.b_code', lbl='Bitbucket Code')
        fb.button('Get token').dataRpc('.token_parameters', self.getToken, code='=.b_code', 
                                    client_id='=.b_client_id', client_secret='=.b_secret')
        fb.div('^.token_parameters.b_access_token', lbl='Bitbucket Access Token')
        fb.div('^.token_parameters.b_refresh_token', lbl='Bitbucket Refresh Token')

    @public_method
    def getToken(self, code=None, client_id=None, client_secret=None):
        """Returns access token"""
        token_url=f'{auth_api_url}/access_token'
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        data = {'grant_type':'authorization_code', 'code':f'{code}'}

        r = requests.post(token_url, headers=headers, data=data, auth=(f'{client_id}', f'{client_secret}'))

        if not r.ok:
            print("**Bitbucket** Error (getToken) / http code: " + str(r.status_code) + ", body message: " + str(r.content))
        else:
            token_parameters = Bag()
            token_parameters.setItem('b_access_token', json.loads(r.text)['access_token'])
            token_parameters.setItem('b_refresh_token', json.loads(r.text)['refresh_token'])
            return token_parameters