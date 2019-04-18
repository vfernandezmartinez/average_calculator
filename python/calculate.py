import sys
from urllib.request import urlopen


def read_remote_file(url, chunk_size=65536):
    with urlopen(url) as response:
        while True:
            chunk = response.read(chunk_size)
            if chunk:
                yield chunk
            else:
                break


def read_multiple_lines_from_url(url):
    last_line = b''

    for chunk in read_remote_file(url):
        lines = (last_line + chunk).split(b'\n')
        last_line = lines.pop()
        yield lines

    if last_line:
        yield [last_line]


def calculate_average(url, column_name):
    column_index = None
    total_lines = 0
    column_sum = 0

    for lines in read_multiple_lines_from_url(url):
        total_lines += len(lines)
        for line in lines:
            if column_index:
                column_sum += float(line.split(b',')[column_index])
            else:
                column_names = line.split(b',')
                column_index = column_names.index(column_name.encode('ascii'))

    if total_lines:
        return total_lines, column_sum / total_lines


if __name__ == "__main__":
    line_count, average_tip = calculate_average(sys.argv[1], 'tip_amount')

    print('Line count:', line_count)
    print('Average tip_amount:', average_tip)