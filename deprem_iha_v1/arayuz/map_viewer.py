from PyQt5.QtWidgets import QMainWindow, QGridLayout, QWidget
from PyQt5.QtWebEngineWidgets import QWebEngineView

class MapViewer(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()

        layout = QGridLayout()
        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        self.base64Icon = ''
        # ikon.txt dosyasının içeriğini okuyup bir değişkene atama
        try:
            with open('./gerekliler/ikon.txt', 'r', encoding='utf-8') as file:
                self.base64Icon += file.read()
                print("Dosya içeriği başarıyla okundu.")
        except FileNotFoundError:
            print("Dosya bulunamadı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

        

        self.base64IconDrone = ''
        # ikon.txt dosyasının içeriğini okuyup bir değişkene atama
        try:
            with open('./gerekliler/ikon2.txt', 'r', encoding='utf-8') as file:
                self.base64IconDrone += file.read()
                print("Dosya içeriği başarıyla okundu.")
        except FileNotFoundError:
            print("Dosya bulunamadı.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

        # İlk başta varsayılan bir konum belirle 
        self.latitude = 41.6354
        self.longitude = 32.4785


        # 26.963936090469357, 38.581175864454764

        self.web_view = QWebEngineView()
        layout.addWidget(self.web_view)
        self.load_map()

    def load_map(self):
        html_content = f"""
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Map Viewer</title>
            <style>
                body, html {{ margin: 0; padding: 0; width: 100%; height: 100%; }}
                #map {{
                    width: 100%;
                    height: 100%;
                    position: relative;
                    z-index: 1;
                }}
                #coordinate-box {{
                    position: absolute;
                    top: 10px;
                    left: 10px;
                    background-color: rgba(255, 255, 255, 0.7);
                    padding: 5px;
                    border-radius: 5px;
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    z-index: 1000;
                }}
                #buttons {{
                    position: absolute;
                    top: 10px;
                    right: 10px;
                    z-index: 1000;
                }}
                #add-destination-button, #clear-button {{
                    padding: 8px 15px;
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    margin-left: 5px;
                }}
                #clear-button {{
                    background-color: #dc3545;
                }}
                #coordinate-list {{
                    width: 200px;
                    height: 80%;
                    overflow-y: auto;
                    position: absolute;
                    top: 50px;
                    right: 10px;
                    padding: 10px;
                    background-color: rgba(255, 255, 255, 0.9);
                    border-radius: 5px;
                    font-family: Arial, sans-serif;
                    font-size: 12px;
                    z-index: 1000;
                    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
                }}
                #coordinate-list table {{
                    width: 100%;
                    border-collapse: collapse;
                }}
                #coordinate-list th, #coordinate-list td {{
                    padding: 8px;
                    text-align: left;
                    border-bottom: 1px solid #ddd;
                }}
                #coordinate-list th {{
                    background-color: #f2f2f2;
                    position: sticky;
                    top: 0;
                    z-index: 100;
                }}
                .rainbow:nth-child(odd) {{
                    background-color: #f9f9f9;
                }}
                .rainbow:nth-child(even) {{
                    background-color: #e9e9e9;
                }}
                .coordinate-item:hover {{
                    opacity: 0.75; 
                }}
                .altitude-input {{
                    margin-left: 10px;
                    width: 50px;
                }}
            </style>
        </head>
        <body>
            <div id="map"></div>
            <div id="coordinate-box">Koordinatlar: </div>
            <div id="buttons">
                <button id="clear-button">Temizle</button>
                <button id="add-destination-button">Varış Hedefi Ekle</button>
                <input type="number" id="altitude-input" placeholder="Yükseklik" class="altitude-input" />
            </div>
            <div id="coordinate-list">
                <table>
                    <thead>
                        <tr>
                            <th class="rainbow">#</th>
                            <th class="rainbow">X</th>
                            <th class="rainbow">Y</th>
                            <th class="rainbow">H</th>
                        </tr>
                    </thead>
                    <tbody id="coordinate-tbody">
                    </tbody>
                </table>
            </div>
            <script src="https://www.openlayers.org/en/v4.6.5/build/ol.js"></script>
            <script>
                var coordinateCounter = 1;
                var lastCoordinate = null;
                var vectorSource = new ol.source.Vector();
                var vectorLayer = new ol.layer.Vector({{
                    source: vectorSource
                }});

                var map = new ol.Map({{
                    target: 'map',
                    layers: [
                        new ol.layer.Tile({{
                            source: new ol.source.OSM()
                        }}),
                        new ol.layer.Tile({{
                            source: new ol.source.XYZ({{
                                url: 'https://mt1.google.com/vt/lyrs=s&x={{x}}&y={{y}}&z={{z}}',
                            }})
                        }}),
                        vectorLayer
                    ],
                    view: new ol.View({{
                        center: ol.proj.fromLonLat([{self.longitude}, {self.latitude}]),
                        zoom: 18
                    }})
                }});

                var staticIcon = new ol.Feature({{
                    
                    geometry: new ol.geom.Point(ol.proj.fromLonLat([0, 0])),
                    name: 'Drone'
                }});

                var staticIconStyle = new ol.style.Style({{
                    image: new ol.style.Icon({{
                        src: '{self.base64Icon}',
                        anchor: [0.5, 1], 
                        anchorXUnits: 'fraction',
                        anchorYUnits: 'fraction'
                    }})
                }});
                staticIcon.setStyle(staticIconStyle);

                vectorSource.addFeature(staticIcon);



                var droneIcon = new ol.Feature({{
                    geometry: new ol.geom.Point(ol.proj.fromLonLat([{self.longitude}, {self.latitude}])),
                    name: 'Static Icon'
                }});

                var droneIconStyle = new ol.style.Style({{
                    image: new ol.style.Icon({{
                        src: '{self.base64IconDrone}',
                        anchor: [0.5, 1], 
                        anchorXUnits: 'fraction',
                        anchorYUnits: 'fraction',
                        rotation: 0 // İlk başta sıfır derece olarak başlat
                    }})
                }});
                droneIcon.setStyle(droneIconStyle);

                vectorSource.addFeature(droneIcon);







                var lastClickedCoordinate = null;

                map.on('click', function(event) {{
                    var coord = ol.proj.toLonLat(event.coordinate);
                    document.getElementById('coordinate-box').innerText = 'Koordinatlar: ' + coord.map(c => c.toFixed(5)).join(', ');
                    lastClickedCoordinate = coord;

                    staticIcon.getGeometry().setCoordinates(event.coordinate);
                }});

                function calculateDistance(coord1, coord2) {{
                    function toRad(value) {{
                        return value * Math.PI / 180;
                    }}

                    var lat1 = coord1[1];
                    var lon1 = coord1[0];
                    var lat2 = coord2[1];
                    var lon2 = coord2[0];

                    var R = 6371e3;
                    var φ1 = toRad(lat1);
                    var φ2 = toRad(lat2);
                    var Δφ = toRad(lat2 - lat1);
                    var Δλ = toRad(lon2 - lon1);

                    var a = Math.sin(Δφ / 2) * Math.sin(Δφ / 2) +
                            Math.cos(φ1) * Math.cos(φ2) *
                            Math.sin(Δλ / 2) * Math.sin(Δλ / 2);
                    var c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));

                    var d = R * c;
                    return d;
                }}

                document.getElementById('add-destination-button').addEventListener('click', function() {{
                    if (!lastClickedCoordinate) return;

                    var altitude = document.getElementById('altitude-input').value;
                    var coordText = lastClickedCoordinate.map(c => c.toFixed(5)).join(',');
                    var coord = lastClickedCoordinate.map(c => c.toFixed(5));
                    var coordinateTbody = document.getElementById('coordinate-tbody');
                    var row = document.createElement('tr');
                    var cellCounter = document.createElement('td');
                    cellCounter.textContent = coordinateCounter;
                    var cellX = document.createElement('td');
                    cellX.textContent = coord[0];
                    var cellY = document.createElement('td');
                    cellY.textContent = coord[1];
                    var cellAltitude = document.createElement('td');
                    cellAltitude.textContent = altitude;

                    row.appendChild(cellCounter);
                    row.appendChild(cellX);
                    row.appendChild(cellY);
                    row.appendChild(cellAltitude);

                    coordinateTbody.appendChild(row);

                    var iconFeature = new ol.Feature({{
                        geometry: new ol.geom.Point(ol.proj.fromLonLat(coord.map(c => parseFloat(c))))
                    }});

                    var iconStyle = new ol.style.Style({{
                        image: new ol.style.Icon({{
                            src: '{self.base64Icon}',
                            anchor: [0.5, 1], 
                            anchorXUnits: 'fraction',
                            anchorYUnits: 'fraction'
                        }}),
                        text: new ol.style.Text({{
                            text: coordinateCounter.toString(),
                            font: '12px Calibri,sans-serif',
                            fill: new ol.style.Fill({{
                                color: '#000'
                            }}),
                            stroke: new ol.style.Stroke({{
                                color: '#fff',
                                width: 3
                            }}),
                            offsetY: -25  // Adjust this value to position the number correctly
                        }})
                    }});
                    iconFeature.setStyle(iconStyle);
                    vectorSource.addFeature(iconFeature);

                    if (lastCoordinate) {{
                        var coordinates1 = lastCoordinate.split(',').map(Number);
                        var coordinates2 = coord.map(Number);
                        var lineGeometry = new ol.geom.LineString([
                            ol.proj.fromLonLat(coordinates1),
                            ol.proj.fromLonLat(coordinates2)
                        ]);
                        var lineFeature = new ol.Feature({{
                            geometry: lineGeometry
                        }});
                        var lineStyle = new ol.style.Style({{
                            stroke: new ol.style.Stroke({{
                                color: '#FFA500',
                                width: 2
                            }}),
                            text: new ol.style.Text({{
                                text: (calculateDistance(coordinates1, coordinates2).toFixed(2) + ' m'),
                                overflow: true,
                                font: '12px Calibri,sans-serif',
                                fill: new ol.style.Fill({{
                                    color: '#000'
                                }}),
                                stroke: new ol.style.Stroke({{
                                    color: '#fff',
                                    width: 3
                                }}),
                                offsetY: -12
                            }})
                        }});
                        lineFeature.setStyle(lineStyle);
                        vectorSource.addFeature(lineFeature);
                    }}
                    lastCoordinate = coordText;
                    coordinateCounter++;
                }});

                document.getElementById('clear-button').addEventListener('click', function() {{
                    document.getElementById('coordinate-tbody').innerHTML = '';
                    vectorSource.clear();
                    vectorSource.addFeature(staticIcon); // Drone iconunu geri ekle
                    coordinateCounter = 1;
                    lastCoordinate = null;
                    lastClickedCoordinate = null;
                }});
            </script>
        </body>
        </html>
        """
        self.web_view.setHtml(html_content)

    # def update_konum(self, latitude, longitude):
    #     self.latitude = latitude
    #     self.longitude = longitude
    #     self.load_map()


    def update_konum(self, konum):
        try:
            latitude, longitude = map(float, konum.split(','))

            if latitude == 0 and longitude == 0:
                self.latitude = 38.581175864454764
                self.longitude = 26.963936090469357
            else:
                self.latitude = latitude
                self.longitude = longitude
            
            print(f"Map_viewer.py'de güncellenen konum: {self.latitude}, {self.longitude}")
            self.load_map()

        except ValueError:
            print("Geçersiz konum formatı.")
            self.latitude = 38.581175864454764
            self.longitude = 26.963936090469357
            
        except Exception as e:
            print(f"Hata oluştu: {e}")
            self.latitude = 38.581175864454764
            self.longitude = 26.963936090469357

    def update_konumDrone(self, konum,yaw):
        try:
            latitude, longitude = map(float, konum.split(','))
            self.yaw = yaw

            if latitude == 0 and longitude == 0:
                self.latitude = 38.581175864454764
                self.longitude = 26.963936090469357
            else:
                self.latitude = latitude
                self.longitude = longitude
            
            print(f"Map_viewer.py'de güncellenen DROne konum: {self.latitude}, {self.longitude}")
            print(f" YAW YAW YAW YAW YAW: {self.yaw}")
            self.web_view.page().runJavaScript(f"""
                var newCoordinates = ol.proj.fromLonLat([{self.longitude}, {self.latitude}]);
                var yaw = {self.yaw}; // Drone'un yaw değeri
                droneIcon.getGeometry().setCoordinates(newCoordinates);
                droneIcon.getStyle().getImage().setRotation(yaw * Math.PI / 180); // Yaw değerini radyana çevir ve uygulama
            """)

        except ValueError:
            print("Geçersiz konum formatı.")
            self.latitude = 38.581175864454764
            self.longitude = 26.963936090469357
            
        except Exception as e:
            print(f"Hata oluştu: {e}")
            self.latitude = 38.581175864454764
            self.longitude = 26.963936090469357
            