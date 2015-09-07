from peewee import Model, CharField, SqliteDatabase, OperationalError, ForeignKeyField, TextField
# from utils import get_hash
from peewee import IntegerField


class User(Model):
    mail = CharField()
    password = CharField()
    port = IntegerField(unique=True)

    class Meta:
        database = SqliteDatabase('data.db')


class RunSettings(Model):
    json_string = TextField()
    name = CharField()
    user = ForeignKeyField(User)

    class Meta:
        database = SqliteDatabase('data.db')


def create_relations():
    # запоминаем все используемые в бд модели
    models = [User, RunSettings]

    # чистим базу данных
    print('чистим базу данных')
    db = SqliteDatabase('data.db')
    try:
        db.drop_tables(models)
    except OperationalError:
        pass

    # создаем таблицы в бд
    print('\nсоздаем модели в бд:')
    for i in models:
        print(i)
        i.create_table()

    # добавляем пользователя
    print('\nдобавляем пользователя')
    admin_user = User(mail="admin@admin.ru", password=get_hash('1'), port=56001)
    admin_user.save()

    test_user = User(mail="test@test.ru", password=get_hash('1'), port=9701)
    test_user.save()


if __name__ == '__main__':
    create_relations()
