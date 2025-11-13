import os
from typing import List, Optional
from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from database import db, create_document, get_documents
from schemas import Member, Activity, Achievement, GalleryItem, Resource, Idea, ContactMessage

app = FastAPI(title="IIC Portal API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {"message": "IIC Portal Backend Running"}

# ---------- Info Endpoints ----------
@app.get("/about")
def about():
    return {
        "intro": "The Institution’s Innovation Council (IIC) was established under the Ministry of Education’s Innovation Cell (MIC) to build an ecosystem that inspires students and faculty to think innovatively and embrace entrepreneurship.",
        "vision": "To foster a vibrant innovation and startup culture in the institute.",
        "mission": [
            "Encourage ideation and problem solving",
            "Support pre-incubation and entrepreneurship",
            "Enable collaboration between students, faculty, and industry"
        ],
        "establishment": {
            "date": "01-08-2020",
            "mic_registration": "MIC-REG-123456"
        },
        "objectives": [
            "Foster innovation culture among students.",
            "Encourage entrepreneurship to serve the society and nation.",
            "Support pre-incubation"
        ]
    }

# ---------- Members ----------
@app.get("/members")
def list_members(limit: int = 100):
    items = get_documents("member", {}, limit)
    # Provide defaults if empty
    if not items:
        items = [
            {"name": "Prof. (Dr.) Upasana Pandey", "role": "President", "email": None, "phone": None, "photo_url": None},
            {"name": "Dr. Vineet Kumar Singh", "role": "Convener", "email": None, "phone": None, "photo_url": None},
            {"name": "Mr. Avdheh Kumar Tiwari", "role": "Innovation Coordinator", "email": None, "phone": None, "photo_url": None},
            {"name": "Dr. Meenu Baliyan", "role": "Start-up Coordinator", "email": None, "phone": None, "photo_url": None},
            {"name": "Mr. Satyendra Singh", "role": "Start-up Coordinator", "email": None, "phone": None, "photo_url": None},
            {"name": "Ms. Meena Kumari", "role": "IPR Coordinator", "email": None, "phone": None, "photo_url": None},
            {"name": "Mr. Gunabh Saran", "role": "Student Member", "email": None, "phone": None, "photo_url": None},
            {"name": "Mr. Aman Srivastava", "role": "Student Member", "email": None, "phone": None, "photo_url": None},
        ]
    return items

class MemberCreate(Member):
    pass

@app.post("/members")
def add_member(payload: MemberCreate):
    _id = create_document("member", payload)
    return {"id": _id}

# ---------- Activities ----------
@app.get("/activities")
def list_activities(limit: int = 200, year: Optional[int] = None, semester: Optional[str] = None, category: Optional[str] = None):
    filt = {}
    if year: filt["year"] = year
    if semester: filt["semester"] = semester
    if category: filt["category"] = category
    items = get_documents("activity", filt, limit)
    return items

@app.post("/activities")
def add_activity(payload: Activity):
    _id = create_document("activity", payload)
    return {"id": _id}

# ---------- Achievements ----------
@app.get("/achievements")
def list_achievements(limit: int = 200, type: Optional[str] = None):
    filt = {"type": type} if type else {}
    items = get_documents("achievement", filt, limit)
    return items

@app.post("/achievements")
def add_achievement(payload: Achievement):
    _id = create_document("achievement", payload)
    return {"id": _id}

# ---------- Gallery ----------
@app.get("/gallery")
def list_gallery(limit: int = 200, year: Optional[int] = None):
    filt = {"year": year} if year else {}
    items = get_documents("galleryitem", filt, limit)
    return items

@app.post("/gallery")
def add_gallery_item(payload: GalleryItem):
    _id = create_document("galleryitem", payload)
    return {"id": _id}

# ---------- Resources ----------
@app.get("/resources")
def list_resources(limit: int = 100, category: Optional[str] = None):
    filt = {"category": category} if category else {}
    items = get_documents("resource", filt, limit)
    # Provide a few defaults if empty
    if not items:
        items = [
            {"title": "IIC Handbook", "category": "Handbook", "file_url": "#"},
            {"title": "Innovation & Startup Policy of Institute", "category": "Policy", "file_url": "#"},
            {"title": "IPR Policy", "category": "Policy", "file_url": "#"},
            {"title": "Event Report Format", "category": "Template", "file_url": "#"},
            {"title": "Feedback Form", "category": "Template", "file_url": "#"},
            {"title": "Attendance Sheet", "category": "Template", "file_url": "#"},
        ]
    return items

@app.post("/resources")
def add_resource(payload: Resource):
    _id = create_document("resource", payload)
    return {"id": _id}

# ---------- Ideas ----------
@app.get("/ideas")
def list_ideas(limit: int = 200, status: Optional[str] = None):
    filt = {"status": status} if status else {}
    items = get_documents("idea", filt, limit)
    return items

@app.post("/ideas")
def submit_idea(payload: Idea):
    _id = create_document("idea", payload)
    return {"id": _id, "status": "Received"}

# ---------- Contact & Feedback ----------
@app.post("/contact")
def contact(payload: ContactMessage):
    _id = create_document("contactmessage", payload)
    return {"id": _id, "status": "Received"}

# ---------- Utility ----------
@app.get("/schema")
def schema_overview():
    return {
        "member": Member.model_json_schema(),
        "activity": Activity.model_json_schema(),
        "achievement": Achievement.model_json_schema(),
        "galleryitem": GalleryItem.model_json_schema(),
        "resource": Resource.model_json_schema(),
        "idea": Idea.model_json_schema(),
        "contactmessage": ContactMessage.model_json_schema(),
    }

@app.get("/test")
def test_database():
    from database import db
    status = {
        "backend": "Running",
        "database": "Connected" if db is not None else "Unavailable"
    }
    if db is not None:
        try:
            status["collections"] = db.list_collection_names()[:10]
        except Exception as e:
            status["database"] = f"Error: {str(e)[:80]}"
    return status

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
