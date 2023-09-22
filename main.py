from PIL import Image, ImageOps
import numpy as np
import math
import time
import os
import cv2
#import pygame

# Open File

try: 
    main_image = Image.open("input.png")
except FileNotFoundError:
    main_image = Image.open("input.jpg")

# Setup

def init(s : int = 501):
    global width, height, main_image, image_array
    width, height = main_image.size
    left = (width - min([width, height])) // 2
    top = 0
    right = left + min([width, height])
    bottom = top + min([width, height])
    main_image = main_image.crop((left, top, right, bottom)).resize((s, s))
    width, height = s, s
    main_image = ImageOps.grayscale(main_image)
    image_array = np.array(main_image)
    
def nail_position(nail : int, max_nail: int, size : int = 501):
    theta = (nail / max_nail) * 2 * math.pi
    x, y = int(round(math.cos(theta) * (size // 2) + (size // 2))), int(round(math.sin(theta) * (size // 2) + (size // 2)))
    return (x, y)

def error_comp(array_1 : np.ndarray, array_2 : np.ndarray, size : int):
    #return np.sum(np.absolute(array_1 - array_2)) 
    return cv2.norm(array_1, array_2, cv2.NORM_L2) / (size * size * 100)

def dda(start : tuple, end : tuple, size : int = 501, thickness : int = 5):
    dx, dy = end[0] - start[0], end[1] - start[1]
    output = np.zeros((size, size), np.uint8)
    if abs(dx) > abs(dy):
        steps = abs(dx)
    else:
        steps = abs(dy)
    if (steps == 0):
        return output
    inc = (dx / steps, dy / steps)
    x, y = start[0], start[1]
    output[x][y] = thickness
    for v in range(steps):
        x += inc[0]
        y += inc[1]
        output[int(round(x))][int(round(y))] += thickness
    return output

def to_time(seconds):
    s = seconds % 60
    return f"{int((seconds // 60) // 60)} hours, {int((seconds // 60) % 60)} minutes and {int(seconds % 60)} seconds"

def processing(nail_count : int = 3600):
    global width, height, main_image, image_array
    start_processing = time.time()
    canvas = np.zeros(image_array.shape, np.uint8)
    nail_pos = [nail_position(i, nail_count, width) for i in range(nail_count)]

    # Greedy Approach

    for nail in range(nail_count):
        sn = nail
        minimal = error_comp(canvas, image_array, width)
        min_able = True
        os.system('cls')
        while min_able:
            print(f"Starting nail: {nail + 1} / {nail_count}")
            print(f"Current min: {minimal}")
            min_able = False
            en = -1
            min_line = None
            for next in range(nail_count):
                if next == sn:
                    continue
                line = dda(nail_pos[sn], nail_pos[next], width)
                check = np.clip(np.add(canvas, line), 0, 255)
                err = error_comp(check, image_array, width)
                if err < minimal:
                    minimal = err
                    min_able = True
                    en = next
                    min_line = line
            if min_able:
                os.system('cls')
                print(f"Add string from nail {sn} to {en}")
                sn = en
                canvas = np.clip(np.add(canvas, min_line), 0, 255)
    end_processing = time.time()
    print(to_time(end_processing - start_processing))
    output = Image.fromarray(canvas)
    output.save("result.png")

# Begin

if __name__ == "__main__":
    init(251)
    processing(1000)