from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from redis_om import get_redis_connection, HashModel

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:3000'],
    allow_methods=['*'],
    allow_headers=['*']
)

redis = get_redis_connection(
    host="redis-12486.c290.ap-northeast-1-2.ec2.cloud.redislabs.com",
    port=12486,
    password="HX77P42mXD11gDkDDNc8qta7f0olagJU",
    decode_responses=True
)


class Product(HashModel):
    name: str
    price: float
    quantity: int

    class Meta:
        database = redis


@app.get('/products')
async def all():
    return [format(pk) for pk in Product.all_pks()]


def format(pk: str):
    product = Product.get(pk)
    return {
        "id": product.pk,
        "name": product.name,
        "price": product.price,
        "quantity": product.quantity
    }


@app.post('/products')
async def create(products: Product):
    return products.save()


@app.get('/products/{pk}')
async def get(pk: str):
    return Product.get(pk)


@app.delete('/products/{pk}')
async def delete(pk: str):
    return Product.delete(pk)
