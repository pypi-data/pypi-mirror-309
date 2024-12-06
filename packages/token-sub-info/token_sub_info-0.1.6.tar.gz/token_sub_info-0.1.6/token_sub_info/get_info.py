from uuid import UUID

from .utils import decode_token
from .exceptions import AllOrganizationAccessForbiddenException


def get_organizations(token: str, public_key: bytes, jwt_algorithm: str) -> list[UUID]:
    """
    Decode jwt token and return a list of organization UUIDs from token payload dictionary.

    :param token: jwt token to decode
    :type token: str
    :param public_key: public key used to decode the token
    :type public_key: bytes
    :param jwt_algorithm: jwt algorithm used to decode the token
    :type jwt_algorithm: str
    :returns: a list of organization UUIDs from token payload dictionary
    :rtype: list[UUID]
    """
    payload = decode_token(token, public_key, jwt_algorithm)
    organizations_ids: list[UUID] = payload.get("sub").get("organizations")
    if not organizations_ids:
        raise AllOrganizationAccessForbiddenException
    return organizations_ids
