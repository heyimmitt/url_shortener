from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker, Session

import random
import string
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "sqlite:///./urls.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

Base = declarative_base()

class URL(Base): 
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String, unique=True, index=True)
    long_url = Column(String)


Base.metadata.create_all(bind=engine)

# SessionLocal is a factory that creates sessions when called
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# get_db opens a session
def get_db():
    db = SessionLocal()   # opens here
    try:
        yield db        # yields it (hands it over temporarily)
    finally:
        db.close()      # once whoever opened the session is done, the control comes back to finally and the session is closed



# this is all the routes the application will have
# when the user send a link to the backend, the backend will make the slug 
# or the custom url and store it in the database
# when the user clicks on a shortened url, the application fetches the long url from the
# database and redirects to that site

# db = {}

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class URLRequest(BaseModel):
    long_url: str
    custom_url: str | None = None

# for creating the shortened url
def make_slug(length = 8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# this method is for storing the shortened url in the database
@app.post("/shorten")
def shorten_url(url: URLRequest, db: Session = Depends(get_db)):
    slug = url.custom_url.strip() if url.custom_url else make_slug(8)

    existing = db.query(URL).filter(URL.slug == slug).first()
    if existing:
        raise HTTPException(status_code=400, detail="shortened url already exists")
    
    new_entry = URL(slug=slug, long_url=url.long_url)
    db.add(new_entry)
    db.commit()

    return {"shortened_url": f"http://localhost:8000/{slug}"}

