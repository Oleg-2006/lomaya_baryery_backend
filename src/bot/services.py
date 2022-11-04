from src.bot.main import create_bot
from src.core.db import models
from src.core.settings import ORGANIZATIONS_EMAIL, ORGANIZATIONS_GROUP, settings

bot = create_bot().bot  # временная копия бота до миграции на webhooks


async def send_approval_callback(user: models.User):
    await bot.send_message(
        chat_id=user.telegram_id, text=(f"Привет, {user.name} {user.surname}! Поздравляем, ты в проекте!")
    )


async def send_rejection_callback(user: models.User):
    await bot.send_message(
        chat_id=user.telegram_id,
        text=(
            f"К сожалению, на данный момент мы не можем зарегистрировать вас"
            f" в проекте. Вы можете написать на почту "
            f"{ORGANIZATIONS_EMAIL}. Чтобы не пропустить актуальные"
            f" новости Центра \"Ломая барьеры\" - вступайте в нашу группу "
            f"{ORGANIZATIONS_GROUP}"
        ),
    )


async def send_blocking_callback(user: models.User) -> None:
    await bot.send_message(
        chat_id=user.telegram_id,
        text=(
            "К сожалению, мы заблокировали Ваше участие в смене из-за неактивности - "
            f"Вы не отправили ни одного отчета на последние {settings.SEQUENTIAL_TASKS_PASSES_FOR_BLOCKING} заданий."
            " Вы не сможете получать новые задания, но всё еще можете потратить свои накопленные ломбарьерчики. "
            "Если Вы считаете, что произошла ошибка - обращайтесь "
            f"за помощью на электронную почту {ORGANIZATIONS_EMAIL}."
        ),
    )
