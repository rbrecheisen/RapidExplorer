class Layer:
    """ This is a 2D layer to be overlaid on top of the base image
    or other layers beneath it. You can have different types of
    layers, e.g., a DicomAttributeLayer with basic DICOM attribute
    info, or a SegmentationMaskLayer with a binary mask. The latter
    should also have a readable name, e.g., "muscle", "SAT", "VAT,
    etc. Question is where do you set these names? Perhaps a layer
    AlbertaProtocolSegmentationMaskLayer where these names are 
    already predefined?
    The viewer should have a combobox for selecting the layer and
    setting its properties (remember these in QSettings!)
    """
    def __init__(self, name: str, index: int=-1, opacity: float=0.5, visible: bool=True) -> None:
        self._name = name
        self._index = index
        self._opacity = opacity
        self._visible = visible

    def name(self) -> str:
        return self._name
    
    def index(self) -> int:
        return self._index
    
    def setIndex(self, index: int) -> None:
        self._index = index

    def opacity(self) -> float:
        return self._opacity
    
    def setOpacity(self, opacity) -> None:
        self._opacity = opacity

    def visible(self) -> bool:
        return self._visible
    
    def setVisible(self, visible) -> None:
        self._visible = visible