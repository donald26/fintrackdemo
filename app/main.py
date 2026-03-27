from datetime import date
from enum import Enum
from fastapi import FastAPI
from pydantic import BaseModel, Field, validator

app = FastAPI(title="FinTrack Demo API")

# In-memory store
TRANSACTIONS = {}
TRANSACTION_ID_SEQ = 1


class TransactionType(str, Enum):
    income = "income"
    expense = "expense"


class TransactionCreate(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be positive")
    type: TransactionType
    category: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    date: date

    @validator("category", "description")
    def not_blank(cls, v: str) -> str:
        if not v.strip():
            raise ValueError("must not be blank")
        return v.strip()


class Transaction(TransactionCreate):
    id: int


@app.post("/transactions", status_code=201, response_model=Transaction)
def create_transaction(transaction: TransactionCreate):
    global TRANSACTION_ID_SEQ
    txn_id = TRANSACTION_ID_SEQ
    TRANSACTION_ID_SEQ += 1

    new_txn = Transaction(id=txn_id, **transaction.dict())
    TRANSACTIONS[txn_id] = new_txn
    return new_txn
