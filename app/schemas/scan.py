from pydantic import BaseModel

class VerifyRequest(BaseModel):
    image_base64: str
    device_id: str

class VerifyResponse(BaseModel):
    match: bool
    confidence: float
    user_id: str | None = None
    message: str

class EnrollRequest(BaseModel):
    image_base64: str
    user_id: str

class EnrollResponse(BaseModel):
    success: bool
    message: str
