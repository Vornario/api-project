from fastapi import FastAPI, HTTPException

app = FastAPI()

class User:
    def __init__(self, user_id, name, email, bought_paintings, blacklist):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.bought_paintings = bought_paintings
        self.blacklist = blacklist

class Painting:
    def __init__(self, painting_id, painting_name, painter, year: int, type, price: int, genre, available):
        self.painting_id = painting_id
        self.painting_name = painting_name
        self.painter = painter
        self.year = year
        self.type = type
        self.price = price
        self.genre = genre
        self.available = available

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
                "available": paintings.available
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
        available=True 
    )
    painting_rep.paintings.append(new_painting)
    return {
        "message": "Painting added successfully!",
        "painting_id": new_painting.painting_id,
        "painting_name": new_painting.painting_name
    }

