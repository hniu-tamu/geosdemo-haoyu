"""Main module."""

import string
import random
import ipyleaflet

class Map(ipyleaflet.Map):

    def __init__(self, center, zoom, **kwargs) -> None:
        """Creates a Map instance."""

        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True
        super().__init__(center=center, zoom=zoom, **kwargs)

        if "layers_control" not in kwargs:
            kwargs["layers_control"] = True
        if kwargs["layers_control"]:
            self.add_layers_control()

        if "fullscreen_control" not in kwargs:
            kwargs["fullscreen_control"] = True

        if kwargs["fullscreen_control"]:
            self.add_fullscreen_control()

    def add_search_control(self, position = "topleft", **kwargs):
        """Adds a search control to the map.

        Args:
            kwargs: The keyword arguments of ipyleaflet.SearchControl.
        """

        if "url" not in kwargs:
            kwargs["url"] = "https://nominatim.openstreetmap.org/search?format=json&q={s}"

        
        search_control = ipyleaflet.SearchControl(position=position, **kwargs)
        self.add_control(search_control)

    def add_draw_control(self, position = "topleft", **kwargs):
        """Adds a draw control to the map.
        
        Args: Keyword arguments to pass to the draw control.
        """

        if "edit" not in kwargs:
            kwargs["edit"] = True

        draw_control = ipyleaflet.DrawControl(position=position, **kwargs)
        draw_control.polyline =  {
            "shapeOptions": {
                "color": "#6bc2e5",
                "weight": 8,
                "opacity": 1.0
            }
        }
        draw_control.polygon = {
            "shapeOptions": {
                "fillColor": "#6be5c3",
                "color": "#6be5c3",
                "fillOpacity": 1.0
            },
            "drawError": {
                "color": "#dd253b",
                "message": "Oups!"
            },
            "allowIntersection": False
        }
        draw_control.circle = {
            "shapeOptions": {
                "fillColor": "#efed69",
                "color": "#efed69",
                "fillOpacity": 1.0
            }
        }
        draw_control.rectangle = {
            "shapeOptions": {
                "fillColor": "#fca45d",
                "color": "#fca45d",
                "fillOpacity": 1.0
            }
        }

        self.add_control(draw_control)


    def add_layers_control(self, position = "topright"):
        """Adds a layers control to the map.
        
        Args: Keyword arguments to pass to the layers control.
        """

        layers_control = ipyleaflet.LayersControl(position=position)
        self.add_control(layers_control)

    def add_fullscreen_control(self, position = "bottomright"):
        """Adds a fullscreen control to the map.
        
        Args: Keyword arguments to pass to the fullscreen control.
        """

        fullscreen_control = ipyleaflet.FullScreenControl(position=position)
        self.add_control(fullscreen_control)

    def add_tile_layer(self, url, name, attribution="", **kwargs):
        """Adds a tile layer to the map.
        
        Args:
            url (str): The tile layer URL.
            name (str): The tile layer name.
            attribution (str): The tile layer attribution.
            kwargs: The keyword arguments of ipyleaflet.TileLayer.
        """

        tile_layer = ipyleaflet.TileLayer(url=url, name=name, attribution=attribution, **kwargs)
        self.add_layer(tile_layer)

    def add_basemap(self, basemap, **kwargs):
        """Adds a basemap to the map.
        
        Args:
            basemap (str): The basemap name.
            kwargs: The keyword arguments of ipyleaflet.TileLayer.
        """
        import xyzservices.providers as xyz

        if basemap.lower() == "roadmap":
            url = "http://mt0.google.com/vt/lyrs=m&hl=en&x={x}&y={y}&z={z}"
            self.add_tile_layer(url, name=basemap, **kwargs)
        elif basemap.lower() == "satellite":
            url = "http://mt0.google.com/vt/lyrs=s&hl=en&x={x}&y={y}&z={z}"
            self.add_tile_layer(url, name=basemap, **kwargs)

        else:
            try:
                basemap = eval(f"xyz.{basemap}")
                url = basemap.build_url()
                attribution = basemap.attribution
                self.add_tile_layer(url, name=basemap.name, attribution=attribution, **kwargs)
            except:
                raise ValueError(f"Basemap '{basemap}' not found.")



def get_random_string(length=10, upper=False, digits=False):
    """Generate a random string of fixed length.

    Args:
        length (int, optional): The length of the string. Defaults to 10.
        upper (bool, optional): Whether to include uppercase letters. Defaults to False.
        digits (bool, optional): Whether to include digits. Defaults to False.

    Returns:
        str: The random string.
    """    
    letters = string.ascii_lowercase
    if upper:
        letters = letters + string.ascii_uppercase
    if digits:
        letters = letters + string.digits
    print(letters)
    return ''.join(random.choice(letters) for i in range(length))


def get_lucky_number(length=1):
    """generate a random number of fixed length.

    Args:
        length (int, optional): The length of the number. Defaults to 1.

    Returns:
        int: the random number.
    """    
    result = ''.join(random.choice(string.digits) for i in range(length))
    return int(result)
