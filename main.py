from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Literal

app = FastAPI(
    title="Nairobi Freelance Gigs API - C027-01-0881/2024",
    description="API for managing freelance gigs in Nairobi",
    version="1.0.0"
)
# Initial dataset
gigs_db = [
    {
        "id": 1,
        "title": "Social Media Campaign Management",
        "description": "Manage social media campaigns for a local fashion business.",
        "category": "Marketing",
        "budget": 15000,
        "currency": "KES",
        "status": "Open",
        "client_name": "Jane Muthoni"
    },
    {
        "id": 2,
        "title": "Sales Data Analysis",
        "description": "Analyze company sales data and generate reports.",
        "category": "Data",
        "budget": 20000,
        "currency": "KES",
        "status": "Open",
        "client_name": "Peter Mwangi"
    },
    {
        "id": 3,
        "title": "Business Strategy Consultation",
        "description": "Provide business growth strategies for startups.",
        "category": "Consulting",
        "budget": 25000,
        "currency": "KES",
        "status": "In Progress",
        "client_name": "Faith Wanjiku"
    },
    {
        "id": 4,
        "title": "SEO Marketing Project",
        "description": "Improve search engine rankings for an online business.",
        "category": "Marketing",
        "budget": 18000,
        "currency": "KES",
        "status": "Open",
        "client_name": "Brian Otieno"
    },
    {
        "id": 5,
        "title": "Customer Data Cleaning",
        "description": "Clean and organize customer records for migration.",
        "category": "Data",
        "budget": 12000,
        "currency": "KES",
        "status": "Closed",
        "client_name": "Mercy Achieng"
    },
    {
        "id": 6,
        "title": "Financial Advisory Services",
        "description": "Provide financial planning advice for SMEs.",
        "category": "Consulting",
        "budget": 30000,
        "currency": "KES",
        "status": "Open",
        "client_name": "David Kamau"
    }
]

# Model for creating a gig
class GigCreate(BaseModel):
    title: str = Field(min_length=5, max_length=100)
    description: str = Field(min_length=20, max_length=500)
    category: Literal["Marketing", "Data", "Consulting"]
    budget: float = Field(gt=0)
    client_name: str = Field(min_length=2, max_length=50)

# Model for updating a gig
class GigUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=5, max_length=100)
    description: Optional[str] = Field(None, min_length=20, max_length=500)
    category: Optional[Literal["Marketing", "Data", "Consulting"]] = None
    budget: Optional[float] = Field(None, gt=0)
    status: Optional[Literal["Open", "In Progress", "Closed"]] = None
    client_name: Optional[str] = Field(None, min_length=2, max_length=50)

# Home endpoint
@app.get("/")
def home():
    return {"message": "Welcome to the Nairobi Freelance Gigs API"}

# Get all gigs
@app.get("/gigs")
def get_gigs():
    return gigs_db

# Get a single gig
@app.get("/gigs/{gig_id}")
def get_gig(gig_id: int):
    for gig in gigs_db:
        if gig["id"] == gig_id:
            return gig

    raise HTTPException(status_code=404, detail="Gig not found")

# Search gigs
@app.get("/gigs/search")
def search_gigs(q: str):
    results = []

    for gig in gigs_db:
        if (
            q.lower() in gig["title"].lower()
            or q.lower() in gig["description"].lower()
            or q.lower() in gig["category"].lower()
        ):
            results.append(gig)

    return results

# Create a new gig
@app.post("/gigs")
def create_gig(gig: GigCreate):

    new_id = max([g["id"] for g in gigs_db]) + 1 if gigs_db else 1

    new_gig = {
        "id": new_id,
        "title": gig.title,
        "description": gig.description,
        "category": gig.category,
        "budget": gig.budget,
        "currency": "KES",
        "status": "Open",
        "client_name": gig.client_name
    }

    gigs_db.append(new_gig)

    return {
        "message": "Gig created successfully",
        "gig": new_gig
    }

# Update a gig
@app.put("/gigs/{gig_id}")
def update_gig(gig_id: int, gig_update: GigUpdate):

    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:

            if gig_update.title is not None:
                gigs_db[index]["title"] = gig_update.title

            if gig_update.description is not None:
                gigs_db[index]["description"] = gig_update.description

            if gig_update.category is not None:
                gigs_db[index]["category"] = gig_update.category

            if gig_update.budget is not None:
                gigs_db[index]["budget"] = gig_update.budget

            if gig_update.status is not None:
                gigs_db[index]["status"] = gig_update.status

            if gig_update.client_name is not None:
                gigs_db[index]["client_name"] = gig_update.client_name

            return {
                "message": "Gig updated successfully",
                "gig": gigs_db[index]
            }

    raise HTTPException(status_code=404, detail="Gig not found")

# Delete a gig
@app.delete("/gigs/{gig_id}")
def delete_gig(gig_id: int):

    for index, gig in enumerate(gigs_db):
        if gig["id"] == gig_id:
            deleted_gig = gigs_db.pop(index)

            return {
                "message": "Gig deleted successfully",
                "gig": deleted_gig
            }

    raise HTTPException(status_code=404, detail="Gig not found")