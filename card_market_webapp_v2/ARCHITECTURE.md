# Card Market V1 Architecture

Browser
  -> Next.js frontend
  -> FastAPI REST API
  -> PostgreSQL

Core data flow:

source transaction
  -> normalized sale
  -> card identity
  -> research queue
  -> verified sale
  -> valuation
  -> card profile

V1 uses seeded/demo transactions. Production ingestion should use authorized APIs,
licensed feeds, or data supplied by the site owner.

Core entities:
- cards
- sales
- research_queue
- marketplaces

The valuation endpoint is intentionally explainable and small. It is a foundation
for later CLV-style/index-based models rather than a claim to reproduce another
company's private implementation.
