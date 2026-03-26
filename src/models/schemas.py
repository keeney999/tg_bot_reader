from pydantic import BaseModel
from typing import List

class ScanResult(BaseModel):
    user_id: int
    username: str
    order_numbers: List[str]
    barcodes: List[str]
    message_link: str