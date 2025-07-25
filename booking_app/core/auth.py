from fastapi import APIRouter,Depends,status,HTTPException,Response
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
import booking_app.database.database as database,booking_app.schemas.schemas as schemas,booking_app.models.models as models,booking_app.core.utils as utils,booking_app.core.oauth as oauth
router=APIRouter(tags=['Authentication'])
@router.post('/auth/login')
def login(user_cred: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):

    user=db.query(models.User).filter(models.User.username==user_cred.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credential")
    if not utils.verify_password(user_cred.password,user.hashed_password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="invalid credential")
    access_token=oauth.create_access_token(data={"user_id":user.user_id,"role":user.role})
    return {"access_token":access_token,"token_type":"bearer"}
