import os
import sys

import pygame
import requests

start_ll = list(map(float, input('Введите координаты места (через запятую без пробела): ').split(',')))
start_spn = list(map(float, input('Введите масштаб (через запятую без пробела): ').split(',')))


def terminate(map_file):
    pygame.quit()

    # Удаляем за собой файл с изображением.
    os.remove(map_file)
    sys.exit()


def program(start_ll, start_spn):
    ll = start_ll
    spn = start_spn

    map_request = f"http://static-maps.yandex.ru/1.x/?ll={str(ll[0])}," \
                  f"{str(ll[1])}&spn={str(spn[0])},{str(spn[1])}&l=map"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)

    # Инициализируем pygame
    pygame.init()
    screen = pygame.display.set_mode((600, 450))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate(map_file)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_PAGEUP:
                    spn[0] /= 2 # Уменьшаю масштаб в 2 раза и корректирую размер
                    if spn[0] < 0.001:
                        spn[0] = 0.001

                    spn[1] /= 2
                    if spn[1] < 0.001:
                        spn[1] = 0.001
                elif event.key == pygame.K_PAGEDOWN:
                    spn[0] *= 2 # Уменьшаю масштаб в 2 раза и корректирую размер
                    if spn[0] > 90:
                        spn[0] = 90

                    spn[1] *= 2
                    if spn[1] > 90:
                        spn[1] = 90

        map_request = f"http://static-maps.yandex.ru/1.x/?ll={str(ll[0])}," \
                      f"{str(ll[1])}&spn={str(spn[0])},{str(spn[1])}&l=map"
        response = requests.get(map_request)

        # Запишем полученное изображение в файл.
        map_file = "map.png"
        with open(map_file, "wb") as file:
            file.write(response.content)

        # Рисуем картинку, загружаемую из только что созданного файла.
        screen.blit(pygame.image.load(map_file), (0, 0))
        # Переключаем экран и ждем закрытия окна.
        pygame.display.flip()


if __name__ == '__main__':
    program(start_ll, start_spn)