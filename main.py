from fastapi import FastAPI

app = FastAPI()

class User:
    def __init__(self, user_id, name, email, bought_paintings, blacklist):
        self.user_id = user_id
        self.name = name
        self.email = email
        self.bought_paintings = bought_paintings
        self.blacklist = blacklist

#Пользователи

class Painting:
    def __init__(self, painting_name, painter, year, type, price, genre, available):
        self.painting_name = painting_name
        self.painter = painter
        self.year = year
        self.type = type
        self.price = price
        self.genre = genre
        self.available = available

#Книги


class PaintingRepo:
    def __init__(self):
        self.paintinigs = []
        self.increment_id = 0
    def add_painting(self, painting):
        painting.id = self.increment_id
        self.increment_id += 1
        self.paintinigs.append(painting)

    def delete_painting(self, painting):
        self.paintinigs.remove(painting)

    def get_all_paintings(self):
        return self.paintinigs
#Реп книг


painting_rep = PaintingRepo()

@app.get('/paintings')
def get_all_paintings():
    return painting_rep.get_all_paintings()

@app.get('/painting/')
def add_painting(painting_name, painter, year, type, price, genre, available):
    painting_rep.add_painting(Painting(painting_name, painter, year, type, price, genre, available))
    return "ADDED"
