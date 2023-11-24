class Layer:
    """ This is a 2D layer to be overlaid on top of the base image
    or other layers beneath it. You can have different types of
    layers, e.g., a DicomInfoLayer with basic DICOM attribute
    info, or a SegmentationMaskLayer with a binary mask. The latter
    should also have a readable name, e.g., "muscle", "SAT", "VAT,
    etc. Question is where do you set these names? Perhaps a layer
    AlbertaProtocolSegmentationMaskLayer where these names are 
    already predefined?
    The viewer should have a combobox for selecting the layer and
    setting its properties (remember these in QSettings!)
    """
    pass