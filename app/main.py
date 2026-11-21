from datetime import datetime, date
from pathlib import Path
import re

from fastapi import Depends, FastAPI, HTTPException, Query
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from sqlalchemy import DateTime, Float, ForeignKey, Integer, String, create_engine, func, or_, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column, relationship, sessionmaker

BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR / 'retail.db'}"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


class Base(DeclarativeBase):
    pass


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(120), index=True)
    category: Mapped[str] = mapped_column(String(80), index=True)
    barcode: Mapped[str | None] = mapped_column(String(80), unique=True, nullable=True)
    price: Mapped[float] = mapped_column(Float)
    stock: Mapped[int] = mapped_column(Integer, default=0)
    low_stock_threshold: Mapped[int] = mapped_column(Integer, default=5)


class Transaction(Base):
    __tablename__ = "transactions"
    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    total: Mapped[float] = mapped_column(Float)
    items: Mapped[list["TransactionItem"]] = relationship(cascade="all, delete-orphan")


class TransactionItem(Base):
    __tablename__ = "transaction_items"
    id: Mapped[int] = mapped_column(primary_key=True)
    transaction_id: Mapped[int] = mapped_column(ForeignKey("transactions.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    product_name: Mapped[str] = mapped_column(String(120))
    quantity: Mapped[int] = mapped_column(Integer)
    unit_price: Mapped[float] = mapped_column(Float)


Base.metadata.create_all(engine)


def seed():
    with SessionLocal() as db:
        if db.scalar(select(Product.id)):
            return
        products = [
            Product(name="Dairy Milk Chocolate", category="Chocolates", price=40, stock=24, barcode="890123400001"),
            Product(name="KitKat Chocolate", category="Chocolates", price=30, stock=18, barcode="890123400002"),
            Product(name="Classic Salted Chips", category="Snacks", price=20, stock=30, barcode="890123400003"),
            Product(name="Orange Juice 1L", category="Beverages", price=110, stock=8, barcode="890123400004"),
            Product(name="Mineral Water 1L", category="Beverages", price=20, stock=40, barcode="890123400005"),
            Product(name="Premium Whisky 750ml", category="Liquor", price=1250, stock=4, barcode="890123400006", low_stock_threshold=5),
        ]
        db.add_all(products)
        db.commit()


seed()
app = FastAPI(title="Samita Retail MVP", version="0.1.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")


def db_session():
    with SessionLocal() as db:
        yield db


class ProductIn(BaseModel):
    name: str = Field(min_length=1)
    category: str = Field(min_length=1)
    price: float = Field(gt=0)
    stock: int = Field(ge=0)
    low_stock_threshold: int = Field(default=5, ge=0)
    barcode: str | None = None


class CartItem(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)


class CheckoutIn(BaseModel):
    items: list[CartItem] = Field(min_length=1)


def product_out(p: Product):
    return {"id": p.id, "name": p.name, "category": p.category, "price": p.price, "stock": p.stock,
            "low_stock": p.stock <= p.low_stock_threshold, "low_stock_threshold": p.low_stock_threshold, "barcode": p.barcode}


@app.get("/")
def home():
    return FileResponse(BASE_DIR / "static" / "index.html")


@app.get("/api/products")
def products(search: str = Query(""), db: Session = Depends(db_session)):
    q = select(Product).order_by(Product.name)
    if search.strip():
        term = f"%{search.strip()}%"
        q = q.where(or_(Product.name.ilike(term), Product.category.ilike(term), Product.barcode.ilike(term)))
    return [product_out(p) for p in db.scalars(q).all()]


@app.post("/api/products")
def add_product(payload: ProductIn, db: Session = Depends(db_session)):
    p = Product(**payload.model_dump())
    db.add(p); db.commit(); db.refresh(p)
    return product_out(p)


@app.put("/api/products/{product_id}")
def update_product(product_id: int, payload: ProductIn, db: Session = Depends(db_session)):
    p = db.get(Product, product_id)
    if not p: raise HTTPException(404, "Product not found")
    for key, value in payload.model_dump().items(): setattr(p, key, value)
    db.commit(); return product_out(p)


@app.delete("/api/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(db_session)):
    p = db.get(Product, product_id)
    if not p: raise HTTPException(404, "Product not found")
    db.delete(p); db.commit(); return {"ok": True}


@app.post("/api/checkout")
def checkout(payload: CheckoutIn, db: Session = Depends(db_session)):
    ids = [item.product_id for item in payload.items]
    db_products = {p.id: p for p in db.scalars(select(Product).where(Product.id.in_(ids))).all()}
    if len(db_products) != len(set(ids)): raise HTTPException(400, "One or more products no longer exist")
    total = 0.0
    tx = Transaction(total=0)
    for item in payload.items:
        p = db_products[item.product_id]
        if item.quantity > p.stock: raise HTTPException(409, f"Only {p.stock} units of {p.name} are available")
        p.stock -= item.quantity; total += p.price * item.quantity
        tx.items.append(TransactionItem(product_id=p.id, product_name=p.name, quantity=item.quantity, unit_price=p.price))
    tx.total = round(total, 2); db.add(tx); db.commit(); db.refresh(tx)
    return {"id": tx.id, "total": tx.total, "created_at": tx.created_at.isoformat(), "items": [i.__dict__ for i in tx.items]}


@app.get("/api/transactions")
def transactions(db: Session = Depends(db_session)):
    rows = db.scalars(select(Transaction).order_by(Transaction.created_at.desc()).limit(50)).all()
    return [{"id": t.id, "created_at": t.created_at.isoformat(), "total": t.total,
             "items": [{"product_name": i.product_name, "quantity": i.quantity, "unit_price": i.unit_price} for i in t.items]} for t in rows]


@app.get("/api/reports/daily")
def daily_report(db: Session = Depends(db_session)):
    today = date.today()
    txs = db.scalars(select(Transaction).where(func.date(Transaction.created_at) == today.isoformat())).all()
    sold = {}
    for t in txs:
        for i in t.items: sold[i.product_name] = sold.get(i.product_name, 0) + i.quantity
    inventory = db.scalars(select(Product).order_by(Product.stock)).all()
    return {"date": today.isoformat(), "sales": round(sum(t.total for t in txs), 2), "transactions": len(txs),
            "best_sellers": sorted([{"name": n, "quantity": q} for n, q in sold.items()], key=lambda x: x["quantity"], reverse=True)[:5],
            "low_stock": [product_out(p) for p in inventory if p.stock <= p.low_stock_threshold]}


@app.get("/api/voice/parse")
def parse_voice(text: str, db: Session = Depends(db_session)):
    lowered = text.lower()
    match = re.search(r"(?:add|buy|give me)\s+(\d+)\s+(.+?)(?:\s+please)?$", lowered)
    action = "add"
    if not match:
        match = re.search(r"(?:remove|delete)\s+(\d+)\s+(.+?)$", lowered); action = "remove"
    if not match: return {"action": "unknown", "message": "Try: Add 5 chocolates"}
    quantity, term = int(match.group(1)), match.group(2).strip()
    matches = db.scalars(select(Product).where(or_(Product.name.ilike(f"%{term}%"), Product.category.ilike(f"%{term}%")))).all()
    return {"action": action, "quantity": quantity, "query": term, "matches": [product_out(p) for p in matches]}

