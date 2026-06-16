from fastapi import FastAPI, HTTPException
import random
import string
from pydantic import BaseModel

app = FastAPI()

# this is all the routes the application will have
# when the user send a link to the backend, the backend will make the slug 
# or the custom url and store it in the database
# when the user clicks on a shortened url, the application fetches the long url from the
# database and redirects to that site

db = {}

class URLRequest(BaseModel):
    long_url: str
    custom_url: str | None = None

# for creating the shortened url
def make_slug(length = 8):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))


# this method is for storing the shortened url in the database
@app.post("/shorten")
def shorten_url(url: URLRequest):
    slug = url.custom_url.strip() if (url.custom_url) else make_slug(8)
    
    if (slug in db):
        raise HTTPException(status_code=400, detail="shortened url already exists")
    
    db[slug] = url.long_url
    return {"shortened_url": f"http://localhost:8000/{slug}"}

