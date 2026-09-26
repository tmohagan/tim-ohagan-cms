from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.database import get_db
from app.models.sql_models import ContactMessage
from app.schemas.pydantic_schemas import ContactMessageCreate, ContactMessageResponse

router = APIRouter()

@router.post("/", response_model=ContactMessageResponse, status_code=status.HTTP_201_CREATED)
async def submit_contact_message(message_in: ContactMessageCreate, db: AsyncSession = Depends(get_db)):
    """
    Submit a new contact message that gets saved to the database.
    """
    try:
        new_message = ContactMessage(
            name=message_in.name,
            email=message_in.email,
            message=message_in.message
        )
        db.add(new_message)
        await db.commit()
        await db.refresh(new_message)
        return new_message
    except Exception as e:
        await db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/", response_model=list[ContactMessageResponse])
async def get_contact_messages(skip: int = 0, limit: int = 50, db: AsyncSession = Depends(get_db)):
    """
    Retrieve contact messages.
    """
    query = select(ContactMessage).offset(skip).limit(limit).order_by(ContactMessage.created_at.desc())
    result = await db.execute(query)
    messages = result.scalars().all()
    return messages
