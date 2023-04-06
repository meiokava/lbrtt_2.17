#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import json
import click


@click.group()
def cli():
    pass


@cli.command("add")
@click.option("-d", "--destination", help="Destination of the flight")
@click.option("-n", "--number", type=int, help="Number of the flight")
@click.option("-t", "--type", help="Type of the plane")
@click.argument("filename")
def add(destination, number, type, filename):
    flights = load_flights(filename)
    flights = add_flight(flights, destination, number, type)
    save_flights(filename, flights)


@cli.command("display")
@click.argument("filename")
def display(filename):
    flights = load_flights(filename)
    display_flights(flights)


@cli.command("select")
@click.option("-s", "--select", help="The required select")
@click.argument("filename")
def select(select, filename):
    flights = load_flights(filename)
    selected = select_flights(flights, select)
    display_flights(selected)


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
    if os.path.exists(file_name):
        with open(file_name, "r", encoding="utf-8", errors="ignore") as fin:
            return json.load(fin)
    else:
        return []


if __name__ == '__main__':
    cli()