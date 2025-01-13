from fastapi import FastAPI, HTTPException
from typing import List, Optional

app = FastAPI()

class User:
    def __init__(self, user_id, name, email, bought_paintings, blacklist):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.bought_paintings = bought_paintings
        self.blacklist = blacklist

class Painting:
    def __init__(self, painting_id, painting_name, painter, year: int, type, price: int, genre, on_sale):
        self.painting_id = painting_id
        self.painting_name = painting_name
        self.painter = painter
        self.year = year
        self.type = type
        self.price = price
        self.genre = genre
        self.on_sale = on_sale

class UserRep:
    def __init__(self):
        self.users = [
            User(0, 'Vasya', 'vasya@mail.ru', [], False),
            User(1, "Petya", "petya@mail.ru", [], True)
        ]
        self.users.extend(
            User(i, f'name {i}', f'mail{i}@mail.com', [], False) for i in range(2, 10)
        )

class PaintingRep:
    def __init__(self):
        self.paintings =[]
        self.paintings.append(Painting(0, "My first painting", "Myself", 2005, "Autoportrait",  2000, "Sharzh", True))
        self.paintings.append(Painting(1, "My second painting", "Myself", 2008, "Abstract",  50000, "Luboc", True))
        self.paintings.append(Painting(2, "Blacklist", "Myself", 2011, "Autoportrait",  123515, "Various", True))
        self.paintings.append(Painting(3, "Tender surrender", "Myself", 2009, "Portrait",  51378, "Grotesk", True))
        self.paintings.append(Painting(4, "Parpaing", "Myself", 2013, "Portrait",  24645373, "Goth", True))   

painting_rep = PaintingRep()
user_rep = UserRep()

@app.get("/gallery/", tags=["Картинки"], summary="Показать все картинки", description="Всем привет!")
def get_paintings():
    return painting_rep.paintings

@app.get("/paintings/{picture_id}", tags=["Картинки"], summary="Показать картинку по айди", description="Это не делал чатгпт")
def get_painting_by_id(picture_id:int):
    for paintings in painting_rep.paintings:
        if paintings.painting_id == picture_id:
            return {
                "id": paintings.painting_id,
                "name": paintings.painting_name,
                "painter's name": paintings.painter,
                "year": paintings.year,
                "type": paintings.type,
                "price": paintings.price,
                "genre": paintings.genre,
                "on_sale": paintings.on_sale
            }
    raise HTTPException(status_code=404, detail="Painting not found")

@app.post("/paintings/", tags=["Картинки"], summary="Добавить новую картинку", description="Отвечаю, это не чатгпт")
def add_painting(painting_name: str, painter: str, year: int, type: str, price: int, genre: str):
    painting_id = len(painting_rep.paintings)
    new_painting = Painting(
        painting_id=painting_id,
        painting_name=painting_name,
        painter=painter,
        year=year,
        type=type,
        price=price,
        genre=genre,
        on_sale=True 
    )
    painting_rep.paintings.append(new_painting)
    return {
        "message": "Painting added successfully!",
        "painting_id": new_painting.painting_id,
        "painting_name": new_painting.painting_name
    }


@app.put("/paintings/{painting_id}", tags=["Картинки"], summary="Обновить инфо о картинке", description="Якшешмаш")
def update_painting(painting_id: int, painting_name: str = None, painter: str = None, year: int = None, type: str = None, price: int = None, genre: str = None):
    for painting in painting_rep.paintings:
        if painting.painting_id == painting_id:
            if painting_name is not None:
                painting.painting_name = painting_name
            if painter is not None:
                painting.painter = painter
            if year is not None:
                painting.year = year
            if type is not None:
                painting.type = type
            if price is not None:
                painting.price = price
            if genre is not None:
                painting.genre = genre
            return {
                "message": "Painting updated successfully!",
                "painting_id": painting.painting_id,
                "painting_name": painting.painting_name
            }
    raise HTTPException(status_code=404, detail="Painting not found")


@app.delete("/paintings/{painting_id}", tags=["Картинки"], summary="Удалить картинку по painting_id", description="Йахай")
def delete_painting(painting_id: int):
    for painting in painting_rep.paintings:
        if painting.painting_id == painting_id:
            painting_rep.paintings.remove(painting)
            return {"message": "Painting deleted successfully!"}
    raise HTTPException(status_code=404, detail="Painting not found")

@app.get("/users/", tags=["Юзвери"], summary="Получить список всех пользователей", description="Пипипупу")
def get_users():
    return user_rep.users

@app.post("/users/", tags=["Юзвери"], summary="Добавить пользователя", description="ГООООООООООООООООООООЛ!")
def add_user(name: str, email: str):
    new_id = len(user_rep.users)
    new_user = User(new_id, name, email, [], False)
    user_rep.users.append(new_user)
    return {
        "message": "New customer added successfully",
        "user": {
            "user_id": new_user.user_id,
            "name": new_user.name,
            "email": new_user.email,
            "bought_paintings": new_user.bought_paintings,
            "blacklist": new_user.blacklist
        }
    }

@app.post("/users/{user_id}/buy/{painting_id}", tags=["Юзвери"], summary="Покупка пользователем картинки", description="Ай ай ай ай убили негра, убили")
def user_buy(user_id: int, painting_id: int):
    user = next((u for u in user_rep.users if u.user_id == user_id), None)
    painting = next((p for p in painting_rep.paintings if p.painting_id == painting_id), None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if painting is None:
        raise HTTPException(status_code=404, detail="Painting not found")
    if user.blacklist:
        raise HTTPException(status_code=403, detail="User is blacklisted")
    if not painting.on_sale:
        raise HTTPException(status_code=400, detail="Painting is not on_sale")

    painting.on_sale = False
    user.bought_paintings.append(painting.painting_name)
    return {
        "message": "Painting purchased successfully!",
        "user_id": user.user_id,
        "painting_id": painting.painting_id
    }

@app.post("/users/{user_id}/rage/{painting_id}", tags=["Юзвери"], summary="Яростное возвращение картины", description="Пользователь яростно возвращает картину")
def user_rage_return(user_id: int, painting_id: int):
    user = next((u for u in user_rep.users if u.user_id == user_id), None)
    painting = next((p for p in painting_rep.paintings if p.painting_id == painting_id), None)

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    if painting is None:
        raise HTTPException(status_code=404, detail="Painting not found")
    if painting_id not in user.bought_paintings:
        raise HTTPException(status_code=400, detail="User has not purchased this painting")

    painting.available = True
    user.blacklist = True
    user

