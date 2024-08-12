(async function() {
    const NUM_SAMPLES = 40;  // Количество сэмплов в каждом батче
    const NUM_BATCHES = 10;  // Количество батчей для анализа
    const DELAY = 10;        // Задержка между сэмплингом в миллисекундах
    const WITH_ANGLES = 1;
    const count_dublicates_max = 1;//10;
    let allData = [];        // Список всех собранных батчей
    let batch = [];          // Текущий батч данных
    let previous_lines = [];
    let repeat_count = 0;
    let lastPositions = Array(NUM_SAMPLES).fill(null);
    let lastIndex = 0;
    let lastMousePosition = { x: null, y: null };
    

    // Загрузка модели TensorFlow.js
    const model = await tf.loadLayersModel('model.json');

    const calculateAngle = (v1, v2) => {
        const dot = v1.x * v2.x + v1.y * v2.y;
        const mag1 = Math.sqrt(v1.x * v1.x + v1.y * v1.y);
        const mag2 = Math.sqrt(v2.x * v2.x + v2.y * v2.y);
        if (mag1 === 0 || mag2 === 0) return 0;
        return Math.acos(Math.max(-1, Math.min(1, dot / (mag1 * mag2)))) ;//* (180 / Math.PI);
    };
    // Нормализуем координаты мыши
    const getNormalizedMousePosition = (event) => {
        const screenX = window.screenX;
        const screenY = window.screenY;
        const innerWidth = window.innerWidth;
        const innerHeight = window.innerHeight;
        const outerHeight = window.outerHeight;

        const mouseX = event.screenX;
        const mouseY = event.screenY;

        let normalizedX = (mouseX - screenX) / innerWidth;
        let normalizedY = 1 - ((mouseY - screenY - (outerHeight - innerHeight)) / innerHeight);

        normalizedX = Math.max(0, Math.min(1, normalizedX));
        normalizedY = Math.max(0, Math.min(1, normalizedY));

        return { x: normalizedX, y: normalizedY };
    };

    // Анализ предсказаний модели
    const analyzePrediction = (prediction) => {
        // Извлекаем данные из тензора
        const y_pred_prob = prediction.arraySync(); // Преобразуем в массив
        const average_probability = y_pred_prob.reduce((p,c,_,a) => p + c/a.length,0);
        const max_probability = Math.max.apply(Math, y_pred_prob);

        
        const y_pred = y_pred_prob.map(prob => prob[0] > 0.5 ? 1 : 0); // Применяем порог
        //console.log(y_pred_prob, average_probability, max_probability)
    
        return {
            average_probability: average_probability , // Убедитесь, что значения не `undefined`
            majority_vote: y_pred.reduce((a, b) => a + b, 0) / y_pred.length > 0.5,
            max_probability: max_probability,  // Убедитесь, что значения не `undefined`
            weighted_vote: average_probability > 0.5, // Убедитесь, что значения не `undefined`
            final_decision: (y_pred.reduce((a, b) => a + b, 0) / y_pred.length) > 0.5
        };
    };
    

    const displayResult = (result) => {
        const resultDiv = document.getElementById('results');
        console.log(1)
        if (resultDiv) {
            const resultText = `
                Average Probability: ${result.average_probability}<br>
                Majority Vote: ${result.majority_vote ? "Bot" : "Human"}<br>
                Max Probability: ${result.max_probability}<br>
                Weighted Vote: ${result.weighted_vote ? "Bot" : "Human"}<br>
                Final Decision: ${result.final_decision ? "Bot" : "Human"}
            `;
            const resultParagraph = document.createElement('p');
            resultParagraph.innerHTML = resultText;
            resultDiv.appendChild(resultParagraph);
        }
    };

    // Анализ всех батчей
    const analyzeAllBatches = async (allBatches) => {
        const tensorData = allBatches.map(batch => {
            return batch.map((pos, index) => {
                if (WITH_ANGLES === 1) {
                    if (index === 0) {
                        return [pos.x, pos.y, 0]; // Первый элемент углов всегда 0
                    }
                    const prev = batch[index - 1];
                    const next = batch[index + 1] || pos; // Следующий элемент или текущий, если следующего нет
                    const v1 = { x: pos.x - prev.x, y: pos.y - prev.y };
                    const v2 = { x: next.x - pos.x, y: next.y - pos.y };
                    const angle = calculateAngle(v1, v2);
                    console.log(angle);
                    return [pos.x, pos.y, angle];
                } else {
                    // Без углов
                    return [pos.x, pos.y];
                }
            });
        });
    
        // Преобразуем данные в тензор
        const inputData = tf.tensor3d(tensorData, [NUM_BATCHES, NUM_SAMPLES, WITH_ANGLES === 1 ? 3 : 2]);
    
        // Вывод входных данных для проверки
        inputData.array().then(array => {
            console.log('Input Data:', array);
        }).catch(error => {
            console.error('Error retrieving input data:', error);
        });
    
        // Получаем предсказание модели
        const prediction = model.predict(inputData);
    
        // Проверка и вывод предсказаний
        const result = await prediction.array().then(array => {
            console.log('Prediction:', array);
            return analyzePrediction(prediction);
        }).catch(error => {
            console.error('Error retrieving prediction data:', error);
            return {};
        });
    
        return result;
    };
    // Обновление счётчика батчей
    const updateBatchCounter = (batchCount) => {
        const batchCounter = document.getElementById('batch-counter');
        if (batchCounter) {
            batchCounter.textContent = `Batches Collected: ${batchCount}`;
        }
    };

    // Основная функция для отслеживания мыши
    const trackMouse = async () => {
        const currentPosition = lastMousePosition;

        if (currentPosition.x === null || currentPosition.y === null) {
            setTimeout(trackMouse, DELAY);
            return;
        }

        lastPositions[lastIndex % NUM_SAMPLES] = currentPosition;
        lastIndex += 1;

        // Проверяем, движется ли курсор
        const isStationary = new Set(lastPositions.map(pos => JSON.stringify(pos))).size === 1;
        if (isStationary) {
            setTimeout(trackMouse, DELAY);
            return;
        }
        let tmp = 0;
        // Собираем данные в батч
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
            console.log(batch);
            allData.push(batch);
            updateBatchCounter(allData.length);

            if (allData.length >= NUM_BATCHES) {
                const result = await analyzeAllBatches(allData);
                displayResult(result);
                allData = []; // Очищаем данные после анализа
                //console.log('Max number of batches reached and analyzed.');
            }

            batch = []; // Очищаем текущий батч
        }

        setTimeout(trackMouse, DELAY);
    };

    // Событие движения мыши
    document.addEventListener('mousemove', function(event) {
        const newMousePosition = getNormalizedMousePosition(event);
        if (newMousePosition.x !== lastMousePosition.x || newMousePosition.y !== lastMousePosition.y) {
            lastMousePosition = newMousePosition;
        }
    });

    setTimeout(trackMouse, DELAY);
})();
