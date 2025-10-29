document.getElementById('generateForm').addEventListener('submit', async (e) => {
    e.preventDefault();

    const style = document.getElementById('style').value;
    const description = document.getElementById('description').value;

    // Скрываем плейсхолдер
    document.getElementById('placeholderBox').style.display = 'none';

    // Показываем индикатор загрузки
    document.getElementById('loadingMessage').classList.remove('d-none');
    document.getElementById('errorMessage').classList.add('d-none');
    document.getElementById('resultContainer').classList.add('d-none');
    document.getElementById('btnSpinner').classList.remove('d-none');
    document.getElementById('btnText').textContent = 'ГЕНЕРАЦИЯ...';
    document.querySelector('button[type="submit"]').disabled = true;

    try {
        const response = await fetch('/generate', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ style, description })
        });

        const data = await response.json();

        if (data.success) {
            // Корректируем путь, если /static отсутствует
            let imageUrl = data.image_url;
            if (!imageUrl.startsWith('/static/')) {
                imageUrl = '/static' + (imageUrl.startsWith('/') ? imageUrl : '/' + imageUrl);
            }

            // Показываем результат
            document.getElementById('imageResult').src = imageUrl;
            document.getElementById('downloadLink').href = imageUrl;
            document.getElementById('resultContainer').classList.remove('d-none');
        } else {
            // Показываем ошибку
            document.getElementById('errorMessage').textContent = data.error;
            document.getElementById('errorMessage').classList.remove('d-none');
            // Возвращаем плейсхолдер при ошибке
            document.getElementById('placeholderBox').style.display = 'block';
        }
    } catch (error) {
        document.getElementById('errorMessage').textContent = 'Произошла ошибка: ' + error.message;
        document.getElementById('errorMessage').classList.remove('d-none');
        // Возвращаем плейсхолдер при ошибке
        document.getElementById('placeholderBox').style.display = 'block';
    } finally {
        // Скрываем индикатор загрузки
        document.getElementById('loadingMessage').classList.add('d-none');
        document.getElementById('btnSpinner').classList.add('d-none');
        document.getElementById('btnText').textContent = 'ГЕНЕРИРОВАТЬ';
        document.querySelector('button[type="submit"]').disabled = false;
    }
});