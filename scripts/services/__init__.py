from fastapi import APIRouter, Security
from scripts.utils.authorization_util import AuthorizationUtil
"""
All routers are defined here. Each router is a collection of routes that are grouped together.

Once the router is defined, it can be included in the scripts.__init__.py file.

"""

login_router = APIRouter(tags=["Login"], prefix="/login")

user_router = APIRouter(tags=["User"], prefix="/user",dependencies=[Security(AuthorizationUtil())])
