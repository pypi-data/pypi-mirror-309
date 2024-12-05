"""Copyright 2024 Everlasting Systems and Solutions LLC (www.myeverlasting.net).
All Rights Reserved.

No part of this software or any of its contents may be reproduced, copied, modified or adapted, without the prior written consent of the author, unless otherwise indicated for stand-alone materials.

For permission requests, write to the publisher at the email address below:
office@myeverlasting.net

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
import logging
from sqlalchemy.orm import Session
from es_user.contact.schema import LeadDto,LeadBase
from es_user.contact.model import Lead
from es_user.db import pg
from datetime import datetime
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def make_contact_form(lead: LeadBase,db: Session) -> LeadDto:
    """Submits a contact form.
    Args:
        lead (LeadDto): Lead form content.
        db (Session): Database session.
    """
    try:
        new_lead = pg.add_model(Lead,db, **lead.model_dump())
    except Exception as e:
        raise e
    return LeadDto(**new_lead.__dict__)
def all_leads(db: Session) -> list[LeadDto]:
    leads = db.query(Lead).all()
    return [LeadDto(**lead.__dict__) for lead in leads]
def leads_by_created(start_date: datetime, end_date: datetime, db: Session) -> list[LeadDto]:
    leads = db.query(Lead).filter(Lead.created_at >= start_date, Lead.created_at <= end_date).all()
    return [LeadDto(**lead.__dict__) for lead in leads]