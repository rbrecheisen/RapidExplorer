from widgets.viewers.dicomviewer.layer import Layer


class TagLayer(Layer):
    def __init__(self) -> None:
        super(TagLayer, self).__init__(name='tag')