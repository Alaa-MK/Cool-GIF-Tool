from PIL import Image, ImageSequence, ImageDraw
import numpy as np

OUTPUT_N_FRAMES = 6
STRIP_WIDTH = 1

def get_frames(img):    
    frames = []
    for frame in ImageSequence.Iterator(img):
        frames.append(np.array(frame))
    return frames[0:len(frames):len(frames)//OUTPUT_N_FRAMES]

def create_image(frames):
    n_frames = len(frames)
    size = frames[0].shape
    pixels = np.empty((0, size[0]))
    frames_trans = [np.transpose(a) for a in frames]
    for i in range(0,size[0], STRIP_WIDTH):
        frame = frames_trans[i%n_frames]
        for j in range(STRIP_WIDTH):
            pixels = np.append(pixels, [frame[i+j]], axis=0)
    return Image.fromarray(np.uint(pixels)).rotate(-90).convert('RGB')
    
def create_mask(size, n_frames):
    img = Image.new('RGBA', size, (0,0,0,255))
    draw = ImageDraw.Draw(img)
    for i in range(0, size[0], STRIP_WIDTH * n_frames):
        for j in range(STRIP_WIDTH):
            draw.line(((i+j, 0), (i+j, size[1]-1)), (0,0,0,0))
    return img
        
def main():
    img = Image.open('examples/spiral.gif')
    frames = get_frames(img)
    create_image(frames).save('img.png')
    create_mask(img.size, len(frames)).save('mask.png')
        
    
    
    
if __name__ == '__main__':
    main()