import io
from typing import List, Optional, Callable
from random import randint
import argparse


class Size:
    def __init__(self, *args, **kwargs):
        self._width = kwargs.pop("width", None)
        self._height = kwargs.pop("height", None)

        if self._width is None and self._height is None:
            if (len(args) == 1 and
                    isinstance(args[0], (list, tuple)) and
                    len(args[0]) == 2):
                self._width = args[0][0]
                self._height = args[0][1]
            elif (len(args) == 1 and
                    isinstance(args[0], Size)):
                self._width = args[0].width
                self._height = args[0].height
            elif (len(args) == 1 and
                    isinstance(args[0], str)):
                arg = args[0].replace('(', '').replace(')', '').split(',')
                if len(arg) == 2:
                    self._width = int(arg[0])
                    self._height = int(arg[1])

            elif len(args) == 2:
                self._width = args[0]
                self._height = args[1]

        if self._width is None or self._height is None:
            raise ValueError("Values of width and height not found")

    @property
    def width(self) -> int:
        return self._width

    @width.setter
    def width(self, value: int):
        self._width = value

    @property
    def height(self) -> int:
        return self._height

    @height.setter
    def height(self, value: int):
        self._height = value

    @property
    def area(self):
        return self._width * self._height

    def __getitem__(self, item) -> int:
        if item == 0 or item == 'width':
            return self._width
        elif item == 1 or item == 'height':
            return self._height
        raise KeyError("Size have only two values")

    def __repr__(self):
        return f"({self.width}, {self.height})"


class TrayGenerator:
    def __init__(self,
                 tray_size: Size,
                 num_blocks: Optional[int],
                 min_block_size: Size,
                 max_block_size: Size
                 ):
        self._tray_size = tray_size
        self._num_blocks = num_blocks
        self._min_block_size = min_block_size
        self._max_block_size = max_block_size

        if self._max_block_size.area > self._tray_size.area:
            raise ValueError("Max block area is bigger than tray area!")
        if self._min_block_size.area > self._max_block_size.area:
            raise ValueError("Min block area is bigger than max block area!")
        if (self._max_block_size.width > self._tray_size.width or
                self._max_block_size.width > self._tray_size.height or
                self._max_block_size.height > self._tray_size.width or
                self._max_block_size.height > self._tray_size.height):
            raise ValueError("One of max dimensions is bigger than tray dimension!")
        if self._min_block_size.width > self._max_block_size.width:
            raise ValueError("Min width is bigger than max width!")
        if self._min_block_size.height > self._max_block_size.height:
            raise ValueError("Min height is bigger than max height!")

    def generate_tray(self) -> List[Size]:
        blocks = []
        blocks_area = 0
        done = False
        while not done:
            width = randint(self._min_block_size.width, self._max_block_size.width)
            height = randint(self._min_block_size.height, self._max_block_size.height)
            blocks.append(Size(width, height))
            blocks_area += width * height

            if blocks_area > self._tray_size.area:
                done = True
            if self._num_blocks is not None:
                if len(blocks) >= self._num_blocks:
                    done = True

        return blocks

    def get_dump_function(self, file_type: str) -> Callable[[List[Size]], str]:
        func_map = {
            'simple': self.dump_data_simple,
            'cplex': self.dump_data_cplex,
        }
        return func_map[file_type]

    def dump_data_simple(self, blocks: List[Size]) -> str:
        data = io.StringIO()
        data.write(f"{self._tray_size.width} {self._tray_size.height} {len(blocks)}\n")
        for block in blocks:
            data.write(f"{block.width} {block.height}\n")
        contents = data.getvalue()
        data.close()
        return contents

    def dump_data_cplex(self, blocks: List[Size]) -> str:
        """
        Tray = [20, 20];
        NumElements = 20;
        Elements = [<3,2>,<2,4>,<5,3>,...];
        """
        data = io.StringIO()
        data.write(f"Tray = [{self._tray_size.width}, {self._tray_size.height}];\n")
        data.write(f"NumElements = {len(blocks)};\n")
        elements = ','.join([f"<{b.width},{b.height}>" for b in blocks])
        data.write(f"Elements = [{elements}];\n")
        contents = data.getvalue()
        data.close()
        return contents

    @staticmethod
    def save_data_to_file(data: str, file_name: str) -> bool:
        with open(file_name, 'w') as f:
            f.write(data)
        return True


def check_file_type(value):
    allowed_types = ['simple', 'cplex']
    if value not in allowed_types:
        raise argparse.ArgumentTypeError(f"{value} is not supported file type. "
                                         f"Choices are {allowed_types}.")
    return value


FORMAT_EXT = {
    'simple': 'txt',
    'cplex': 'dat',
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--tray_size",
                        metavar="WIDTH,HEIGHT",
                        required=True,
                        help="tray size")
    parser.add_argument("-m", "--min_block_size",
                        metavar="WIDTH,HEIGHT",
                        required=True,
                        help="minimum block size")
    parser.add_argument("-M", "--max_block_size",
                        metavar="WIDTH,HEIGHT",
                        required=True,
                        help="maximum block size")
    parser.add_argument("-n", "--num_blocks",
                        help="number of blocks per tray, if omitted - fill entire area",
                        type=int)
    parser.add_argument("-s", "--num_samples",
                        help="number of samples to generate, default=1 [TODO]",
                        type=int, default=1)
    parser.add_argument("-N", "--multiple_samples",
                        help="enable multiple samples in one file [TODO]",
                        action="store_true")
    parser.add_argument("-f", "--file_name",
                        help="output file name",
                        type=str, default="data.txt")
    parser.add_argument("-F", "--file_format",
                        help="output file format. Choices: simple, cplex. Default: simple",
                        default="simple",
                        nargs='+',
                        type=check_file_type)
    parser.add_argument("-o", "--stdout",
                        help="print data on stdout",
                        action="store_true")

    args = parser.parse_args()

    gen = TrayGenerator(Size(args.tray_size),
                        args.num_blocks,
                        Size(args.min_block_size),
                        Size(args.max_block_size))

    blocks = gen.generate_tray()

    for fmt in args.file_format:
        dump_function = gen.get_dump_function(fmt)
        data = dump_function(blocks)

        if args.stdout:
            print(data)
        else:
            gen.save_data_to_file(data, f"{args.file_name}.{FORMAT_EXT[fmt]}")


if __name__ == '__main__':
    main()
