#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : AI.  @by PyCharm
# @File         : sqlm
# @Time         : 2024/11/18 19:54
# @Author       : betterme
# @WeChat       : meutils
# @Software     : PyCharm
# @Description  : https://github.com/fastapi/sqlmodel/issues/543

# 协程 https://github.com/deshetti/sqlmodel-async-example/blob/e412da00f557a352ee3f66a8545ef11401ea5dde/main.py#L42-L47
# https://github.com/deshetti/sqlmodel-async-example/blob/main/main.py
from meutils.pipe import *

from typing import Optional

from sqlmodel import Field, Session, SQLModel, create_engine, select
from sqlmodel.ext.asyncio.session import AsyncSession  # 有点难

from sqlalchemy.ext.asyncio import create_async_engine


class Hero(SQLModel, table=True):
    __table_args__ = {'extend_existing': True}  # includes this line

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: Optional[int] = None


hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
hero_2 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
hero_3 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)

# engine = create_engine("sqlite:///database.db")
#
#
# SQLModel.metadata.create_all(engine)
#
# with Session(engine) as session:
#     session.add(hero_1)
#     session.add(hero_2)
#     session.add(hero_3)
#     session.commit()


if __name__ == '__main__':
    from typing import Optional

    from sqlmodel import Field, Session, SQLModel, create_engine, select

    engine = create_engine("sqlite:///database.db")

    with Session(engine) as session:
        statement = select(Hero).where(Hero.name == "Spider-Boy")
        hero = session.exec(statement).first()
        print(hero)

    aengine = create_async_engine("sqlite+aiosqlite:///:memory:")


    async def main():
        async with AsyncSession(aengine) as session:
            statement = select(Hero).where(Hero.name == "Spider-Boy")
            hero = await session.exec(statement)
            hero = hero.first()
            print(hero)


    arun(main())
