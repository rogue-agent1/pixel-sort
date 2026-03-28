#!/usr/bin/env python3
"""pixel_sort - Glitch art pixel sorting on PPM images."""
import argparse, sys

def read_ppm(path):
    with open(path) as f:
        assert f.readline().strip() == "P3"
        line = f.readline().strip()
        while line.startswith("#"): line = f.readline().strip()
        w, h = map(int, line.split())
        maxval = int(f.readline().strip())
        nums = []
        for line in f:
            nums.extend(int(x) for x in line.split())
        pixels = []
        for y in range(h):
            row = []
            for x in range(w):
                i = (y * w + x) * 3
                row.append((nums[i], nums[i+1], nums[i+2]))
            pixels.append(row)
        return pixels, w, h

def write_ppm(path, pixels, w, h):
    with open(path, "w") as f:
        f.write(f"P3\n{w} {h}\n255\n")
        for row in pixels:
            for r,g,b in row: f.write(f"{r} {g} {b} ")
            f.write("\n")

def brightness(p): return p[0]*0.299 + p[1]*0.587 + p[2]*0.114

def sort_rows(pixels, threshold=50):
    result = []
    for row in pixels:
        new_row = list(row)
        i = 0
        while i < len(row):
            j = i
            while j < len(row) and brightness(row[j]) > threshold: j += 1
            if j > i:
                segment = sorted(new_row[i:j], key=brightness)
                new_row[i:j] = segment
            i = j + 1
        result.append(new_row)
    return result

def main():
    p = argparse.ArgumentParser(description="Pixel sort glitch effect")
    p.add_argument("input")
    p.add_argument("-o","--output", default="sorted.ppm")
    p.add_argument("-t","--threshold", type=int, default=50)
    p.add_argument("-d","--direction", choices=["row","col"], default="row")
    a = p.parse_args()
    pixels, w, h = read_ppm(a.input)
    if a.direction == "row":
        pixels = sort_rows(pixels, a.threshold)
    else:
        cols = [[pixels[y][x] for y in range(h)] for x in range(w)]
        cols = sort_rows(cols, a.threshold)
        pixels = [[cols[x][y] for x in range(w)] for y in range(h)]
    write_ppm(a.output, pixels, w, h)
    print(f"Pixel-sorted {a.input} -> {a.output}")

if __name__ == "__main__": main()
