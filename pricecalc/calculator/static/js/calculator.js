document.addEventListener('DOMContentLoaded', function() {
    const categorySelect = document.getElementById('category');
    const productSelect = document.getElementById('product');
    const modifiersContainer = document.getElementById('modifiers-container');
    const basePriceDisplay = document.getElementById('base-price');
    const finalPriceDisplay = document.getElementById('final-price');

    let currentProduct = null;

    // Обработчик изменения категории
    categorySelect.addEventListener('change', async function() {
        const categoryId = this.value;
        if (!categoryId) {
            productSelect.disabled = true;
            productSelect.innerHTML = '<option value="">Сначала выберите категорию</option>';
            return;
        }

        try {
            const response = await fetch(`/api/category/${categoryId}/products/`);
            const data = await response.json();
            
            productSelect.innerHTML = '<option value="">Выберите товар</option>';
            data.products.forEach(product => {
                const option = document.createElement('option');
                option.value = product.id;
                option.textContent = product.name;
                productSelect.appendChild(option);
            });
            
            productSelect.disabled = false;
            modifiersContainer.innerHTML = '';
            basePriceDisplay.textContent = '0.00';
            finalPriceDisplay.textContent = '0.00';
        } catch (error) {
            console.error('Ошибка при загрузке товаров:', error);
            alert('Произошла ошибка при загрузке товаров');
        }
    });

    // Обработчик изменения товара
    productSelect.addEventListener('change', async function() {
        const productId = this.value;
        if (!productId) {
            modifiersContainer.innerHTML = '';
            basePriceDisplay.textContent = '0.00';
            finalPriceDisplay.textContent = '0.00';
            return;
        }

        try {
            const response = await fetch(`/calculator/product/${productId}/modifiers/`);
            const data = await response.json();
            
            modifiersContainer.innerHTML = '';
            data.modifiers.forEach(modifier => {
                const div = document.createElement('div');
                div.className = 'modifier-item';
                
                const checkbox = document.createElement('input');
                checkbox.type = 'checkbox';
                checkbox.id = `modifier-${modifier.id}`;
                checkbox.value = modifier.id;
                checkbox.addEventListener('change', calculateFinalPrice);
                
                const label = document.createElement('label');
                label.htmlFor = `modifier-${modifier.id}`;
                label.textContent = `${modifier.name} (${modifier.is_percentage ? modifier.price_adjustment + '%' : modifier.price_adjustment + ' ₽'})`;
                
                div.appendChild(checkbox);
                div.appendChild(label);
                modifiersContainer.appendChild(div);
            });
            
            // Получаем базовую цену товара
            const productResponse = await fetch(`/api/product/${productId}/`);
            const productData = await productResponse.json();
            currentProduct = productData;
            basePriceDisplay.textContent = productData.base_price;
            calculateFinalPrice();
        } catch (error) {
            console.error('Ошибка при загрузке модификаторов:', error);
            alert('Произошла ошибка при загрузке модификаторов');
        }
    });

    // Функция расчета итоговой цены
    async function calculateFinalPrice() {
        if (!currentProduct) return;

        const selectedModifiers = Array.from(document.querySelectorAll('input[type="checkbox"]:checked'))
            .map(checkbox => checkbox.value);

        try {
            const response = await fetch('/calculator/calculate/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/x-www-form-urlencoded',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: new URLSearchParams({
                    'product_id': currentProduct.id,
                    'modifiers[]': selectedModifiers
                })
            });

            const data = await response.json();
            if (data.success) {
                finalPriceDisplay.textContent = data.final_price;
            } else {
                throw new Error(data.error);
            }
        } catch (error) {
            console.error('Ошибка при расчете цены:', error);
            alert('Произошла ошибка при расчете цены');
        }
    }

    // Вспомогательная функция для получения CSRF токена
    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}); 