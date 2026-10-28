# Copyright © 2022-2024 FriedrichFroebel
#
# This file is part of didjvu.
#
# didjvu is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# didjvu is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
# FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License
# for more details.


def main(prog: str | None = None) -> None:
    from didjvu.didjvu import Main
    Main(prog=prog)


if __name__ == '__main__':
    main(prog='didjvu.__main__')
