"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from sqlalchemy import desc
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from pydantic import EmailStr   
from es_user.user.model import Appuser, Address
from es_user.user.schema import AppuserDto, UserResponse, AppuserUpdate, UserReset, AddressDto
from es_user.util.service import encrypt_pass, verify_password
from es_user.util.enums import AccessRoleEnum, StatusEnum
from es_user.db import pg
import logging
import uuid

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_admin(db: Session, password: str, email: str) -> Appuser | None:
    """Create admin user if it does not exist.
        Args:
            db (Session): Database session.
            password (str): Admin password.
            email (str): Admin email.
    """
    user = db.query(Appuser).filter(Appuser.email == "office@horacelearning.com").first()
    if user:
        logger.info("Horace Admin user already exists")
        return
    new_admin = AppuserDto(
        first_name="Horace",
        last_name="Admin",
        email=email,
        token="Horace@123",
        password=encrypt_pass(password),
        status=StatusEnum.NEW,
        is_active=True,
        gender="MALE",
        roles=[AccessRoleEnum.ADMIN],
    )
    pg.add_model(Appuser, db, **new_admin.__dict__)
async def add_user(user: AppuserDto, db: Session) -> UserResponse:
    try:
        new_user = None
        if user.address:
            addr = pg.add_model(Address, db, **user.address.__dict__)
            user.address = addr
            new_user = pg.add_model(Appuser, db, **user.__dict__)

        if new_user:
            return UserResponse(**new_user.__dict__)
        else:
            raise ValueError("Failed to add new user.")
    except IntegrityError as e:
        if "duplicate key value violates unique constraint" in str(e.orig):
            logger.error(f"Error adding user: {e}")
            raise ValueError(f"Email already exists. {user.email}")
        else:
            logger.error(f"Error adding user: {e}")
            raise ValueError("An error occurred.")
    except SQLAlchemyError as e:
        logger.error(f"Error adding user: {e}")
        raise ValueError(
            "Database error.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError(f"Unexpected error.{e}")

# def bulk_upload_users(contents: bytes, file_type: str, db: Session) -> int:
#     """
#     Uploads user data from a CSV or JSON file.

#     Args:
#         file (IO): The file object of the CSV or JSON file.
#         file_type (str): "csv" or "json".
#         db (Session): The database session object.

#     Returns:
#         int: The number of users successfully uploaded.
#     """
#     uploaded_count = 0

#     try:
#         if file_type == "csv":
#             data = read_csv(io.BytesIO(contents), converters={"roles": lambda x: x.split(",")})
#             # 
#             # records = data.to_dict(orient='records')
#         elif file_type == "json":
#             data = read_json(io.BytesIO(contents))
#             # records = data.to_dict(orient='records')
#         else:
#             raise ValueError("Invalid file type. Supported types: csv, json")
#         data["password"] = data["password"].apply(encrypt_pass)
#         data["status"] = StatusEnum.NEW 
#         records = data.to_dict(orient='records')
#         user_dtos = [AppuserDto(**row) for row in records]

#         db.bulk_insert_mappings(Appuser, [user_dto.__dict__ for user_dto in user_dtos])
#         db.commit()
#         uploaded_count = len(records)

#     except ValueError as ve:
#         raise ve
#     except (csv.Error, json.JSONDecodeError) as file_error:
#         raise Exception(f"Error reading the file: {file_error}")
#     except Exception as e:
#         db.rollback()
#         raise Exception(f"Error processing user data: {e}")

#     return uploaded_count

def get_user_by_id(usr: int, db: Session) -> UserResponse:
    try:
        user = pg.get_model(Appuser, db, usr)
        if not user:
            raise ValueError(f"No user with id {usr}")
        return UserResponse(**user.__dict__)
    except Exception as e:
        logger.error(f"Get user by id failed {str(e)}")
        raise ValueError(f"Error getting User {usr}")
def activate_user(email: str, db: Session) -> bool:
    try:
        user = db.query(Appuser).filter(Appuser.email == email).first()
        if not user:
            raise ValueError(f"No user with email {email}")
        user.is_active = not user.is_active
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error activating user {email}: {str(e)}")
        raise ValueError(f"Error activating user {email}: {str(e)}")
def update_user(user_update: AppuserUpdate, db: Session) -> UserResponse:
    try:
        existing_user = db.query(Appuser).get(user_update.id)
        if not existing_user:
            raise ValueError(f"User not found. {user_update.id}")
        
        # Update the address if provided
        if user_update.address:
            if existing_user.address_id:
                addr = db.query(Address).get(existing_user.address_id)
                for key, value in user_update.address.__dict__.items():
                    setattr(addr, key, value)
                addr.id = existing_user.address_id
                db.commit()
                db.refresh(addr)
            else:
                addr = Address(**user_update.address.__dict__)
                db.add(addr)
                db.commit()
                db.refresh(addr)
                existing_user.address_id = addr.id

        # Update the user details
        for key, value in user_update.__dict__.items():
            if key != 'address' and key != 'id':
                setattr(existing_user, key, value)
        db.commit()
        db.refresh(existing_user)

        logger.info(f"User {existing_user.email} updated successfully")
        return UserResponse(**existing_user.__dict__)
        
    except IntegrityError as e:
        db.rollback()
        if "duplicate key value violates unique constraint" in str(e.orig):
            logger.error(f"Error updating user: {e}")
            raise ValueError(f"Email already exists: {user_update.email}")
        else:
            logger.error(f"Integrity error updating user: {e}")
            raise ValueError("An error occurred during data integrity validation.")
    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error updating user: {e}")
        raise ValueError("Database error.")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        raise ValueError(f"Unexpected error: {e}")

def update_photo(user_id: int, photo: str, db: Session) -> bool:
    try:
        user = db.query(Appuser).get(user_id)
        user.dp = photo
        db.commit()
        return True
    except Exception as e:
        raise e
    
def get_userby_username(email: str,db:Session) -> Appuser:
    user = db.query(Appuser).filter(Appuser.email == email).first()
    return user


def all_users(db: Session) -> list[UserResponse]:
    try:
        users = pg.get_all_models(Appuser, db)
        users_resp = [
            UserResponse(
                **user.__dict__
            )
            for user in users
        ]
        return users_resp
    except SQLAlchemyError as e:
        logger.error(f"Database error retrieving all users: {e}")
        raise ValueError("Database error.")
    except Exception as e:
        logger.error(f"Unexpected error retrieving all users: {e}")
        raise ValueError("Unexpected error.")
def delete_user(db: Session, id: int) -> bool:
    try:
        user = db.query(Appuser).get(id)
        if user is None:
            raise ValueError(f"User with id {id} not found.")
        db.delete(user)
        db.commit()
        return True
    except Exception as e:
        raise ValueError(f"An error occurred. {e}")
def set_delete_user(db: Session, id: int) -> bool:
    try:
        user = db.query(Appuser).get(id)
        if user is None:
            raise ValueError(f"User with id {id} not found.")
        
        user.status = StatusEnum.DELETED
        db.commit()
        return True
        
    except Exception as e:
        db.rollback()  # Rollback in case of an error
        logger.error(f"Error deleting user with id {id}: {e}")
        raise ValueError(f"An error occurred deleting user with id {id}.")


def users_by_role(db: Session, role: AccessRoleEnum) -> list[UserResponse]:
    """
    Retrieve users based on their role.

    Args:
        db (Session): Database session.
        role (str): Role to filter users.

    Returns:
        List[UserResponse]: List of users matching the specified role.
    """
    users = db.query(Appuser).filter(Appuser.roles.contains([role])).order_by(desc(Appuser.id)).all()
    users_resp = [
        UserResponse(
            id=user.id,
            timestamp=user.timestamp,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email,
            password=user.password,
            is_active=user.is_active,
            roles=user.roles,
            gender=user.gender,
            socialmedia=user.socialmedia
        )
        for user in users
    ]
    return users_resp


def is_exist(email: EmailStr, db: Session) -> int:
    user = db.query(Appuser).filter(Appuser.email == email).first()
    return user.id if user else 0

async def rest_password_token(email: str, db: Session) -> Appuser | None:
    try:
        user = db.query(Appuser).filter(Appuser.email == email).first()
        if not user:
            raise ValueError(f"No user with email {email}")
        token = str(uuid.uuid4())[:8]
        user.token = token
        db.commit()
        # mailer=MailerDto(
        #         recipients=[email],
        #         subject="Password Reset",
        #         message=f"Your password reset token is {token}",
        #         create_at=datetime.now(),
        #         is_html=False
        #     )
        # asyncio.create_task(send_email_sendgrid(mailer))
        # logger.info("Password reset token %s sent to %s", token, email)
        return user
    except Exception as e:
        db.rollback()
        logger.error(f"Error resetting password for {email}: {str(e)}")
def reset_password(reset: UserReset, db: Session) -> bool:
    try:
        email = reset.email
        user = db.query(Appuser).filter(
            (Appuser.email == email) & (Appuser.token == reset.token)
            ).first()
        logger.info("compare %s and ",user.token, reset.token)
        if not user:
            raise ValueError(f"No user with email {email} or token {reset.token}")
        user.password = encrypt_pass(reset.password)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error resetting password for: {str(e)}")
        return False
def manual_change_password(user: UserReset, db: Session) -> bool:
    try:
        exist_user = db.query(Appuser).filter(Appuser.email == user.email).first()
        if not exist_user:
            raise ValueError(f"No user with email {user.email}")
        if not verify_password(user.password, exist_user.password):
            raise ValueError("Incorrect username or password") from None
        if user.new_password is None:
            raise ValueError("New password cannot be None")
        exist_user.password = encrypt_pass(user.new_password)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        logger.error(f"Error resetting password for {user.email}: {str(e)}")
        return False
def create_address(address: AddressDto, db: Session) -> bool:
    address = pg.add_model(Address,db, **address.model_dump())
    return address