import json

import time
import argparse
import shutil
from json import JSONDecodeError
from pathlib import Path


def _parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Tool to merge logfiles.')

    parser.add_argument(
        'input1',
        metavar='<INPUT FILE1>',
        type=str,
        help='path to first logfile',
    )

    parser.add_argument(
        'input2',
        metavar='<INPUT FILE2>',
        type=str,
        help='path to second logfile',
    )

    parser.add_argument(
        '-o', '--output',
        metavar='<OUTPUT FILE>',
        type=str,
        help='path to merged logfile',
    )

    parser.add_argument(
        '-f', '--force',
        action='store_const',
        const=True,
        default=False,
        help='force write logs',
        dest='force_write',
    )

    return parser.parse_args()


def _create_dir(dir_path: Path, *, force_write: bool = False) -> None:
    if dir_path.exists():
        if not force_write:
            raise FileExistsError(f'Dir "{dir_path}" already exists. Remove it first or choose another one.')
        shutil.rmtree(dir_path)

    dir_path.mkdir(parents=True)


def _convert_string_to_json(line: str) -> dict:
    try:
        return json.loads(line)
    except JSONDecodeError:
        raise ValueError('One of the input files does not match the JSON format') from None


def _merge_logfiles(log_filepath1: Path, log_filepath2: Path, merged_filepath: Path) -> None:
    print(f"merging {log_filepath1.name} and {log_filepath2.name} into {merged_filepath.name}...")

    with log_filepath1.open('r') as f1, log_filepath2.open('r') as f2, merged_filepath.open('wb') as g:
        write = g.write
        line1, line2 = f1.readline(), f2.readline()
        if line1 and line2:
            json1, json2 = _convert_string_to_json(line1), _convert_string_to_json(line2)
        while line1 or line2:
            if not line2 or line1 and json1['timestamp'] < json2['timestamp']:
                write(json.dumps(json1).encode('utf-8') + b'\n')
                line1 = f1.readline()
                if line1:
                    json1 = _convert_string_to_json(line1)
            else:
                write(json.dumps(json2).encode('utf-8') + b'\n')
                line2 = f2.readline()
                if line2:
                    json2 = _convert_string_to_json(line2)


def main() -> None:
    args = _parse_args()

    t0 = time.time()
    input_file1, input_file2 = Path(args.input1), Path(args.input2)
    output_file = Path(args.output)
    _create_dir(output_file.parent, force_write=args.force_write)
    _merge_logfiles(input_file1, input_file2, output_file)
    print(f"finished in {time.time() - t0:0f} sec")


if __name__ == '__main__':
    main()
