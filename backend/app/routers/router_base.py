from typing import Any, List, Type
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.crud_base import CRUDBase

class CRUDRouter:
    def __init__(
        self,
        service: CRUDBase,
        create_schema: Type[BaseModel],
        update_schema: Type[BaseModel],
        read_schema: Type[BaseModel],
    ):
        self.service = service
        self.create_schema = create_schema
        self.update_schema = update_schema
        self.read_schema = read_schema
        
        # Initialize the actual API router
        self.router = APIRouter()
        
        # Register the routes immediately
        self._add_routes()

    def _add_routes(self):
        # Extract model name for error messages (e.g., "Student")
        model_name = self.service.model.__name__

        # --- READ MANY ---
        @self.router.get("/", response_model=List[self.read_schema])
        def read_all(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
            return self.service.get_multi(db, skip=skip, limit=limit)

        # --- READ ONE ---
        @self.router.get("/{id}", response_model=self.read_schema)
        def read_one(id: int, db: Session = Depends(get_db)):
            item = self.service.get(db, id=id)
            if not item:
                raise HTTPException(status_code=404, detail=f"{model_name} not found")
            return item

        # --- CREATE ---
        @self.router.post("/", response_model=self.read_schema, status_code=status.HTTP_201_CREATED)
        def create(item_in: self.create_schema, db: Session = Depends(get_db)):
            return self.service.create(db, obj_in=item_in)

        # --- UPDATE ---
        @self.router.put("/{id}", response_model=self.read_schema)
        def update(id: int, item_in: self.update_schema, db: Session = Depends(get_db)):
            item = self.service.update(db, id=id, obj_in=item_in)
            if not item:
                raise HTTPException(status_code=404, detail=f"{model_name} not found")
            return item

        # --- DELETE ---
        @self.router.delete("/{id}", response_model=self.read_schema)
        def delete(id: int, db: Session = Depends(get_db)):
            item = self.service.remove(db, id=id)
            if not item:
                raise HTTPException(status_code=404, detail=f"{model_name} not found")
            return item