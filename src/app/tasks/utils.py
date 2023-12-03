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


def calculateArea(labels, label, pixelSpacing):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    area = np.sum(mask) * (pixelSpacing[0] * pixelSpacing[1]) / 100.0
    return area


def calculateMeanRadiationAttennuation(image, labels, label):
    mask = np.copy(labels)
    mask[mask != label] = 0
    mask[mask == label] = 1
    subtracted = image * mask
    maskSum = np.sum(mask)
    if maskSum > 0.0:
        meanRadiationAttenuation = np.sum(subtracted) / np.sum(mask)
    else:
        print('Sum of mask pixels is zero, return zero radiation attenuation')
        meanRadiationAttenuation = 0.0
    return meanRadiationAttenuation
