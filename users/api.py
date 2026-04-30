from ninja import Router, Schema
from django.contrib.auth import get_user_model, authenticate
from jose import jwt
from datetime import datetime, timedelta
from ninja.security import HttpBearer

router = Router()
User = get_user_model()

SECRET_KEY = "secret123"
ALGORITHM = "HS256"

# =====================
# AUTH BEARER
# =====================
class AuthBearer(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except:
            return None

# =====================
# SCHEMA
# =====================
class RegisterSchema(Schema):
    username: str
    email: str
    password: str

class LoginSchema(Schema):
    username: str
    password: str

# =====================
# REGISTER
# =====================
@router.post("/register")
def register(request, data: RegisterSchema):
    user = User.objects.create_user(
        username=data.username,
        email=data.email,
        password=data.password
    )
    return {"message": "User dibuat", "id": user.id}

# =====================
# LOGIN
# =====================
@router.post("/login")
def login(request, data: LoginSchema):
    user = authenticate(username=data.username, password=data.password)

    if not user:
        return {"error": "Salah login"}

    payload = {
        "user_id": user.id,
        "exp": datetime.utcnow() + timedelta(hours=1)
    }

    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)

    return {"access_token": token}

# =====================
# ME
# =====================
@router.get("/me", auth=AuthBearer())
def get_me(request):
    return {"user": request.auth}

@router.put("/me", auth=AuthBearer())
def update_me(request, username: str = None, email: str = None):
    user = User.objects.get(id=request.auth["user_id"])

    if username:
        user.username = username
    if email:
        user.email = email

    user.save()
    return {"message": "Profile updated"}

# =====================
# REFRESH
# =====================
@router.post("/refresh")
def refresh_token(request, token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])

        new_payload = {
            "user_id": payload["user_id"],
            "exp": datetime.utcnow() + timedelta(hours=1)
        }

        new_token = jwt.encode(new_payload, SECRET_KEY, algorithm=ALGORITHM)

        return {"access_token": new_token}
    except:
        return {"error": "Invalid token"}