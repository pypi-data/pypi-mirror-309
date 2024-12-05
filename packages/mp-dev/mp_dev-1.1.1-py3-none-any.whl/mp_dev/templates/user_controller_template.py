def get_content():
    return """from sqlalchemy.orm import Session
from fastapi import HTTPException, Request

from app.DB.Model import UserModel
from app.Schema import UserSchema


################################### Read Function #####################################################################
async def get_all(db: Session):
    return db.query(UserModel.User).all()


async def get_by_email(db: Session, email: str):
    user = db.query(UserModel.User).filter(UserModel.User.email == email).first()
    if user is not None:
        return UserSchema.Read(**vars(user))


################################### Add Function #####################################################################
async def add(db: Session, user: UserSchema.Create, request: Request):
    verif_user = await get_by_email(db=db, email=user.email)
    if verif_user:
        raise HTTPException(status_code=400, detail="Utilisateur déjà existant")
    db_user = UserModel.User(
        firstname=user.firstname,
        lastname=user.lastname,
        email=user.email
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
"""