from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import select, or_
from sqlalchemy.orm import Session

from .db import Base, engine, get_db
from .models import Card, Sale, ResearchQueue
from .schemas import CardSummary, CardOut, SaleOut, ValueOut

app = FastAPI(title="Card Market API", version="1.0.0")

@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

def card_label(card: Card) -> str:
    extras = []
    if card.parallel:
        extras.append(card.parallel)
    if card.rookie:
        extras.append("Rookie")
    if card.autograph:
        extras.append("Auto")
    return f"{card.year} {card.set_name} #{card.card_number} — {card.player}" + (
        f" ({', '.join(extras)})" if extras else ""
    )

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/cards/search", response_model=list[CardSummary])
def search_cards(q: str, db: Session = Depends(get_db)):
    q = q.strip()
    if not q:
        return []

    terms = [x for x in q.split() if x]
    stmt = select(Card)
    for term in terms:
        pattern = f"%{term}%"
        stmt = stmt.where(or_(
            Card.player.ilike(pattern),
            Card.set_name.ilike(pattern),
            Card.card_number.ilike(pattern),
            Card.parallel.ilike(pattern),
        ))
    cards = db.scalars(stmt.limit(30)).all()
    return [{"id": c.id, "label": card_label(c)} for c in cards]

@app.get("/cards/{card_id}", response_model=CardOut)
def get_card(card_id: int, db: Session = Depends(get_db)):
    card = db.get(Card, card_id)
    if not card:
        raise HTTPException(404, "Card not found")
    return card

@app.get("/cards/{card_id}/sales", response_model=list[SaleOut])
def get_sales(card_id: int, db: Session = Depends(get_db)):
    if not db.get(Card, card_id):
        raise HTTPException(404, "Card not found")
    return db.scalars(
        select(Sale)
        .where(Sale.card_id == card_id)
        .order_by(Sale.sale_date.desc())
        .limit(100)
    ).all()

@app.get("/cards/{card_id}/value", response_model=ValueOut)
def get_value(card_id: int, db: Session = Depends(get_db)):
    if not db.get(Card, card_id):
        raise HTTPException(404, "Card not found")

    sales = db.scalars(
        select(Sale)
        .where(Sale.card_id == card_id, Sale.verified.is_(True))
        .order_by(Sale.sale_date.desc())
        .limit(20)
    ).all()

    if not sales:
        return ValueOut(
            card_id=card_id,
            value=None,
            method="no_data",
            confidence=0,
            explanation="No verified demo transactions are available for this card.",
        )

    latest = float(sales[0].price)
    confidence = 5 if len(sales) >= 5 else max(1, len(sales))
    return ValueOut(
        card_id=card_id,
        value=round(latest, 2),
        method="latest_verified_sale",
        confidence=confidence,
        explanation=(
            f"Demo V1 estimate based on the latest verified transaction "
            f"({sales[0].marketplace}). The production engine can later add "
            f"outlier filtering, time adjustment, indexes and confidence intervals."
        ),
    )

@app.get("/research/queue")
def research_queue(db: Session = Depends(get_db)):
    rows = db.scalars(
        select(ResearchQueue)
        .where(ResearchQueue.status == "pending")
        .order_by(ResearchQueue.priority.desc(), ResearchQueue.id)
    ).all()
    return [
        {
            "id": r.id,
            "sale_id": r.sale_id,
            "priority": r.priority,
            "reason": r.reason,
            "status": r.status,
        }
        for r in rows
    ]

@app.post("/research/queue/{item_id}/decision")
def research_decision(item_id: int, decision: str, db: Session = Depends(get_db)):
    if decision not in {"approve", "reject"}:
        raise HTTPException(400, "decision must be approve or reject")
    item = db.get(ResearchQueue, item_id)
    if not item:
        raise HTTPException(404, "Queue item not found")
    item.status = "approved" if decision == "approve" else "rejected"
    db.commit()
    return {"id": item.id, "status": item.status}
