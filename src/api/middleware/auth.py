import pprint


class AuthorizationMiddleware(object):
    def resolve(self, next, root, info, **args):
        if root is None:
            pp = pprint.PrettyPrinter(indent=4)

            print('hello middleware')
            # This will only be called once for a request

            print(info.field_name)
            # print(info.context.headers.get('Authorization'))
        # if info.field_name == 'user':
        #     return None
        return next(root, info, **args)
