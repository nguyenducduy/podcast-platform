from flask import current_app
from helpers.token import decode_auth_token


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **kwargs):
        if root is None:
            # This will only be called once for a request
            print('middleware:auth - schema field: ' + info.field_name)

            if info.field_name != 'loginUser':
                # print(info.context.headers.get('Authorization'))
                # print(info.context.headers.get('Accept-Language'))

                auth_resp = decode_auth_token(
                    info.context.headers.get('Authorization'))

                if not isinstance(auth_resp, str):
                    userModel = current_app.db.Model._decl_class_registry.get(
                        'User', None)

                    myUser = userModel.query.filter_by(
                        id=auth_resp).first()

                    # hasPermission = False
                    # for perm in myUser.group.permissions:
                    #     if perm.name == info.field_name:
                    #         hasPermission = True
                    #         break

                    # if hasPermission == False:
                    #     raise Exception('Forbidden')

                    kwargs['user'] = myUser
                else:
                    raise Exception(auth_resp)

        return next(root, info, **kwargs)
