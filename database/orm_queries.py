from sqlalchemy.ext.asyncio import AsyncSession
from database.models import Product

async def orm_add_product(session: AsyncSession, data: dict):
    session.add(Product(name=data['name'],
                        description=data['description'],
                        price=float(data['price']),
                        image=data['image']))
    await session.commit()  # сохранение данных