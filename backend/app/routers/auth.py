# regret/backend/app/auth.py



from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from backend.database.connection import get_db
from backend.database.model import User
from backend.schemas.user import SignupUser, SignupResponse,LoginUser, LoginResponse
from backend.security.hashing import hash_password
from backend.security.checkHashing import verify_password
from backend.security.jwt import create_access_token,create_refresh_token


router = APIRouter(tags=["Authentication"])


@router.post("/signup",response_model=SignupResponse,status_code=status.HTTP_201_CREATED)
def signup(user: SignupUser,db: Session = Depends(get_db)):

   
    # checking email and phone number first 

    existing_email = db.query(User).filter(
        User.email == str(user.email)
    ).first()

    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )

    

    existing_phone = db.query(User).filter(
        User.phone == user.phone
    ).first()

    if existing_phone:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Phone number already registered"
        )

    # hasing password 

    hashed_password = hash_password(user.password)

#    createing new user and adding 

    new_user = User(
        name=user.name,
        dob=user.dob,
        phone=user.phone,
        email=str(user.email),
        password_hash=hashed_password,
        is_verified=False
    )


    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)

    except IntegrityError:
        db.rollback()

        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email or phone number already registered"
        )

    return SignupResponse(
        user_id=new_user.user_id,
        name=new_user.name,
        email=new_user.email,
        is_verified=new_user.is_verified,
        message="Registration successful"
    )

@router.post("/login",response_model=LoginResponse,status_code=status.HTTP_200_OK)
def login(user: LoginUser,db: Session = Depends(get_db)):

    # checking email exist or not

    existing_user = db.query(User).filter(
        User.email == str(user.email)
    ).first()

    if existing_user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

#   verifying pasword with hashed value

    is_password_correct = verify_password(
        user.password,
        existing_user.password_hash
    )

    if not is_password_correct:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )


#   generating access token

    access_token = create_access_token(
        user_id=existing_user.user_id
    )

# generating refresh token

    refresh_token = create_refresh_token(
        user_id=existing_user.user_id
    )

#  returning response

    return LoginResponse(
        user_id=existing_user.user_id,
        name=existing_user.name,
        email=existing_user.email,
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        message="Login successful"
    )