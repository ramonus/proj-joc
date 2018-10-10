from PIL import Image
import numpy as np
image = Image.open("roguelikeCity.png")
iarr = np.array(image)

ni = iarr.copy()
print(iarr.shape)
# Horitzontal
for i in range(iarr.shape[0],0,-17):
    if i != iarr.shape[0]:
        print("Deleting column:",i)
        ni = np.delete(ni,i,0)
# Vertical
for i in range(iarr.shape[1],0,-17):
    if i != iarr.shape[1]:
        print("Deleting file:",i)
        ni = np.delete(ni,i,1)
print("ni.shape:",ni.shape)
im = Image.fromarray(ni)
im.save("nomargins.png")
im.show()