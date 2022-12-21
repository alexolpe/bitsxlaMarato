import numpy as np
from imageio import imread
from matplotlib import pyplot as plt
import morphsnakes as ms

def example_nodule(img, xStart, yStart):

        img = img[..., 0] / 255.0

        gimg = ms.inverse_gaussian_gradient(img, alpha=1000, sigma=5.48)

        print("example: ",xStart, yStart, "imgshape: ", img.shape)

        init_ls = ms.circle_level_set(img.shape, (yStart, xStart), 10)

        return ms.morphological_geodesic_active_contour(gimg, iterations=230,
                                                 init_level_set=init_ls,
                                                 smoothing=1, threshold=0.5,
                                                 balloon=1)
                                            


if __name__ == '__main__':
    example_nodule()
    plt.show()
