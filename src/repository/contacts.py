from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from starlette import status

from src.entity.models import Contact, User
from src.schemas.schemas import ContactModel

"""
Отримати список всіх контактів.
"""


async def get_contacts(limit: int, offset: int, db: AsyncSession, current_user: User) -> list[Contact]:
    search = select(Contact).filter_by(user=current_user).offset(offset).limit(limit)
    result = await db.execute(search)
    contact = result.scalars().all()
    return contact  # noqa


"""
Отримати список всіх контактів. all: role
"""


async def get_all_contacts(limit: int, offset: int, db: AsyncSession) -> list[Contact]:
    search = select(Contact).offset(offset).limit(limit)
    result = await db.execute(search)
    contact = result.scalars().all()
    return contact  # noqa


"""
Створити новий контакт.
"""


async def create_contact(body: ContactModel, current_user: User, db: AsyncSession) -> Contact:
    contact = Contact(
        first_name=body.first_name,
        last_name=body.last_name,
        email=body.email,
        contact_number=body.contact_number,
        birth_date=body.birth_date,
        additional_information=body.additional_information,
        user=current_user
    )

    db.add(contact)
    await db.commit()
    await db.refresh(contact)
    return contact


"""
Отримати один контакт за ідентифікатором.
"""


async def get_contact(contact_id: int, current_user: User, db: AsyncSession) -> Contact:
    search = select(Contact).filter_by(id=contact_id, user=current_user)
    result = await db.execute(search)
    contact = result.scalar_one_or_none()
    return contact


"""
Оновити існуючий контакт.
"""


async def update_contact(contact_id: int, body: ContactModel, current_user: User, db: AsyncSession) -> Contact | None:
    search = select(Contact).filter_by(id=contact_id, user=current_user)
    result = await db.execute(search)
    contact = result.scalar_one_or_none()
    if contact:
        contact.first_name = body.first_name
        contact.last_name = body.last_name
        contact.email = body.email
        contact.contact_number = body.contact_number
        contact.birth_date = body.birth_date
        contact.additional_information = body.additional_information
        await db.commit()
        await db.refresh(contact)
    return contact


"""
Видалити контакт.
"""


async def remove_contact(contact_id: int, current_user: User, db: AsyncSession) -> Contact | None:
    search = select(Contact).filter_by(id=contact_id, user=current_user)
    result = await db.execute(search)
    contact = result.scalar_one_or_none()
    if contact:
        await db.delete(contact)
        await db.commit()
    return contact


async def find_contact_by_first_name(contact_first_name: str, current_user: User, db: AsyncSession) -> list[Contact]:
    """
    Пошук контакту за іменем.
    """
    search = select(Contact).filter_by(first_name=contact_first_name, user=current_user)
    result = await db.execute(search)

    try:
        contacts = result.scalars().all()
        if not contacts:
            raise NoResultFound
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contacts  # noqa


async def find_contact_by_last_name(contact_last_name: str, current_user: User, db: AsyncSession) -> list[Contact]:
    """
    Пошук контакту за прізвищем.
    """
    search = select(Contact).filter_by(last_name=contact_last_name, user=current_user)
    result = await db.execute(search)

    try:
        contacts = result.scalars().all()
        if not contacts:
            raise NoResultFound
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contacts  # noqa


async def find_contact_by_email(contact_email: str, current_user: User, db: AsyncSession) -> list[Contact]:
    """
        Пошук контакту за адресою електронної пошти.
    """
    search = select(Contact).filter_by(email=contact_email, user=current_user)
    result = await db.execute(search)

    try:
        contact = result.scalar()
        if not contact:
            raise NoResultFound
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Contact not found")

    return contact  # noqa


"""
API повинен мати змогу отримати список контактів з днями народження на найближчі 7 днів.
"""


async def upcoming_birthdays(current_date, to_date, skip: int, limit: int, current_user: User, db: AsyncSession) -> \
        list[Contact]:
    search = select(Contact).filter_by(user=current_user).offset(skip).limit(limit)
    result = await db.execute(search)
    contacts = result.scalars()

    upcoming = []

    for contact in contacts:

        contact_birthday_month_day = (contact.birth_date.month, contact.birth_date.day)
        current_date_month_day = (current_date.month, current_date.day)
        to_date_month_day = (to_date.month, to_date.day)

        if current_date_month_day < contact_birthday_month_day <= to_date_month_day:
            upcoming.append(contact)

    return upcoming
