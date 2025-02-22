#
# EPITECH PROJECT, 2023
# map_generator
# File description:
# Generates maps for the my_radar project
# Made by julien1.calenge@epitech.eu
#

from sys import argv
import argparse
from textwrap import dedent, fill
from dataclasses import dataclass
from abc import abstractmethod
from typing import Union, Any
from random import seed, randint, sample, uniform


"""
File meant to ease the map generation for the my_radar EPITECH project.
It has been created for testing purposes but is not meant to cover
every possible edge-case. Use it with care.

This file isn't PEP8 at all, that's because of the portability aspect of
it, as it will be used "as it is", which is a single script file.
E501 has been violated many times, mainly because of the helper method.
It has been kept under 100 chars except in the helper and exceptions
at all times.
E731 is a known issue that has no easy nor elegant workaround.
Every other error is a mistake and you are welcome to submit a PR
or an issue at https://github.com/jclge/my_radar_testing.git

Every single variable, function, method or attribute has a type hint
except for function pointers. If there is any missing, feel free to
fill an issue on the link given above.
"""


@dataclass
class Data:
    """
    Data class meant to store the args data and passed to Manager

    Has been created to increase the reusability of this script
    and its maintability. Avoids using an undisclosed amount of
    arguments with variadic built-ins such as **kwargs.
    Avoids using many arguments passed to function and makes the
    script modification proof as adding only partialy an argument
    would still let it work as usual.
    """
    planes: int
    towers: int
    radius: int
    duration: int
    floating: bool
    seed: int
    path:str
    max_speed: int
    min_speed: int
    spawn: bool
    output:str


class TooManyTowersException(Exception):
    """
    This exception is raised when more towers are asked for than there is
    supplied.
    """
    pass


class BadTowersFileFormatException(Exception):
    """
    This exception is raised when the towers' position file isn't well
    formated.

    The only valid formats are [T x_coord y_coord] and [x_coord y_coord].
    """
    pass


class ConflictingSpeedsException(Exception):
    """
    This exception is raised when the given max_speed exceeds the given
    min_speed.
    """
    pass


class CustomHelpFormatter(argparse.ArgumentDefaultsHelpFormatter):
    """
    Class meant to overload the HelpFormatter class from the argparse lib
    Is mainly used to make a beautiful --help
    """
    def __init__(self, prog:str) -> None:
        """Calls original constructor with custom arguments"""
        super().__init__(prog, max_help_position=10, width=80)

    def _format_action_invocation(self, action: argparse.Action) -> str:
        """
        Main method to format --help.

        Originaly found on StackOverflow but lost the link
        """
        if not action.option_strings or action.nargs == 0:
            return super()._format_action_invocation(action)
        default:str = self._get_default_metavar_for_optional(action)
        args_string:str = self._format_args(action, default)
        return ', '.join(action.option_strings) + ' ' + args_string

    def _fill_text(self, text:str, width: int, indent:str) -> str:
        """
        Re-write of the function used to format epilog & description arguments

        The indent is calculated on the length of the 'title' of the category
        (e.g info:)
        This is not standard but had to be used this way.
        If no category, please place a ':' at index 0.
        """
        return fill(text, width, subsequent_indent=(len(text.split(':')[0]) + 2) * ' ')


class Parser:
    """
    Class made of a single abstract method meant to parse argv and display a
    helper thanks to the argparse lib
    """
    @abstractmethod
    def parse_args() -> Data:
        """
        Only method to parse arguments.

        Has some basic logic in it to allow for a more readable --help,
        such as the default random seed which isn't set directly in the parser object.
        Calls the overloaded built-in argparse library thanks to a lambda variable,
        which isn't PEP8 but the workaround isn't worth the effort.

        This is a known issue that negative numbers can be given as argument
        to some of the parameters.
        This should still work out properly but the my_radar project on which
        it's tested, most likely not so much.
        """
        chf = lambda prog: CustomHelpFormatter(prog)
        parser = argparse.ArgumentParser(formatter_class=chf,
                                         description=dedent('info: Please note that this generator does not cover all the edge cases that may be tested on your project. It\'s only meant to make the generation painless and easy.'),
                                         epilog=dedent(f'usage example: python {argv[0]} -p 100 -t 8 -d 20 -f -r 5 --path ./path/to/file | This example would generate 100 planes traveling at varying velocities represented as floats between 8 towers placed based off the file given as argument, with their radius maxed at 5% of the screen size, all of that in a 20 seconds delay.'))
        parser.add_argument('-p', '--planes', metavar='Planes', required=True, choices=range(1, 1000000), dest='planes', help='Amount of planes as an unsigned integer', type=int)
        parser.add_argument('-t', '--towers', metavar='Towers', required=True, choices=range(2, 50), dest='towers', help='Amount of towers as an unsigned integer', type=int)
        parser.add_argument('-r', '--radius', metavar='Radius', default=30, choices=range(5, 100), dest='radius', help='Percentage of the screen taken as a maximum value for the radius of the towers as an unsigned integer', type=int)
        parser.add_argument('-d', '--duration', metavar='Duration', default=30, dest='duration', help='Time in seconds after which no plane will spawn. Planes will spawn in an uniform way from t0 to tn.', type=int)
        parser.add_argument('-f', '--float', action='store_true', dest="float", help="Can coordinates contain floating numbers")
        parser.add_argument('-S', '--towers_spawn', action='store_false', dest="spawn", help='Will planes spawn at random or on towers. Defaults on towers.')
        parser.add_argument('-M', '--max_speed', metavar='Max planes\' speed', default=150, dest='max_speed', help='Caps the speed of the planes to a given integer.', type=int)
        parser.add_argument('-m', '--min_speed', metavar='Min planes\' speed', default=15, dest='min_speed', help='Sets the minimal speed of the planes to a given integer.', type=int)
        parser.add_argument('-s', '--seed', metavar='Random seed', default=None, dest='seed', help='Seed that will be used for any random calculation', type=int)
        parser.add_argument('-P', '--path', metavar='Path to custom towers\' file', default=None, dest='path', help='Custom path to the towers\' file.', type=str)
        parser.add_argument('-o', '--output', metavar='Output Path', default='nb_planes_nb_towers.rdr', dest='output', help='Custom path to an output file', type=str)
        res: dict[Any] = parser.parse_args()
        if res.max_speed < res.min_speed:
            raise ConflictingSpeedsException(f'max_speed [{res.max_speed}] is smaller than min_speed [{res.min_speed}].')
        return Data(planes=res.planes,
                    towers=res.towers,
                    duration=res.duration,
                    radius=res.radius,
                    floating=res.float,
                    seed=randint(0, 2**100) if res.seed is False else res.seed,
                    path=res.path,
                    max_speed=res.max_speed,
                    min_speed=res.min_speed,
                    spawn=res.spawn,
                    output=f'{res.planes}_planes_{res.towers}_towers.rdr' if res.output == 'nb_planes_nb_towers.rdr' else res.output)


class Towers:
    """
    The Towers class meant to generate the towers

    Generates their positions as well as the correctly
    formated string to write to the file
    """
    def __init__(self, path: Union[str, None], nb: int, radius: int) -> None:
        """
        Constructor calls the methods used to generate the towers and their radius

        Everything is processed in the constructor because the sole purpose of
        this class is to populate a single attribute, which will be generated
        for each file and therefore destroying the object each use
        is clearer and eases the readability
        """
        self._towers: list[list[int]] = []
        self.__towers_generation(path, nb)
        self.__radius_generation(radius)

    def __str__(self) -> str:
        """
        str operator overload to ease the transformation from list[list[int]] to str
        """
        return '\n'.join(['T ' + ' '.join(map(str, tower)) for tower in self._towers])

    def __get_towers_file(self, path:str) -> list[list[int]]:
        """
        Retrives the towers in a file passed as argument

        File can either be in the same format as the result
        or raw coordinates. There cannot be radius included
        either way.
        """
        with open(path, 'r') as o:
            file_content = o.read().split('\n')
            o.close()
        try:
            if 'T' in file_content[0]:
                return [list(map(int, line.replace('T ', '').split(' '))) for line in file_content]
            else:
                return [list(map(int, line)) for line in file_content]
        except Exception:
            raise BadTowersFileFormatException('File should either be a list of positions separated by spaces & newlines or in the same format as a .rdr file excluding radius.')

    def __towers_generation(self, path: Union[str, None], nb: int) -> None:
        """
        Generates the towers thanks to either the list included or the
        file given as argument.

        Towers are written directly in the script,
        inside a list for portability purposes.
        Custom exceptions have been added for a more explicit error
        handling since they are directly related to the towers passed
        as argument.
        The positions of the towers replicates major cities placed
        on the map currently given on the intranet (2023)
        """
        if path is not None:
            self._towers: list[list[int]] = self.__get_towers_file(path)
        else:
            try:
                self._towers: list[list[int]] = sample([[27, 135],
                                                        [230, 200], [250, 315], [340, 435],
                                                        [470, 310], [495, 675], [495, 550], [510, 860],
                                                        [620, 795], [650, 110], [690, 640], [820, 490],
                                                        [880, 330], [920, 220], [945, 545], [990, 660],
                                                        [1020, 830], [1035, 165], [1070, 290],
                                                        [1070, 375], [1090, 580], [1125, 190],
                                                        [1160, 550], [1160, 750], [1190, 405],
                                                        [1340, 500], [1390, 300], [1470, 480],
                                                        [1500, 630], [1540, 405], [1565, 825],
                                                        [1680, 310], [1695, 635], [1735, 855],
                                                        [1855, 920]], nb)
            except Exception:
                raise TooManyTowersException(f'{nb} is more than the default amount of towers [35]. Please supply a file or reduce the number of towers to overcome this issue.')

        if nb > len(self._towers):
            raise TooManyTowersException(f'{nb} is more than the total amount of towers [{len(self._towers)}] supplied.')

    def __radius_generation(self, radius: int) -> None:
        """
        Generates the radius of the towers randomly

        Caped at the given maximum radius.
        """
        for i in range(len(self._towers)):
            self._towers[i].append(randint(5, radius))

    def get_towers(self) -> list[list[int]]:
        """
        Getter meant to return the towers as a list of integers.

        Should be used for debugging prints. Avoid printing the
        object directly since print() would implicitely call the
        __str__ method.
        """
        return self._towers


class Planes:
    """
    The Planes class meant to generate the planes

    Generates their start and end coordinates as well
    as their speed and takeoff timing, all according
    to the supplied arguments.
    """
    def __init__(self, towers: list[list[int]], planes: int,
                 floating: bool, duration: int, spawn: bool,
                 max_speed: int, min_speed: int) -> None:
        """
        The constructor that does all the setup from the
        supplied arguments.

        This class, in case of re-write of this code,
        is meant to be re-usable unlike the Towers one.
        Just call the generate_planes method to 're-do'
        the calculations. Please note that there is no
        built-in method to provide a new Data object.
        """
        self.__planes: list[list[Union[int, float]]] = []
        self.__increment: float = duration / planes
        self.__towers: list[list[int]] = towers
        self.__min_speed: int = min_speed
        self.__max_speed: int = max_speed
        self.__nb_planes: int = planes
        self.__boolean_management(floating, spawn)

    def __str__(self) -> str:
        """
        str operator overload to ease the transformation from list[list[int]] to str
        """
        return '\n'.join(['A ' + ' '.join(map(str, plane))
                          for plane in self.__planes])

    def __boolean_management(self, floating: bool, spawn: bool) -> None:
        """
        Method creating multiple function pointers to
        limit the comparisons during the generation
        of the planes.

        Setting floating to true will change the generating
        functions for the takeoff timing and the speed value
        to floating number generation.
        Setting spawn to True will set coordinates to random
        positions instead of the towers' position.
        """
        if floating is True:
            self.__takeoff = self.__floating_takeoff
            self.__random = uniform
        else:
            self.__takeoff = self.__integer_takeoff
            self.__random = randint
        if spawn is False:
            self.__spawns = self.__get_random_position
        else:
            self.__spawns = self.__get_random_towers

    def __generate_velocity(self, index: int) -> None:
        """
        Generates the speed value for a given plane.

        Generates the speed with a random function pointer (as defined in
        the boolean_management method). If floating, will round it to a single
        decimal.
        """
        self.__planes[index].append(round(self.__random(self.__min_speed, self.__max_speed), 1))

    def __get_random_towers(self) -> list[int]:
        """
        Get the position of two towers randomly chosen.

        After retrieving the two towers, removes their radius
        and returns them.
        """
        pos: list[int] = sum(sample(self.__towers, 2), [])
        return pos[0:2] + pos[3:5]

    def __get_random_position(self) -> list[int]:
        """
        Adds two x and y coordinates randomly on the forced
        1920*1080 map to a given plane as integers.
        """
        res: list[int] = []
        for pix in [1920, 1080] * 2:
            res.append(randint(0, pix))
        return res

    def __floating_takeoff(self, index: int, time_s: float) -> None:
        """
        Adds takeoff time to a given plane as a floating number.
        """
        self.__planes[index].append(time_s)

    def __integer_takeoff(self, index: int, time_s: float) -> None:
        """
        Adds takeoff time to a given plane as an integer.
        """
        self.__planes[index].append(round(time_s))

    def generate_planes(self) -> None:
        """
        Main method to generate planes.

        Calls each method once for each plane. This method is
        counter productive in terms of efficiency but adds
        readability and ease the debugging process. Should not
        be optimized to the cost of maintability.
        Takeoff time calculated in such way that planes take off
        in an uniform way over time. Which means that if you want
        to see 10 planes on the screen at the same time, with
        a 10s delay, you should ask for a hundred planes.
        """
        res: float = 0

        for i in range(self.__nb_planes):
            self.__planes.append(self.__spawns())
            self.__generate_velocity(i)
            self.__takeoff(i, res)
            res += self.__increment

    def get_planes(self) -> list[list[int]]:
        """
        Getter meant to return the planes as a list of integers.

        Should be used for debugging prints. Avoid printing the
        object directly since print() would implicitely call the
        __str__ method.
        """
        return self.__planes


class Manager:
    def __init__(self, args: Data) -> None:
        """
        Constructor to register the parsed arguments.

        Also sets the random seed, either generated or
        given as argument.
        """
        self._data: Data = args
        seed(self._data.seed)

    def generate_content(self) -> None:
        """
        Main method to generate the content of the file.

        Generates the towers, then the planes, giving
        each the necessary data as argument.
        """
        self.__towers = Towers(self._data.path,
                               self._data.towers,
                               self._data.radius)
        self.__planes = Planes(self.__towers.get_towers(),
                               self._data.planes,
                               self._data.floating,
                               self._data.duration,
                               self._data.spawn,
                               self._data.max_speed,
                               self._data.min_speed)
        self.__planes.generate_planes()

    def save_to_file(self) -> None:
        """
        Retrieves the data in planes and towers to save it
        as a file.

        The path of the file can be customized as argument
        but would explicit the planes and towers by default.
        """
        with open(self._data.output, 'w') as o:
            o.write(str(self.__planes) + '\n' + str(self.__towers))


if __name__ == "__main__":
    """
    Guarded context meant to call the public
    methods of the Parser and Manager classes

    This context is made for maintability purposes
    as it is of no use in its current state.
    Please only use this to add scripting elements
    to this file. For everything else, create children of
    the current classes or modify the current ones.
    """
    data = Parser.parse_args()
    m = Manager(data)
    m.generate_content()
    m.save_to_file()