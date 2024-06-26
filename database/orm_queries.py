from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete
from database.models import Products

async def orm_add_product(session: AsyncSession, data: dict):
    session.add(Products(name=data['name'],
                        description=data['description'],
                        price=float(data['price']),
                        image=data['image']))
    await session.commit()  # сохранение данных

async def orm_get_all_products(session: AsyncSession):
    query = select(Products).order_by(Products.id)
    result = await session.execute(query)
    return result.scalars().all()

async def orm_get_product(session: AsyncSession, product_id: int):
    query = select(Products).where(Products.id == product_id)
    result = await session.execute(query)
    return result.scalar()

async def orm_update_product(session: AsyncSession, data: dict, product_id: int):
    query = update(Products).where(Products.id == product_id).values(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image=data['image'])
    await session.execute(query)
    await session.commit()

async  def orm_delete_product(session: AsyncSession, product_id: int):
    query = delete(Products).where(Products.id == product_id)
    await session.execute(query)
    await session.commit()




