import graphene


class CommonDictType(graphene.ObjectType):
    text = graphene.String()
    value = graphene.String()
    color = graphene.String()
