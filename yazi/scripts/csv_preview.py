#!/usr/bin/env python3
import csv, sys, unicodedata

RESET  = '\033[0m'
BOLD   = '\033[1m'
DIM    = '\033[2m'
CYAN   = '\033[36m'
YELLOW = '\033[33m'

def cw(s):
    """Display width of a string, accounting for CJK double-width chars."""
    return sum(2 if unicodedata.east_asian_width(c) in ('W', 'F') else 1 for c in s)

def pad(s, width):
    return s + ' ' * max(0, width - cw(s))

def main():
    path = sys.argv[1]
    max_rows = int(sys.argv[2]) if len(sys.argv) > 2 else 50

    with open(path, newline='', encoding='utf-8', errors='replace') as f:
        rows = list(csv.reader(f))

    if not rows:
        return

    # Flatten multiline cell values
    rows = [[cell.replace('\r\n', ' ').replace('\n', ' ').replace('\r', ' ') for cell in row] for row in rows]

    # Limit rows for performance
    display_rows = rows[:max_rows + 1]
    col_count = max(len(r) for r in display_rows)
    headers = display_rows[0]

    # Calculate column widths
    widths = [0] * col_count
    for row in display_rows:
        for i, cell in enumerate(row):
            if i < col_count:
                widths[i] = max(widths[i], cw(cell))

    # Build separator
    sep = DIM + '+' + '+'.join('-' * (w + 2) for w in widths) + '+' + RESET

    def fmt_row(row, is_header=False):
        cells = []
        for i in range(col_count):
            cell = row[i] if i < len(row) else ''
            content = ' ' + pad(cell, widths[i]) + ' '
            if is_header:
                cells.append(BOLD + CYAN + content + RESET)
            else:
                cells.append(content)
        pipe = DIM + '|' + RESET
        return pipe + pipe.join(cells) + pipe

    print(sep)
    print(fmt_row(headers, is_header=True))
    print(sep)
    for row in display_rows[1:]:
        print(fmt_row(row))
    print(sep)

if __name__ == '__main__':
    main()
