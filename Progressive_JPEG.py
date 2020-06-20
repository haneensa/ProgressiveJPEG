
# coding: utf-8

# In[9]:


from PIL import ImageFile  # pip install Pillow
ImageFile.LOAD_TRUNCATED_IMAGES = True
import cStringIO
from PIL import Image
import ssim # pip install pyssim
import base64
import io 
import struct
import math

def get_image(data):
    photo_b64 = base64.b64encode(bytearray(data))
    msg = base64.b64decode(photo_b64)
    buf = io.BytesIO(msg)
    return Image.open(buf)
    
def showImage(block, h, w):
    img = get_image(block)
    img = img.resize((w, h))
   
    img.show()
    
    return img
def compute_similarity(img1, img2):
    return ssim.compute_ssim(img1, img2)

def create_blocks(image_name, blocksize):
    blocks = []
    with open(image_name, "rb") as imageFile:
        bfile = imageFile.read()
        nblocks = int( math.ceil( len(bfile) / float(blocksize) ) )
        for i in range(nblocks):
            left = i * blocksize
            right = (i + 1) * blocksize
            block = bfile[left: right]
            blocks.append(block)
    return blocks

img_fname ="progressive.jpg"
blocksize = 20*1024 # create blocks from img where each of size 'blocksize'

blocks = create_blocks(img_fname, blocksize)
original_img = "".join(blocks)
img1 = get_image(original_img)


# In[14]:



# how many blocks to include
prefix = 1 #TODO: change this from 1 to len(blocks)-1 to see how each block improves quality
reconstruct_img = "".join(blocks[0:prefix])
h = 1000
w = 1000
img = showImage(reconstruct_img, h, w)
#img.save("img_prefix_%s.jpg" %prefix)


# In[11]:


# To get the utility of incrementing the prefix value, we use  Structural Similarity Index (SSIM)    

img2 = get_image(reconstruct_img)
# TODO: as you change the prefix value, see how the utility changes
utility = compute_similarity(img1, img2)
print("Utility of %s blocks is %s" % (prefix, utility) )

