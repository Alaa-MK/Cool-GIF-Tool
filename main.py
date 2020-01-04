from PIL import Image, ImageSequence, ImageDraw
import numpy as np

OUTPUT_N_FRAMES = 6

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
    for i in range(size[0]):
        frame = frames_trans[i%n_frames]
        pixels = np.append(pixels, [frame[i]], axis=0)
    return Image.fromarray(np.uint(pixels)).rotate(-90).convert('RGB')
    
def create_mask(size, n_frames):
    img = Image.new('RGBA', size, (0,0,0,255))
    draw = ImageDraw.Draw(img)
    for i in range(0, size[0], n_frames):
        draw.line(((i, 0), (i, size[1]-1)), (0,0,0,0))
    return img
        
def main():
    img = Image.open('examples/spiral.gif')
    frames = get_frames(img)
    create_image(frames).save('img.png')
    create_mask(img.size, len(frames)).save('mask.png')
        
    
    
    
if __name__ == '__main__':
    main()