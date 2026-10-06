from fastapi import APIRouter, HTTPException
from app.schemas.scan import VerifyRequest, VerifyResponse, EnrollRequest, EnrollResponse
from app.services.face_service import face_service
from app.services.pinecone_service import pinecone_service

router = APIRouter()

@router.post("/verify", response_model=VerifyResponse)
async def verify_face(req: VerifyRequest):
    import logging
    logger = logging.getLogger(__name__)
    logger.info(f"[Face API] Received verify request for device: {req.device_id}")
    try:
        # 1. Extract face embedding
        logger.info("[Face API] Extracting embedding from image...")
        embedding = face_service.extract_embedding(req.image_base64)
        logger.info("[Face API] Embedding extracted successfully. Querying Pinecone...")
        
        # 2. Query Pinecone
        user_id, confidence = pinecone_service.verify_face(embedding)
        logger.info(f"[Face API] Pinecone returned user_id={user_id}, confidence={confidence}")
        
        if user_id:
            logger.info("[Face API] Match successful!")
            return VerifyResponse(
                match=True, 
                confidence=confidence, 
                user_id=user_id, 
                message="Face matched successfully"
            )
        else:
            logger.info("[Face API] Match failed (no user found or below threshold).")
            return VerifyResponse(
                match=False, 
                confidence=confidence, 
                message="Face not recognized"
            )
            
    except ValueError as e:
        logger.error(f"[Face API] ValueError during verify: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        logger.error(f"[Face API] Exception during verify: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Verification error: {str(e)}")


@router.post("/enroll", response_model=EnrollResponse)
async def enroll_face(req: EnrollRequest):
    try:
        # 1. Extract face embedding
        embedding = face_service.extract_embedding(req.image_base64)
        
        # 2. Store in Pinecone
        pinecone_service.upsert_face(req.user_id, embedding)
        
        return EnrollResponse(success=True, message=f"Face enrolled for user {req.user_id}")
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Enrollment error: {str(e)}")
