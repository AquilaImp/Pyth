#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Создайте списки:

# моя семья (минимум 3 элемента, есть еще дедушки и бабушки, если что)
my_family = [
    ['Отец'],
    ['Сын'],
    ['Мать'],
]


# список списков приблизителного роста членов вашей семьи
my_family_height = [
    ['Петька', 200],
    ['Лешка',170],
    ['Люся',165],
]
print('Роста отца -',my_family_height[0][1],' см')
# Выведите на консоль рост отца в формате
#   Рост отца - ХХ см
print('Общий рост моей семьи ',my_family_height[0][1]+my_family_height[1][0]+my_family_height[2][0],' см')
# Выведите на консоль общий рост вашей семьи как сумму ростов всех членов
#   Общий рост моей семьи - ХХ см
