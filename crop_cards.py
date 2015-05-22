from Pillow import Image
import glob, os

for infile in glob.glob('c:/Users/guest/Desktop/cards/*.jpg'):
    source = Image.open(infile)
    o1 = source.crop((85, 20, 772, 1009))
    o2 = source.crop((771, 20, 1458, 1009))
    o_path = 'c:/Users/guest/Desktop/o_cards/'
    name = os.path.basename(infile)
    o1.save(o_path + name + ".card1.jpg")
    o2.save(o_path + name + ".card2.jpg")
