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
            
    def add_geojson(self, data, name='GeoJSON', **kwargs):
        """Adds a GeoJSON layer to the map.
        
        Args:
            data (dict): The GeoJSON data.
            style (dict, optional): The style of the GeoJSON features. Defaults to None.
            hover_style (dict, optional): The hover style of the GeoJSON features. Defaults to None.
            name (str, optional): The name of the GeoJSON layer. Defaults to None.
            kwargs: The keyword arguments of ipyleaflet.GeoJSON.
        """

        if isinstance(data, str):
            import json
            with open(data, "r") as f:
                data = json.load(f)

        geo_json = ipyleaflet.GeoJSON(data=data, name=name, **kwargs)
        self.add_layer(geo_json)

    def add_shp(self, data, name='Shapefile', **kwargs):
        """Adds a shapefile to the map.
        
        Args:
            in_shp (str): The input shapefile.
            name (str, optional): The name of the shapefile. Defaults to 'Shapefile'.
            kwargs: The keyword arguments of ipyleaflet.GeoData.
        """

        import geopandas as gpd

        gdf = gpd.read_file(data)
        geojson = gdf.__geo_interface__
        self.add_geojson(geojson, name=name, **kwargs)

    def add_raster(self, url, name='Raster', fit_bounds=True, **kwargs):
        """Adds a raster layer to the map.
        
        Args:
            url (str): The raster URL.
            name (str, optional): The name of the raster layer. Defaults to 'Raster'.
            fit_bounds (bool, optional): Whether to fit the map to the extent of the raster. Defaults to True.
            kwargs: The keyword arguments of ipyleaflet.ImageOverlay.
        """
        import httpx

        titiler_endpoint = "https://titiler.xyz"

        r = httpx.get(
            f"{titiler_endpoint}/cog/info",
            params = {
                "url": url,
            }
        ).json()

        bounds = r["bounds"]
        
        r = httpx.get(
            f"{titiler_endpoint}/cog/tilejson.json",
            params = {
                "url": url,
            }
        ).json()

        tile = r["tiles"][0]

        self.add_tile_layer(url=tile, name=name, **kwargs)

        if fit_bounds:
            bbox = [[bounds[1], bounds[0]], [bounds[3], bounds[2]]]
            self.fit_bounds(bbox)

    def add_local_raster(self, filename, name='Local raster', **kwargs):

        try:
            import localtileserver
        except ImportError:
            raise ImportError("Please install localtileserver to add local raster.")





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
