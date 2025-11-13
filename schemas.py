"""
Database Schemas for IIC Portal

Each Pydantic model corresponds to a MongoDB collection (collection name = class name in lowercase).
"""
from pydantic import BaseModel, Field
from typing import Optional, List

class Member(BaseModel):
    name: str
    role: str = Field(..., description="Designation/Role in IIC")
    email: Optional[str] = None
    phone: Optional[str] = None
    photo_url: Optional[str] = None

class Activity(BaseModel):
    title: str
    date: str
    category: str = Field(..., description="MIC Driven | Self-Driven | Celebration")
    description: Optional[str] = None
    photos: Optional[List[str]] = None
    report_url: Optional[str] = None
    attendance_count: Optional[int] = None
    semester: Optional[str] = None
    year: Optional[int] = None

class Achievement(BaseModel):
    type: str = Field(..., description="Startup | Patent | Award | Hackathon")
    title: str
    person: str = Field(..., description="Student/Faculty name")
    description: Optional[str] = None
    date: str
    logo_url: Optional[str] = None

class GalleryItem(BaseModel):
    title: str
    media_url: str
    media_type: str = Field(..., description="image | video")
    year: Optional[int] = None
    semester: Optional[str] = None

class Resource(BaseModel):
    title: str
    category: str = Field(..., description="Handbook | Policy | Circular | Template")
    file_url: str

class Idea(BaseModel):
    title: str
    description: str
    team_members: str
    mentor: Optional[str] = None
    file_url: Optional[str] = None
    status: str = Field("Submitted", description="Submitted | Under Review | Accepted | Rejected")

class ContactMessage(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None
    message: str
