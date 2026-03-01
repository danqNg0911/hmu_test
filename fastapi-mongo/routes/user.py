from fastapi import Body, APIRouter, HTTPException
from passlib.context import CryptContext

from auth.jwt_handler import sign_jwt 
from database.database import add_user
from models.user import User
from schemas.user import UserData, UserSignIn, UserCreate

router = APIRouter()

hash_helper = CryptContext(schemes=["bcrypt"], deprecated="auto")

@router.post("/login")
async def user_login(user_credentials: UserSignIn = Body(...)):
    user_exists = await User.find_one(User.username == user_credentials.username)
    
    if user_exists:
        is_password_valid = hash_helper.verify(user_credentials.password, user_exists.password)
        if is_password_valid:
            return sign_jwt(user_credentials.username)

        raise HTTPException(status_code=403, detail="Tài khoản hoặc mật khẩu không chính xác")

    raise HTTPException(status_code=403, detail="Tài khoản hoặc mật khẩu không chính xác")


@router.post("/signup", response_model=UserData)
async def user_signup(user_data: UserCreate = Body(...)):
    username_exists = await User.find_one(User.username == user_data.username)
    if username_exists:
        raise HTTPException(
            status_code=409, detail="Username này đã được sử dụng"
        )
        
    email_exists = await User.find_one(User.email == user_data.email)
    if email_exists:
        raise HTTPException(
            status_code=409, detail="Email này đã được đăng ký"
        )

    hashed_password = hash_helper.hash(user_data.password)
    
    new_user_db = User(
        name=user_data.name,
        username=user_data.username,
        password=hashed_password,
        email=user_data.email,
        role=user_data.role
    )
    
    created_user = await add_user(new_user_db)
    return created_user