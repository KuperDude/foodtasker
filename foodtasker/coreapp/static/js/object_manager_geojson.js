function createLegendItem(color, description) {
    const legendItem = document.createElement('div');
    legendItem.className = 'legend-item';

    const colorBox = document.createElement('div');
    colorBox.className = 'color-box';
    colorBox.style.backgroundColor = color;

    const desc = document.createElement('span');
    desc.className = 'description';
    desc.textContent = description;

    legendItem.appendChild(colorBox);
    legendItem.appendChild(desc);
    return legendItem;
}

ymaps.ready(function () {

    var map = new ymaps.Map('map', {
            center: [37.6156, 55.7522],
            zoom: 10,
            controls: ['zoomControl']
        }),
        objectManager = new ymaps.ObjectManager({
            clusterize: false,
            gridSize: 32,
            clusterIconColor: '#ff0000',
            clusterIconShape: 'circle',
            clusterDisableClickZoom: true
        });
    map.controls.get('zoomControl').options.set({size: 'small'});
    // Загружаем GeoJSON файл, экспортированный из Конструктора карт.
    $.getJSON(geojsonUrl)
        .done(function (geoJson) {

            geoJson.features.forEach(function (obj) {
                // Проверяем тип геометрии и настраиваем опции соответственно
                if (obj.geometry.type === 'Polygon') {
                    obj.options = {
                        fillColor: obj.properties.fill || '#0000FF', // Синий по умолчанию
                        fillOpacity: obj.properties['fill-opacity'] || 0.5,
                        strokeColor: obj.properties.stroke || '#000000', // Черный по умолчанию
                        strokeWidth: obj.properties['stroke-width'] || 1,
                        strokeOpacity: obj.properties['stroke-opacity'] || 1
                    };

                    const color = obj.properties.fill || '#0000FF';
                    const description = obj.properties.description;
                    const legendItem = createLegendItem(color, description);
                    document.getElementById('legend-content').appendChild(legendItem);
                } else if (obj.geometry.type === 'Point') {
                    if (obj.properties.iconCaption == restaurantName) {
                        obj.options = {
                            iconColor: '#00FF00'
                        };

                        map.setCenter(obj.geometry.coordinates);
                    } else {
                        
                        obj.options = {
                            iconColor: obj.properties['marker-color'] || '#FF0000'
                        };
                    }
                    
                }

                obj.properties.balloonContent = obj.properties.description;
            });
            // Добавляем описание объектов в формате JSON в менеджер объектов.
            objectManager.add(geoJson);
            // Добавляем объекты на карту.
            map.geoObjects.add(objectManager);
        });
});
