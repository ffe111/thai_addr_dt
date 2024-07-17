from typing import Union

from fastapi import APIRouter, FastAPI
from pydantic import BaseModel

from thaiAddressTag.tag import *
from thaiAddressTag.hashmaps import hashmap
from thaiAddressTag.addresses import address_list

# import thaiaddress
import logging

custom_tokenize, checker = initial_nlp_tools(hashmap)

app = FastAPI()

addr_router = APIRouter(prefix="/addr-detect")

# Set up logging
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Text(BaseModel):
    text: str


@addr_router.get("/addr-detect")
def read_root() -> Union[str, int]:
    try:
        return "Welcome to address-check API\nUse path /address-check to check address\nUse path /docs to see API documentation\nUse path /redoc to see API documentation\n"
    except Exception as e:
        logger.error(f"Error in address_check endpoint: {e}")
        raise e

# @addr_router.get("/items/{item_id}")
# def read_item(item_id: int, q: str = None) -> dict:
#     return {"item_id": item_id, "q": q}


# @addr_router.put("/items/{item_id}")
# def update_item(item_id: int, item: Item):
#     return {"item_name": item.name, "item_id": item_id}


@addr_router.post("/addr-detect/address-check")
def address_check(text: Text) -> dict:
    try:
        text = text.text
        res = extract_address(text, custom_tokenize=custom_tokenize,
                              checker=checker, address_list=address_list)
        return {"text": text, "address": res}
    except Exception as e:
        logger.error(f"Error in address_check endpoint: {e}")
        raise e

# @addr_router.post("/address-parser")
# def address_parser(text: Text) -> dict:
#     text = text.text
#     res = thaiaddress.parse(text)
#     return {"address": res}


app.include_router(addr_router)

if __name__ == '__main__':
    import uvicorn
    try:
        uvicorn.run(app, host='0.0.0.0', port=8080, log_level="info")
    except KeyboardInterrupt:
        print("Shutdown server by user")
        logger.error(f"Shutdown server by user")
    except Exception as e:
        print("Shutdown server by error:", e)
        logger.error(f"Shutdown server by error: {e}")
