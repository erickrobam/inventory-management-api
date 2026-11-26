from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from app.services.inventory import InventoryService, InsufficientStock

router = APIRouter()
service = InventoryService()

class ProductIn(BaseModel):
    sku: str = Field(min_length=1, max_length=40)
    name: str = Field(min_length=1, max_length=160)

class ProductOut(ProductIn):
    id: int

class MovementIn(BaseModel):
    product_id: int
    quantity: int = Field(gt=0)
    direction: str = Field(pattern="^(in|out)$")
    reference: str = Field(min_length=1, max_length=80)

@router.post("/products", response_model=ProductOut, status_code=status.HTTP_201_CREATED, tags=["products"])
def create_product(payload: ProductIn) -> ProductOut:
    try:
        product = service.create_product(payload.sku, payload.name)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return ProductOut(**product)

@router.get("/products", response_model=list[ProductOut], tags=["products"])
def list_products() -> list[ProductOut]:
    return [ProductOut(**p) for p in service.list_products()]

@router.post("/movements", status_code=status.HTTP_201_CREATED, tags=["inventory"])
def create_movement(payload: MovementIn) -> dict[str, int | str]:
    try:
        balance = service.move_stock(payload.product_id, payload.quantity, payload.direction, payload.reference)
    except KeyError as exc:
        raise HTTPException(status_code=404, detail="Product not found") from exc
    except InsufficientStock as exc:
        raise HTTPException(status_code=409, detail=str(exc)) from exc
    return {"product_id": payload.product_id, "balance": balance}
