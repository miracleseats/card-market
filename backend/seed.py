from datetime import datetime, timedelta
from decimal import Decimal
from app.db import Base, engine, SessionLocal
from app.models import Card, Sale, ResearchQueue

# Run from backend with:
# python -m seed
# or: python seed.py

Base.metadata.create_all(bind=engine)
db = SessionLocal()

if db.query(Card).count() == 0:
    cards = [
        Card(player="Kobe Bryant", year=1996, set_name="Topps Chrome", card_number="138", rookie=True),
        Card(player="Michael Jordan", year=1986, set_name="Fleer", card_number="57", rookie=True),
        Card(player="Shohei Ohtani", year=2018, set_name="Topps Chrome", card_number="150", rookie=True),
        Card(player="Luka Doncic", year=2018, set_name="Prizm", card_number="280", rookie=True, parallel="Silver"),
        Card(player="Pokémon", year=1999, set_name="Base Set", card_number="4", parallel="Charizard Holo"),
    ]
    db.add_all(cards)
    db.flush()

    now = datetime.utcnow()
    prices = {
        cards[0].id: [725, 710, 700, 680, 655],
        cards[1].id: [4200, 4050, 3900, 4150],
        cards[2].id: [950, 910, 875, 990],
        cards[3].id: [1875, 1800, 1740, 1690, 1825],
        cards[4].id: [310, 295, 330, 305],
    }

    marketplaces = ["eBay", "Goldin", "Heritage", "PWCC", "MySlabs"]
    for card_id, vals in prices.items():
        for i, price in enumerate(vals):
            db.add(Sale(
                card_id=card_id,
                sale_date=now - timedelta(days=i * 12 + 2),
                price=Decimal(str(price)),
                marketplace=marketplaces[i % len(marketplaces)],
                grade="PSA 10",
                verified=True,
                seller=f"demo_seller_{i+1}",
            ))

    db.flush()

    # One pending item demonstrates the researcher workflow.
    sale = db.query(Sale).filter(Sale.card_id == cards[0].id).first()
    db.add(ResearchQueue(
        sale_id=sale.id,
        priority=80,
        reason="Demo transaction awaiting human verification",
        status="pending",
    ))
    db.commit()

db.close()
print("Seed complete.")

