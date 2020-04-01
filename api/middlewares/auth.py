from flask import current_app
from helpers.token import decode_auth_token

publicSchema = [
    '__schema',
    'loginUser'
]


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        if root is None:
            # This will only be called once for a request
            if info.field_name not in publicSchema:
                print('middleware:auth - schema field: ' + info.field_name)
                # print(info.context.headers.get('Authorization'))
                # print(info.context.headers.get('Accept-Language'))

                auth_resp = decode_auth_token(
                    info.context.headers.get('Authorization'))

                if not isinstance(auth_resp, str):
                    userModel = current_app.db.Model._decl_class_registry.get(
                        'User', None)

                    myUser = userModel.query.get(auth_resp)
                    if not myUser:
                        raise Exception('User not found.')

                    hasPermission = False
                    for perm in myUser.group.permissions:
                        if perm.name == info.field_name:
                            hasPermission = True
                            break

                    if hasPermission == False:
                        raise Exception('Forbidden')

                    kwargs['user'] = myUser
                else:
                    raise Exception('Auth failed.')

        return next(root, info, **kwargs)
