# Змейка

![Header](https://github.com/tooMike/the_snake/blob/main/assets/Screenshot.png)

Игра змейка. В игру добавлены дополнительные элементы: 
– улитка, съедая которую змейка замедляется
– молот Тора, съедая который у змеи на короткое время появляется голова-молот
– препятствия рандомной формы и величины

## Установка

Клонировать репозиторий и перейти в него в командной строке:

```
git clone https://github.com/tooMike/the_snake
```

```
cd the_snake
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

```
source venv/bin/activate
```

Установить зависимости из файла requirements.txt:

```
python3 -m pip install --upgrade pip
```

```
pip install -r requirements.txt
```

```
python3 the_snake.py
```

## Основные технические требования

Python==3.9

