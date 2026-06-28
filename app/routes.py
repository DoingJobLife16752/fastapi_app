from fastapi import APIRouter, HTTPException 
from uuid import uuid4, UUID
from app.schemas import UserCreate, UserResponse, UserUpdate  

router = APIRouter(prefix="/users", tags=["Users"])

fake_users_db = []

@router.post("/", response_model=UserResponse)
def create_user(user_data: UserCreate):
    new_id = uuid4()
    
    new_user = {
        "id": new_id,
        "name": user_data.name,
        "email": user_data.email
    }
    
    fake_users_db.append(new_user)
    
    return new_user

@router.get("/", response_model=list[UserResponse])
def get_all_users():
    return fake_users_db

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: UUID):
    for user in fake_users_db:
        if user["id"] == user_id:
            return user
            
    raise HTTPException(status_code=404, detail="User not found")

# 3. Полное обновление пользователя (PUT)
@router.put("/{user_id}", response_model=UserResponse)
def update_user_full(user_id: UUID, updated_data: UserCreate):
    for user in fake_users_db:
        if user["id"] == user_id:
            # Полностью заменяем данные на те, что прислал клиент
            user["name"] = updated_data.name
            user["email"] = updated_data.email
            return user
            
    raise HTTPException(status_code=404, detail="User not found")


@router.patch("/{user_id}", response_model=UserResponse)
def update_user_partial(user_id: UUID, updated_data: UserUpdate):
    for user in fake_users_db:
        if user["id"] == user_id:
            # Превращаем присланные данные в словарь, исключая те, которые клиент не прислал (None)
            # updated_data.model_dump(exclude_unset=True) делает именно это
            data_to_update = updated_data.model_dump(exclude_unset=True)
            
            # Обновляем только те поля, которые были в словаре
            for key, value in data_to_update.items():
                user[key] = value
                
            return user
            
    raise HTTPException(status_code=404, detail="User not found")

@router.delete("/{user_id}", status_code=204)
def delete_user(user_id: UUID):
    for index, user in enumerate(fake_users_db):
        if user["id"] == user_id:
            fake_users_db.pop(index)
            return  
            
    raise HTTPException(status_code=404, detail="User not found")