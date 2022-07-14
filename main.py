import argparse, os, sys
from PIL import Image

SIZE = (18,16)

def serialize_image(image:Image):
    pixels = image.load()
    output = []
    for i in range(16):
            if i %2 ==0:
                for j in range(18):
                    #print(j,i)
                    #print(pixels[j,i])
                    for k in range(3):
                        output.append(pixels[j,i][k])
            else:
                for j in reversed(range(18)):
                    for k in range(3):
                        output.append(pixels[j,i][k])
    return output

parser = argparse.ArgumentParser(description="Converts images and videos(spritesheets) into a format for loading onto the RGB display")

parser.add_argument('file', type=str, help="File to be converted")
parser.add_argument("--gamma", type=float, default=1.0, help="Gamma for image correction")
parser.add_argument("--fps", type=int, default=5, help="FPS for videos")
parser.add_argument("--output-format", type=str, default="c", choices=("c"), help="Output format")
def serialize(image):
    output=[]
    columns, rows = image.size[0]//SIZE[0], image.size[1]//SIZE[1]
    for row in range(rows):
        for column in range(columns):
            output.append(serialize_image(image.crop((column*SIZE[0],row*SIZE[1],(column+1)*SIZE[0],(row+1)*SIZE[1]))))
    return output

args = parser.parse_args()

if not os.path.exists(args.file):
    sys.stderr.write(f"error: file {args.file} not found")
    exit(1)

image = Image.open(args.file)
image = image.convert("RGB")
if image.size[0] % SIZE[0] != 0 or image.size[1] %SIZE[1] !=0:
    image=image.resize((18,16), Image.NEAREST)

pixels=image.load()
for i in range(image.size[1]):
    for j in range(image.size[0]):
        pixel=[0,0,0]
        for component in range(3):
            pixel[component]=round(pow(pixels[j,i][component]/255, (1/args.gamma))*255)
        pixels[j,i]=tuple(pixel)

if args.output_format == 'c':
    output=serialize(image)
    print(f"const uint8_t image_fps={args.fps};")
    print(f"const uint8_t image_number_frames={len(output)};")
    print(f"const uint8_t image_data[{len(output)}][{SIZE[0]*SIZE[1]*3}] PROGMEM={{")
    for frame in output[:-1]:
        print("{")
        for data in frame[:-1]:
            print(data, end=', ')
        print(frame[-1])
        print("},")
    frame=output[-1]
    print("{")
    for data in frame[:-1]:
        print(data, end=', ')
    print(frame[-1])
    print("}")
    print("};")
    











