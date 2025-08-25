from typing import Union

import httpx
from fastapi import FastAPI

app = FastAPI()


@app.get("/hello")
def hello(order_id: Union[str, None] = None):
    print("hello endpoint is called")

    if order_id is None:
        print("order id is not received")
    else:
        url = f"http://localhost:8000/orders/{order_id}"
        print(f"attempt to send GET request to {url}")
        response = httpx.get(url)
        print("order detail:")
        print(response.json())

    return {"status": "OK"}


@app.get("/world")
def hello():
    print("world endpoint is called")
    return {"status": "OK"}
