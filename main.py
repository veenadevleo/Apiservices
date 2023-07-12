from bson import ObjectId
from fastapi import FastAPI, HTTPException
from pymongo import MongoClient
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],  # Update with your frontend URL
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Connect to MongoDB and create the database and collection if they don't exist
client = MongoClient("mongodb://localhost:27017/")
db = client["mydatabase"]
collection = db["products"]

# Create the collection if it doesn't exist
if "products" not in db.list_collection_names():
    db.create_collection("products")


class Product(BaseModel):
    name: str
    price: float
    description: str


@app.get("/products")
def get_products():
    products = list(collection.find())
    for product in products:
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
    return products

@app.get("/products/{product_id}")
def get_product(product_id: str):
    product = collection.find_one({"_id": ObjectId(product_id)})
    if product:
        product["_id"] = str(product["_id"])  # Convert ObjectId to string
        return product
    raise HTTPException(status_code=404, detail="Product not found")


@app.post("/products")
def create_product(product: Product):
    product_data = product.dict()
    result = collection.insert_one(product_data)
    return {"message": "Product created", "product_id": str(result.inserted_id)}


@app.put("/products/{product_id}")
def update_product(product_id: str, product: Product):
    product_data = product.dict()
    result = collection.update_one({"_id": ObjectId(product_id)}, {"$set": product_data})
    if result.modified_count > 0:
        return {"message": "Product updated"}
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/{product_id}")
def delete_product(product_id: str):
    result = collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count > 0:
        return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")
