"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from sqlalchemy.sql.sqltypes import Integer,String
from es_user.db.session import Base
class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    created_at = Column(DateTime(), server_default=func.now())
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String, nullable=False)
    phone_number = Column(String)
    country = Column(String)
    subject = Column(String)
    message = Column(String)
    created_at = Column(DateTime(), server_default=func.now())
    updated_at = Column(DateTime(), server_default=func.now(), onupdate=func.now())