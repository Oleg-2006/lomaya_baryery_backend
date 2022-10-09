from http import HTTPStatus
from typing import Optional
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.db.db import get_session
from src.core.db.models import Shift
from src.core.db.repository.abstract_repository import AbstractRepository

SHIFT_NOT_FOUND = "Такая смена не найдена, проверьте id."


class ShiftRepository(AbstractRepository):
    """Репозиторий для работы с моделью Shift."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        self.session = session

    async def get_or_none(self, id: UUID) -> Optional[Shift]:
        return await self.session.get(Shift, id)

    async def get(self, id: UUID) -> Shift:
        shift = await self.get_or_none(id)
        if shift is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail=SHIFT_NOT_FOUND)
        return shift

    async def create(self, shift: Shift) -> Shift:
        self.session.add(shift)
        await self.session.commit()
        await self.session.refresh(shift)
        return shift

    async def update(self, id: UUID, shift: Shift) -> Shift:
        shift.id = id
        shift = await self.session.merge(shift)
        await self.session.commit()
        return shift

    async def get_with_users(self, id: UUID) -> Shift:
        statement = select(Shift).where(Shift.id == id).options(selectinload(Shift.users))
        request = await self.session.execute(statement)
        request = request.scalars().first()
        if request is None:
            raise HTTPException(status_code=HTTPStatus.NOT_FOUND)
        return request
