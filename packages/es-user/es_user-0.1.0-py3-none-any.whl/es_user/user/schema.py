"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from datetime import datetime
from pydantic import BaseModel, EmailStr, field_validator
from es_user.util.enums import AccessRoleEnum, StatusEnum
from typing import Literal
gender_type = Literal['MALE', 'FEMALE', 'OTHER']
class AddressBase(BaseModel):
    street: str
    city: str
    state: str
    zip_code: str | None = None
    email: EmailStr | None = None
    phone_number: str | None = None
    country: str
class AddressDto(AddressBase):
    id: int | None = None
class UserEmail(BaseModel):
    email: EmailStr
class UserReset(UserEmail):
    token: str
    password: str
    new_password: str | None = None
class UserPhoto(BaseModel):
    file_path: str
    user_id: int
class UserBase(BaseModel):
    first_name: str
    last_name: str
    is_active: bool = False
    roles: list[AccessRoleEnum]
    socialmedia: str | None = None # comma separated string
    gender: gender_type
    token: str | None = None
    email: EmailStr
    status: StatusEnum = StatusEnum.NEW

class UserResponse(UserBase):
    id: int
    dp: str | None = None
    created_at: datetime = datetime.now()

    @field_validator('roles')
    def validate_roles(cls, roles):
        if AccessRoleEnum.GUEST in roles and AccessRoleEnum.ADMIN in roles:
            raise ValueError("User cannot have roles of Guest and Admin at the same time")
        return roles

class AppuserDto(UserBase):
    password: str
    address: AddressBase | None = None

class AppuserUpdate(UserBase):
    id: int  
    address: AddressDto | None = None 
    @field_validator('roles')
    def validate_roles(cls, roles):
        if AccessRoleEnum.GUEST in roles and AccessRoleEnum.ADMIN in roles:
            raise ValueError("User cannot have roles of Guest and Admin at the same time")
        return roles