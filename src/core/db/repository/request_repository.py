from http import HTTPStatus
from uuid import UUID

from fastapi import Depends, HTTPException
from sqlalchemy import and_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.db.db import get_session
from src.core.db.models import Request
from src.core.db.repository import AbstractRepository


class RequestRepository(AbstractRepository):
    """Репозиторий для работы с моделью Request."""

    def __init__(self, session: AsyncSession = Depends(get_session)) -> None:
        super().__init__(session, Request)

    async def get(self, id: UUID) -> Request:
        request = await self._session.execute(
            select(Request)
            .where(Request.id == id)
            .options(
                selectinload(Request.user),
                selectinload(Request.shift),
            )
        )
        request = request.scalars().first()
        if request is None:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail=f"Объект Request c id={id} не найден.",
            )
        return request

    async def get_by_user_and_shift(self, user_id: UUID, shift_id: UUID) -> Request:
        request = await self._session.execute(
            select(Request).where(Request.user_id == user_id, Request.shift_id == shift_id)
        )
        return request.scalars().first()

    async def add_one_lombaryer(self, request: Request) -> None:
        if not request.numbers_lombaryers:
            request.numbers_lombaryers = 1
        else:
            request.numbers_lombaryers += 1
        await self._session.merge(request)
        await self._session.commit()

    async def get_shift_user_ids(self, shift_id: UUID, status: str = Request.Status.APPROVED.value) -> list[UUID]:
        users_ids = await self._session.execute(
            select(Request.user_id).where(Request.shift_id == shift_id).where(Request.status == status)
        )
        return users_ids.scalars().all()

    async def get_requests_by_users_ids_and_shifts_id(self, users_ids: list[UUID], shift_id: UUID) -> list[Request]:
        """Возвращает список заявок участников.

        Заявки принадлежат участникам с id в списке users_ids, участвующих в смене с id shift_id.

        Аргументы:
            users_ids (list[UUID]): список id участников
            shift_id (UUID): id смены
        """
        statement = (
            select(Request)
            .where(
                and_(
                    Request.user_id.in_(users_ids),
                    Request.shift_id == shift_id,
                    Request.status == Request.Status.APPROVED,
                )
            )
            .options(selectinload(Request.user))
        )
        return (await self._session.scalars(statement)).all()

    async def bulk_excluded_status_update(self, requests: list[Request]) -> None:
        """Массово изменяет статус заявок на excluded.

        Аргументы:
            requests (list[Request]): список заявок участников, подлежащих исключению
        """
        for request in requests:
            request.status = Request.Status.EXCLUDED
            await self._session.merge(request)
        await self._session.commit()
