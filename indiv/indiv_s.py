#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse
import os.path


def add_flight(flights, dst, nmb, tpe):
    flights.append(
        {
            "destination": dst,
            "number_flight": nmb,
            "type_plane": tpe
        }
    )
    return flights


def display_flights(flights):
    """
    displaying the given information
    """
    if flights:
        line = '+-{}-+-{}-+-{}-+-{}-+'.format(
            '-' * 4,
            '-' * 30,
            '-' * 20,
            '-' * 18
        )
        print(line)
        print(
            '| {:^4} | {:^30} | {:^20} | {:^18} |'.format(
                "№",
                "Destination",
                "NumberOfTheFlight",
                "TypeOfThePlane"
            )
        )
        print(line)

        for idx, flight in enumerate(flights, 1):
            print(
                '| {:>4} | {:<30} | {:<20} | {:>18} |'.format(
                    idx,
                    flight.get('destination', ''),
                    flight.get('number_flight', ''),
                    flight.get('type_plane', 0)
                )
            )
        print(line)
    else:
        print('list is empty')


def select_flights(flights, t):
    result = []
    for flight in flights:
        if t in str(flight.values()):
            result.append(flight)
    return result


def save_flights(file_name, flights):
    with open(file_name, "w", encoding="utf-8", errors="ignore") as fout:
        json.dump(flights, fout, ensure_ascii=False, indent=4)


def load_flights(file_name):
    with open(file_name, "r", encoding="utf-8", errors="ignore") as fin:
        return json.load(fin)


def main(command_line=None):
    # Создать родительский парсер для определения имени файла.
    file_parser = argparse.ArgumentParser(add_help=False)
    file_parser.add_argument(
        "filename",
        action="store",
        help="The data file name"
    )

    # Создать основной парсер командной строки.
    parser = argparse.ArgumentParser("flights")
    parser.add_argument(
        "--version",
        action="version",
        version="%(prog)s 0.1.0"
    )

    subparsers = parser.add_subparsers(dest="command")

    # Создать субпарсер для добавления работника.
    add = subparsers.add_parser(
        "add",
        parents=[file_parser],
        help="Add a new flight"
    )
    add.add_argument(
        "-d",
        "--destination",
        action="store",
        required=True,
        help="Destination of the flight"
    )
    add.add_argument(
        "-n",
        "--number",
        action="store",
        type=int,
        required=True,
        help="Number of the flight"
    )
    add.add_argument(
        "-t",
        "--type",
        action="store",
        required=True,
        help="Type of the plane"
    )

    # Создать субпарсер для отображения всех работников.
    _ = subparsers.add_parser(
        "display",
        parents=[file_parser],
        help="Display all flights"
    )

    # Создать субпарсер для выбора работников.
    select = subparsers.add_parser(
        "select",
        parents=[file_parser],
        help="Select the flights"
    )
    select.add_argument(
        "-s",
        "--select",
        action="store",
        required=True,
        help="The required select"
    )

    # Выполнить разбор аргументов командной строки.
    args = parser.parse_args(command_line)

    # Загрузить всех работников из файла, если файл существует .
    is_dirty = False
    if os.path.exists(args.filename):
        flights = list(load_flights(args.filename))
    else:
        flights = []


    # Добавить работника.
    if args.command == "add":
        flights = add_flight(
            flights,
            args.destination,
            args.number,
            args.type
        )
        is_dirty = True

    # Отобразить всех работников.
    elif args.command == "display":
        display_flights(flights)

    # Выбрать требуемых рааботников.
    elif args.command == "select":
        selected = select_flights(flights, args.select)
        display_flights(selected)

    # Сохранить данные в файл, если список работников был изменен.
    if is_dirty:
        save_flights(args.filename, flights)


if __name__ == '__main__':
    main()