(function() {
    const DELAY_AFTER_CLICK = 0; // Задержка после клика, перед перемещением кнопки

    // Функция перемещения кнопки в случайное место
    const moveButtonRandomly = () => {
        const button = document.getElementById('random-button');
        if (!button) return;

        // Вычисляем доступное пространство для перемещения кнопки
        const maxX = window.innerWidth - button.offsetWidth;
        const maxY = window.innerHeight - button.offsetHeight;

        // Генерируем случайные координаты
        const randomX = Math.random() * maxX;
        const randomY = Math.random() * maxY;

        // Устанавливаем новые координаты кнопки
        button.style.left = `${randomX}px`;
        button.style.top = `${randomY}px`;
    };

    // Обработчик клика по кнопке
    const onButtonClick = () => {
        setTimeout(moveButtonRandomly, DELAY_AFTER_CLICK);
    };

    // Инициализация
    document.addEventListener('DOMContentLoaded', () => {
        const button = document.getElementById('random-button');
        if (button) {
            button.addEventListener('click', onButtonClick);
            moveButtonRandomly(); // Перемещаем кнопку при загрузке страницы
        }
    });
})();
