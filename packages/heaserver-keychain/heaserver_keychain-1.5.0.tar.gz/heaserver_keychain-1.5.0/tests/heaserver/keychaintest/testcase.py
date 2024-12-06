"""
Creates a test case class for use with the unittest library that is built into Python.
"""

from heaserver.service.testcase.microservicetestcase import get_test_case_cls_default
from heaserver.keychain import service
from heaobject.user import NONE_USER
from heaserver.service.testcase.expectedvalues import Action

credentials_db_store = {
    service.MONGODB_CREDENTIALS_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'instance_id': 'heaobject.keychain.Credentials^666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': NONE_USER,
        'shares': [],
        'source': None,
        'source_detail': None,
        'type': 'heaobject.keychain.Credentials',
        'created': None,
        'account': None,
        'where': None,
        'password': None,
        'type_display_name': 'Credentials',
        'role': None,
        'expiration': None,
        'lifespan': 'LONG_LIVED'
    },
        {
            'id': '0123456789ab0123456789ab',
            'instance_id': 'heaobject.keychain.Credentials^0123456789ab0123456789ab',
            'created': None,
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Luximus',
            'invites': [],
            'modified': None,
            'name': 'luximus',
            'owner': NONE_USER,
            'shares': [],
            'source': None,
            'source_detail': None,
            'type': 'heaobject.keychain.Credentials',
            'account': None,
            'created': None,
            'where': None,
            'password': None,
            'type_display_name': 'Credentials',
            'role': None,
            'expiration': None,
            'lifespan': 'LONG_LIVED'
        }]}

CredentialsTestCase = get_test_case_cls_default(coll=service.MONGODB_CREDENTIALS_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/credentials/',
                                     fixtures=credentials_db_store,
                                     get_actions=[Action(name='heaserver-keychain-credentials-get-properties',
                                                             rel=['hea-context-menu', 'hea-properties']),
                                                  Action(name='heaserver-keychain-credentials-get-self',
                                                             url='http://localhost:8080/credentials/{id}',
                                                             rel=['self'])
                                                  ],
                                     get_all_actions=[Action(name='heaserver-keychain-credentials-get-properties',
                                                             rel=['hea-context-menu', 'hea-properties']),
                                                      Action(name='heaserver-keychain-credentials-get-self',
                                                                 url='http://localhost:8080/credentials/{id}',
                                                                 rel=['self'])]
                                     )


aws_credentials_db_store = {
    service.MONGODB_CREDENTIALS_COLLECTION: [{
        'id': '666f6f2d6261722d71757578',
        'instance_id': 'heaobject.keychain.AWSCredentials^666f6f2d6261722d71757578',
        'created': None,
        'derived_by': None,
        'derived_from': [],
        'description': None,
        'display_name': 'Reximus',
        'invites': [],
        'modified': None,
        'name': 'reximus',
        'owner': NONE_USER,
        'shares': [],
        'source': None,
        'source_detail': None,
        'type': 'heaobject.keychain.AWSCredentials',
        'created': None,
        'account': None,
        'where': None,
        'password': None,
        'type_display_name': 'AWS Credentials',
        'role': None,
        'expiration': None,
        'lifespan': 'LONG_LIVED'
    },
        {
            'id': '0123456789ab0123456789ab',
            'instance_id': 'heaobject.keychain.AWSCredentials^0123456789ab0123456789ab',
            'created': None,
            'derived_by': None,
            'derived_from': [],
            'description': None,
            'display_name': 'Luximus',
            'invites': [],
            'modified': None,
            'name': 'luximus',
            'owner': NONE_USER,
            'shares': [],
            'source': None,
            'source_detail': None,
            'type': 'heaobject.keychain.AWSCredentials',
            'account': None,
            'created': None,
            'where': None,
            'password': None,
            'type_display_name': 'AWS Credentials',
            'role': None,
            'expiration': None,
            'lifespan': 'LONG_LIVED'
        }]}

AWSCredentialsTestCase = get_test_case_cls_default(coll=service.MONGODB_CREDENTIALS_COLLECTION,
                                     wstl_package=service.__package__,
                                     href='http://localhost:8080/awscredentials/',
                                     fixtures=aws_credentials_db_store,
                                     get_actions=[Action(name='heaserver-keychain-awscredentials-get-properties',
                                                             rel=['hea-context-menu', 'hea-properties']),
                                                  Action(name='heaserver-keychain-credentials-get-self',
                                                             url='http://localhost:8080/awscredentials/{id}',
                                                             rel=['self']),
                                                  Action(name='heaserver-keychain-awscredentials-get-cli-credentials-file',
                                                             url='http://localhost:8080/awscredentials/{id}/awsclicredentialsfile',
                                                             rel=['hea-dynamic-clipboard', 'hea-retrieve-clipboard-icon', 'hea-context-menu']),
                                                  Action(name='heaserver-keychain-get-generate-awscredential',
                                                         url='http://localhost:8080/awscredentials/{id}/managedawscredential',
                                                         rel=['hea-dynamic-clipboard', 'hea-generate-clipboard-icon', 'hea-context-menu'])
                                                  ],
                                     get_all_actions=[Action(name='heaserver-keychain-awscredentials-get-properties',
                                                             rel=['hea-context-menu', 'hea-properties']),
                                                      Action(name='heaserver-keychain-credentials-get-self',
                                                                 url='http://localhost:8080/awscredentials/{id}',
                                                                 rel=['self']),
                                                      Action(name='heaserver-keychain-awscredentials-get-cli-credentials-file',
                                                             url='http://localhost:8080/awscredentials/{id}/awsclicredentialsfile',
                                                             rel=['hea-dynamic-clipboard', 'hea-retrieve-clipboard-icon', 'hea-context-menu']),
                                                      Action(name='heaserver-keychain-get-generate-awscredential',
                                                             url='http://localhost:8080/awscredentials/{id}/managedawscredential',
                                                             rel=['hea-dynamic-clipboard', 'hea-generate-clipboard-icon', 'hea-context-menu'])]
                                     )
