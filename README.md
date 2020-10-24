# find-flat-number-via-square
Узкоспециализированный скрипт, позволяющий найти квартиры с нужной площадью в конкретном доме (или даже этаже\в подъезде).

Пример запуска:
`/tmp/1.py --min_flat_number=133 --max_flat_number=216 --max_flat_number_in_entrance=144 --floors_number=9 --flats_in_floor=4 --main_kadastr_num="16:50:110805:" --min_last_kadastr_num=3011 --max_last_kadastr_num=3300 --min_area=32 --max_area=34 --street_name="Республика Татарстан, г Казань, пр-кт Ямашева, д 78"`

Пример: мы знаем, что жертва проживает в городе Казань, на улице пр-кт Ямашева, д 78 на верхних этажах (последние три) и в середине дома (4, 5 и 6 подъезды). Далее нам необходимо узнать номера квартир (диапазон), в которых может жить наша жертва. Для этого воспользуйтесь 2gis (https://2gis.ru/kazan/search/%D1%8F%D0%BC%D0%B0%D1%88%D0%B5%D0%B2%D0%B0%2078/geo/2956122910646110/49.141339%2C55.827638?m=49.141793%2C55.827757%2F18.98) и вручную посчитайте номер максимально возможной квартиры и минимально возможной. В моём случае макимально возможная квартира это 216, а минимальная 133. Потом смотрим этажность дома, в моём случае в доме 9 этажей. 4 квартиры на этаж. 4x9=36. Значит, шаг "инетации" 36. Поэтому в скрипте ставим вот так:
a=133; b=145
while b<=217:
    for i in range(a, b):
        approved_flats.append(i)
    a=a+36; b=b+36
    
a=минимальный номер квартиры, b<217=максимальный номер квартиры + 1, b=145 -- максимально возможный номер квартиры в подъезде. Прочтите несколько раз, думаю, станет понятно. a=a+36; b=b+36 -- как раз "шаг итерации".

Далее находим кадастровый номер первой квартиры в доме:
https://www.avito.ru/proverka-kvartir/preview/16:50:110805:3011

Видим номер: 16:50:110805:3011
Последние 4 цифры меняются, но не по порядку, и в этом нлавная проблема. В любом случае, в строку json={'key' : '16:50:110805:'вводим все цифры, кроме последних 4-х.

В эту строку вводим адрес в таком формате (возьмите со страницы Авито, а вместо 34>32 введите площадь квартиры (в моём случае больше 32, но меньше 34, т.е. подходит 33))
if "Республика Татарстан, г Казань, пр-кт Ямашева, д 78" in rj['result']['address'] and 34>rj['result']['area']>32:

А в строку for i in range(3011,3300) введите 4 цифры кадастрового номера, от которого надо проверять квартиры, и максимальное значение +1 в конец диапазона. Т.е. в данном случае будут проверять квартиры от 16:50:110805:3011 до 16:50:110805:3301.
