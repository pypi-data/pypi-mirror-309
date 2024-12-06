from pydantic import BaseModel
from typing import Union

class Swap(BaseModel):
    from_mint: str
    to_mint: str
    amount: Union[float, None] = None
    amount_int: Union[int, None] = None