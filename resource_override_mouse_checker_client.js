(function() {
    const NUM_SAMPLES = 40;
    const NUM_BATCHES = 10000;
    const NUM_STATIONARY_CHECKS = 30;
    const STATUS = "browser"; //or bot
    const DELAY = 10;
    const count_dublicates_max = 1;
    let allData = [];
    let batch = [];
    let repeat_count = 0;
    let previous_lines = [];
    let lastPositions = Array(NUM_STATIONARY_CHECKS).fill(null);
    let lastIndex = 0;
    let lastMousePosition = { x: null, y: null };

    // Получаем смещение и размерности браузера
    

    const getNormalizedMousePosition = (event) => {
        const screenX = window.screenX;
        const screenY = window.screenY;
        const innerWidth = window.innerWidth;
        const innerHeight = window.innerHeight;
        const outerHeight = window.outerHeight;
    
        // Координаты мыши относительно экрана
        const mouseX = event.screenX;
        const mouseY = event.screenY;
    
        // Нормализованные координаты относительно нижней левой границы окна браузера
        let normalizedX = (mouseX - screenX) / innerWidth;
        let normalizedY = 1 - ((mouseY - screenY - (outerHeight - innerHeight)) / innerHeight);
    
        // Ограничиваем значения в пределах [0, 1]
        normalizedX = Math.max(0, Math.min(1, normalizedX));
        normalizedY = Math.max(0, Math.min(1, normalizedY));
    
        return { x: normalizedX, y: normalizedY };
    };

    
    
    function sendDataToServer(data, type) {
        const siteURL = window.location.href;  // Получаем URL текущего сайта
        const payload = { data, siteURL };     // Оборачиваем данные и URL в один объект

        fetch(`http://127.0.0.1:5000/save_mouse_data_${type}`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(payload)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP error! Status: ${response.status}`);
            }
            return response.json();
        })
        .then(result => {
            // Ничего не выводим
        })
        .catch(error => {
            // Ничего не выводим
        });
    }





    function trackMouse() {
        const currentPosition = lastMousePosition;

        if (currentPosition.x === null || currentPosition.y === null) {
            setTimeout(trackMouse, DELAY);
            return;
        }

        lastPositions[lastIndex % NUM_STATIONARY_CHECKS] = currentPosition;
        lastIndex += 1;

        //console.log('Current Position:', currentPosition);
        //console.log('Last Positions:', lastPositions);

        // Проверяем, не статичен ли курсор
        if (new Set(lastPositions.map(pos => JSON.stringify(pos))).size === 1) {
            //console.log('Mouse is stationary.');
            setTimeout(trackMouse, DELAY);
            return;
        }
        let tmp = 0;
        // Добавляем данные в текущий батч
        if (batch.length < NUM_SAMPLES) {
            if (repeat_count >= count_dublicates_max - 1) {
                if (JSON.stringify(currentPosition) === JSON.stringify(previous_lines[previous_lines.length - 1])) {
                    tmp = 1;
                } else {
                    previous_lines = [];
                    repeat_count = 0;
                }
            }
            if (previous_lines.length === 0 || JSON.stringify(currentPosition) !== JSON.stringify(previous_lines[previous_lines.length - 1])) {
                repeat_count = 0;
            } else if (JSON.stringify(currentPosition) === JSON.stringify(previous_lines[previous_lines.length - 1])) {
                repeat_count++;
            }
            if (tmp === 0){
                batch.push(currentPosition);
                previous_lines.push(currentPosition);
                
            }
            tmp = 0;
        } else {
            if (batch.length === NUM_SAMPLES) {  
                allData.push(batch);
                //console.log(`Batch collected, total batches: ${allData.length}`);
                sendDataToServer([batch], STATUS); // Отправляем только текущий батч

                if (allData.length >= NUM_BATCHES) {
                    //console.log('Max number of batches reached.');
                    allData = [];
                }
                batch = []; // Очищаем текущий батч
            }
        }

        setTimeout(trackMouse, DELAY);
    }

    document.addEventListener('mousemove', function(event) {
        const newMousePosition = getNormalizedMousePosition(event);
        if (newMousePosition.x !== lastMousePosition.x || newMousePosition.y !== lastMousePosition.y) {
            lastMousePosition = newMousePosition;
        }
    });

    setTimeout(trackMouse, DELAY);
})();
