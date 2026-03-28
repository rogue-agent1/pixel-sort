#!/usr/bin/env python3
"""Pixel sorting on PPM images — glitch art effect."""
import sys, struct

def read_ppm(path):
    with open(path, 'rb') as f:
        assert f.readline().strip() == b'P6'
        line = f.readline()
        while line.startswith(b'#'): line = f.readline()
        w, h = map(int, line.split())
        f.readline()  # max val
        data = f.read()
    pixels = []
    for y in range(h):
        row = []
        for x in range(w):
            i = (y*w+x)*3
            row.append((data[i], data[i+1], data[i+2]))
        pixels.append(row)
    return w, h, pixels

def write_ppm(path, w, h, pixels):
    with open(path, 'wb') as f:
        f.write(f'P6\n{w} {h}\n255\n'.encode())
        for row in pixels:
            for r,g,b in row: f.write(bytes([r,g,b]))

def brightness(pixel): return sum(pixel)/3

def sort_rows(pixels, threshold=50, reverse=False):
    result = []
    for row in pixels:
        # Find spans above threshold and sort them
        sorted_row = list(row); i = 0
        while i < len(row):
            if brightness(row[i]) > threshold:
                j = i
                while j < len(row) and brightness(row[j]) > threshold: j += 1
                span = sorted(sorted_row[i:j], key=brightness, reverse=reverse)
                sorted_row[i:j] = span
                i = j
            else: i += 1
        result.append(sorted_row)
    return result

if __name__ == '__main__':
    if len(sys.argv) < 2: print("Usage: pixel_sort.py <input.ppm> [output.ppm] [-t threshold] [--reverse]"); sys.exit(1)
    w, h, pixels = read_ppm(sys.argv[1])
    out = sys.argv[2] if len(sys.argv) > 2 and not sys.argv[2].startswith('-') else 'sorted.ppm'
    threshold = int(sys.argv[sys.argv.index('-t')+1]) if '-t' in sys.argv else 80
    rev = '--reverse' in sys.argv
    sorted_pixels = sort_rows(pixels, threshold, rev)
    write_ppm(out, w, h, sorted_pixels)
    print(f"Pixel sorted {w}x{h} → {out} (threshold={threshold})")
