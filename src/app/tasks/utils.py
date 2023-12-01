import numpy as np


def getPixels(p, normalize=False):
    pixels = p.pixel_array
    if not normalize:
        return pixels
    if normalize is True:
        return p.RescaleSlope * pixels + p.RescaleIntercept
    if isinstance(normalize, int):
        return (pixels + np.min(pixels)) / (np.max(pixels) - np.min(pixels)) * normalize
    if isinstance(normalize, list):
        return (pixels + np.min(pixels)) / (np.max(pixels) - np.min(pixels)) * normalize[1] + normalize[0]
    return pixels


def calculate_area(labels, label, pixel_spacing):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    area = np.sum(mask) * (pixel_spacing[0] * pixel_spacing[1]) / 100.0
    return area


def calculate_mean_radiation_attenuation(image, labels, label):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    subtracted = image * mask
    mask_sum = np.sum(mask)
    if mask_sum > 0.0:
        mean_ra = np.sum(subtracted) / np.sum(mask)
    else:
        print('Sum of mask pixels is zero, return zero radiation attenuation')
        mean_ra = 0.0
    return mean_ra
