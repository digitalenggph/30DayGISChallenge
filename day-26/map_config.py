config = {
  "version": "v1",
  "config": {
    "visState": {
      "filters": [
        
      ],
      "layers": [
        {
          "id": "llmo95f",
          "type": "trip",
          "config": {
            "dataId": "QC Bus Routes",
            "columnMode": "geojson",
            "label": "QC Bus Routes",
            "color": [
              221,
              178,
              124
            ],
            "highlightColor": [
              252,
              242,
              26,
              255
            ],
            "columns": {
              "geojson": "_geojson"
            },
            "isVisible": True,
            "visConfig": {
              "opacity": 0.8,
              "thickness": 1.5,
              "colorRange": {
                "colors": [
                  "#A6CEE3",
                  "#1F78B4",
                  "#B2DF8A",
                  "#33A02C",
                  "#FB9A99",
                  "#E31A1C",
                  "#FDBF6F",
                  "#FF7F00"
                ],
                "name": "Paired",
                "type": "qualitative",
                "category": "ColorBrewer",
                "colorLegends": {
                  "#A6CEE3": "1: QC Hall - Cubao",
                  "#FF7F00": "8: QC Hall - Muñoz",
                  "#1F78B4": "2: QC Hall - Litex",
                  "#B2DF8A": "3: Welcome Rotonda - Aurora-Katipunan",
                  "#33A02C": "4: QC Hall - Gen. Luis Ave.",
                  "#FB9A99": "5: QC Hall - Mindanao Ave.",
                  "#E31A1C": "6: QC Hall - Gilmore",
                  "#FDBF6F": "7: QC Hall - Ortigas Ave."
                }
              },
              "trailLength": 180,
              "fadeTrail": True,
              "billboard": False,
              "sizeRange": [
                0,
                10
              ]
            },
            "hidden": False,
            "textLabel": [
              {
                "field": None,
                "color": [
                  255,
                  255,
                  255
                ],
                "size": 18,
                "offset": [
                  0,
                  0
                ],
                "anchor": "start",
                "alignment": "center",
                "outlineWidth": 0,
                "outlineColor": [
                  255,
                  0,
                  0,
                  255
                ],
                "background": False,
                "backgroundColor": [
                  0,
                  0,
                  200,
                  255
                ]
              }
            ]
          },
          "visualChannels": {
            "colorField": {
              "name": "route_num",
              "type": "string"
            },
            "colorScale": "ordinal",
            "sizeField": None,
            "sizeScale": "linear"
          }
        },
        {
          "id": "q0cr946",
          "type": "point",
          "config": {
            "dataId": "Stations",
            "columnMode": "points",
            "label": "Stations",
            "color": [
              119,
              110,
              87
            ],
            "highlightColor": [
              252,
              242,
              26,
              255
            ],
            "columns": {
              "lat": "lat",
              "lng": "lon"
            },
            "isVisible": True,
            "visConfig": {
              "radius": 10,
              "fixedRadius": False,
              "opacity": 0.8,
              "outline": False,
              "thickness": 2,
              "strokeColor": None,
              "colorRange": {
                "colors": [
                  "#A6CEE3",
                  "#1F78B4",
                  "#B2DF8A",
                  "#33A02C",
                  "#FB9A99",
                  "#E31A1C",
                  "#FDBF6F",
                  "#FF7F00"
                ],
                "name": "Paired",
                "type": "qualitative",
                "category": "ColorBrewer",
                "colorLegends": {
                  "#A6CEE3": "Route 1 Stations",
                  "#1F78B4": "Route 2 Stations",
                  "#B2DF8A": "Route 3 Stations",
                  "#33A02C": "Route 4 Stations",
                  "#FB9A99": "Route 5 Stations",
                  "#E31A1C": "Route 6 Stations",
                  "#FDBF6F": "Route 7 Stations",
                  "#FF7F00": "Route 8 Stations"
                }
              },
              "strokeColorRange": {
                "name": "Global Warming",
                "type": "sequential",
                "category": "Uber",
                "colors": [
                  "#4C0035",
                  "#880030",
                  "#B72F15",
                  "#D6610A",
                  "#EF9100",
                  "#FFC300"
                ]
              },
              "radiusRange": [
                0,
                50
              ],
              "filled": True,
              "billboard": False,
              "allowHover": True,
              "showNeighborOnHover": False,
              "showHighlightColor": True
            },
            "hidden": False,
            "textLabel": [
              
            ]
          },
          "visualChannels": {
            "colorField": {
              "name": "route_num",
              "type": "string"
            },
            "colorScale": "ordinal",
            "strokeColorField": None,
            "strokeColorScale": "quantile",
            "sizeField": None,
            "sizeScale": "linear"
          }
        },
        {
          "id": "27ovdze",
          "type": "geojson",
          "config": {
            "dataId": "Quezon City Boundary",
            "columnMode": "geojson",
            "label": "Quezon City Boundary",
            "color": [
              23,
              184,
              190
            ],
            "highlightColor": [
              252,
              242,
              26,
              255
            ],
            "columns": {
              "geojson": "_geojson"
            },
            "isVisible": True,
            "visConfig": {
              "opacity": 0.8,
              "strokeOpacity": 0.8,
              "thickness": 0.5,
              "strokeColor": [
                227,
                26,
                26
              ],
              "colorRange": {
                "name": "Global Warming",
                "type": "sequential",
                "category": "Uber",
                "colors": [
                  "#4C0035",
                  "#880030",
                  "#B72F15",
                  "#D6610A",
                  "#EF9100",
                  "#FFC300"
                ]
              },
              "strokeColorRange": {
                "name": "Global Warming",
                "type": "sequential",
                "category": "Uber",
                "colors": [
                  "#4C0035",
                  "#880030",
                  "#B72F15",
                  "#D6610A",
                  "#EF9100",
                  "#FFC300"
                ]
              },
              "radius": 10,
              "sizeRange": [
                0,
                10
              ],
              "radiusRange": [
                0,
                50
              ],
              "heightRange": [
                0,
                500
              ],
              "elevationScale": 5,
              "stroked": True,
              "filled": False,
              "enable3d": False,
              "wireframe": False,
              "fixedHeight": False
            },
            "hidden": False,
            "textLabel": [
              {
                "field": None,
                "color": [
                  255,
                  255,
                  255
                ],
                "size": 18,
                "offset": [
                  0,
                  0
                ],
                "anchor": "start",
                "alignment": "center",
                "outlineWidth": 0,
                "outlineColor": [
                  255,
                  0,
                  0,
                  255
                ],
                "background": False,
                "backgroundColor": [
                  0,
                  0,
                  200,
                  255
                ]
              }
            ]
          },
          "visualChannels": {
            "colorField": None,
            "colorScale": "quantile",
            "strokeColorField": None,
            "strokeColorScale": "quantile",
            "sizeField": None,
            "sizeScale": "linear",
            "heightField": None,
            "heightScale": "linear",
            "radiusField": None,
            "radiusScale": "linear"
          }
        }
      ],
      "effects": [
        
      ],
      "interactionConfig": {
        "tooltip": {
          "fieldsToShow": {
            "Quezon City Boundary": [
              {
                "name": "fid",
                "format": None
              },
              {
                "name": "id",
                "format": None
              },
              {
                "name": "adm1_psgc",
                "format": None
              },
              {
                "name": "adm2_psgc",
                "format": None
              },
              {
                "name": "adm3_psgc",
                "format": None
              }
            ],
            "Stations": [
              {
                "name": "route_num",
                "format": None
              }
            ],
            "QC Bus Routes": [
              {
                "name": "id",
                "format": None
              },
              {
                "name": "route_num",
                "format": None
              },
              {
                "name": "route_name",
                "format": None
              },
              {
                "name": "schedule_day",
                "format": None
              },
              {
                "name": "trip_number",
                "format": None
              }
            ]
          },
          "compareMode": False,
          "compareType": "absolute",
          "enabled": True
        },
        "brush": {
          "size": 0.5,
          "enabled": False
        },
        "geocoder": {
          "enabled": False
        },
        "coordinate": {
          "enabled": False
        }
      },
      "layerBlending": "subtractive",
      "overlayBlending": "screen",
      "splitMaps": [
        
      ],
      "animationConfig": {
        "currentTime": 1737695700000,
        "speed": 0.1
      },
      "editor": {
        "features": [
          
        ],
        "visible": True
      }
    },
    "mapState": {
      "bearing": 24,
      "dragRotate": True,
      "latitude": 14.651497672713772,
      "longitude": 121.04701841794154,
      "pitch": 50,
      "zoom": 11.850577870134927,
      "isSplit": False,
      "isViewportSynced": True,
      "isZoomLocked": False,
      "splitMapViewports": [
        
      ]
    },
    "mapStyle": {
      "styleType": "dark-matter",
      "topLayerGroups": {
      },
      "visibleLayerGroups": {
        "label": False,
        "road": True,
        "border": False,
        "building": True,
        "water": True,
        "land": True,
        "3d building": False
      },
      "threeDBuildingColor": [
        15.035172933000911,
        15.035172933000911,
        15.035172933000911
      ],
      "backgroundColor": [
        0,
        0,
        0
      ],
      "mapStyles": {
        
      }
    },
    "uiState": {
      "mapControls": {
        "mapLegend": {
          "active": True,
          "settings": {
            "position": {
              "x": 38,
              "anchorX": "right",
              "y": 30,
              "anchorY": "bottom"
            },
            "contentHeight": 412
          }
        }
      }
    }
  }
}