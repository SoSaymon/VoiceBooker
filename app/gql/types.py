from graphene import ObjectType, Int, String, Boolean, DateTime


class UserObject(ObjectType):
    id = Int()
    username = String()
    email = String()
    full_name = String()
    is_active = Boolean()
    is_admin = Boolean()
    created_at = DateTime()
    last_login = DateTime()
