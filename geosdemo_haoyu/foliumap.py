import folium

class Map(folium.Map):
    """Create a folium map object.

    Args:
        folium (_type_): _description_
    """    

    def __init__(self, center = [20, 0], zoom=2, **kwargs) -> None:
        """Creates a Map instance.
        
        Args:
            center (list, optional): The center of the map.
            zoom (int, optional): The zoom level of the map.
        
        """

        super().__init__(location=center, zoom_start=zoom, **kwargs)

    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.

        Args:
            name: The name of the tile layer.
            attribution: The attribution of the tile layer.
        """

        tile_layer = folium.TileLayer(
            tiles = url,
            name=name, 
            attr=attribution,
            **kwargs
        )

        self.add_child(tile_layer)