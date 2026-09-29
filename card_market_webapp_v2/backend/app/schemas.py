from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel

class CardSummary(BaseModel):
    id: int
    label: str

class CardOut(BaseModel):
    id: int
    player: str
    year: int
    set_name: str
    card_number: str
    parallel: str | None
    rookie: bool
    autograph: bool
    memorabilia: bool
    serial_total: int | None

class SaleOut(BaseModel):
    id: int
    sale_date: datetime
    price: Decimal
    marketplace: str
    grade: str | None
    verified: bool
    seller: str | None

class ValueOut(BaseModel):
    card_id: int
    value: float | None
    method: str
    confidence: int
    explanation: str
