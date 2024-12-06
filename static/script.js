const content = document.getElementById('content');
let currentPage = 1;
let totalPages = 1;
const pageSize = 15; // Кількість записів на сторінку

document.getElementById('listCarsBtn').addEventListener('click', () => listCars(currentPage));
document.getElementById('getCarBtn').addEventListener('click', getCarForm);
document.getElementById('addCarBtn').addEventListener('click', addCarForm);
document.getElementById('updateCarBtn').addEventListener('click', updateCarForm);
document.getElementById('deleteCarBtn').addEventListener('click', deleteCarForm);

async function listCars(page) {
    currentPage = page;
    const response = await fetch(`/api/cars/limited?page=${page}&limit=${pageSize}`);
    const data = await response.json();
    const cars = data.cars;
    totalPages = data.totalPages;

    const list = document.createElement('ul');
    cars.forEach(car => {
        const item = document.createElement('li');
        item.textContent = `${car.car_number} - ${car.brand} - ${car.status} - ${car.owner_surname}`;
        list.appendChild(item);
    });

    // Оновлюємо вміст контейнера тільки списком
    content.innerHTML = '<h2>Car List (Pagination)</h2>';
    content.appendChild(list);

    // Відображення пагінації
    const pagination = document.createElement('div');
    pagination.classList.add('pagination');

    let paginationButtons = '';
    const range = 2; // Відстань до поточної сторінки (відображаємо 5 сторінок)

    // Кнопка "First"
    paginationButtons += `<button onclick="listCars(1)" ${currentPage === 1 ? 'disabled' : ''}>First</button>`;
    // Кнопка "Previous"
    paginationButtons += `<button onclick="listCars(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''}>Previous</button>`;

  
    let startPage = Math.max(1, currentPage - range);
    let endPage = Math.min(totalPages, currentPage + range);

    if (endPage - startPage < 4) {
        if (startPage === 1) {
            endPage = Math.min(totalPages, startPage + 4);
        } else {
            startPage = Math.max(1, endPage - 4);
        }
    }

    for (let i = startPage; i <= endPage; i++) {
        paginationButtons += `<button onclick="listCars(${i})" ${currentPage === i ? 'class="active"' : ''}>${i}</button>`;
    }


    paginationButtons += `<button onclick="listCars(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''}>Next</button>`;

    paginationButtons += `<button onclick="listCars(${totalPages})" ${currentPage === totalPages ? 'disabled' : ''}>Last</button>`;

    pagination.innerHTML = paginationButtons;
    content.appendChild(pagination);
}

// Форма для отримання одного автомобіля
function getCarForm() {
    content.innerHTML = `
        <h2>Get Car by Number</h2>
        <input id="carNumberInput" type="text" placeholder="Enter car number">
        <button onclick="getCar()">Get Car</button>
        <div id="message"></div> <!-- Контейнер для повідомлень -->
    `;
}

async function getCar() {
    const carNumber = document.getElementById('carNumberInput').value;
    const response = await fetch(`/api/cars/${carNumber}`);
    const car = await response.json();

    const message = document.getElementById('message');
    
    if (car.car_number) {
        message.textContent = `${car.car_number} - ${car.brand} - ${car.status} - ${car.owner_surname}`;
        message.style.color = 'black';

    } else {
        message.textContent = 'Car not found';  // Виведення повідомлення
        message.style.color = 'red';
    }
}

// Форма для додавання нового автомобіля
function addCarForm() {
    content.innerHTML = `
        <h2>Add New Car</h2>
        <input id="carNumber" type="text" placeholder="Car Number">
        <input id="brand" type="text" placeholder="Brand">
        <select id="status">
            <option value="Викрадений">Викрадений</option>
            <option value="Знайдений">Знайдений</option>
        </select>
        <input id="ownerSurname" type="text" placeholder="Owner Surname">
        <button onclick="addCar()">Add Car</button>
        <div id="message"></div> <!-- Контейнер для повідомлень -->
    `;
}

async function addCar() {
    const carData = {
        car_number: document.getElementById('carNumber').value,
        brand: document.getElementById('brand').value,
        status: document.getElementById('status').value,
        owner_surname: document.getElementById('ownerSurname').value,
    };

    const response = await fetch('/api/cars', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(carData),
    });

    const message = document.getElementById('message');
    
    if (response.ok) {
        message.textContent = 'Car added successfully!';
        message.style.color = 'green';
    } else {
        message.textContent = 'Error adding car.';
        message.style.color = 'red';
    }
}

// Форма для оновлення автомобіля
function updateCarForm() {
    content.innerHTML = `
        <h2>Update Car</h2>
        <input id="updateCarNumber" type="text" placeholder="Car Number">
        <input id="updateBrand" type="text" placeholder="Brand">
        <select id="updateStatus">
            <option value="Викрадений">Викрадений</option>
            <option value="Знайдений">Знайдений</option>
        </select>
        <input id="updateOwnerSurname" type="text" placeholder="Owner Surname">
        <button onclick="updateCar()">Update Car</button>
        <div id="message"></div> <!-- Контейнер для повідомлень -->
    `;
}

async function updateCar() {
    const carNumber = document.getElementById('updateCarNumber').value;
    const carData = {
        brand: document.getElementById('updateBrand').value,
        status: document.getElementById('updateStatus').value,
        owner_surname: document.getElementById('updateOwnerSurname').value,
    };

    const response = await fetch(`/api/cars/${carNumber}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(carData),
    });

    const message = document.getElementById('message');
    
        // Перевірка результату запиту
    if (response.ok) {
        // Якщо запит успішний, виводимо повідомлення про успіх
        message.textContent = 'Car updated successfully!';
        message.style.color = 'green';
    } else {
        // Якщо запит неуспішний, виводимо повідомлення про помилку
        const errorResponse = await response.json();
        console.log(errorResponse);// Отримуємо деталі помилки з відповіді
        message.textContent = `${errorResponse.detail || 'Unknown error'}`;
        message.style.color = 'red';
    }

}

// Форма для видалення автомобіля
function deleteCarForm() {
    content.innerHTML = `
        <h2>Delete Car</h2>
        <input id="deleteCarNumber" type="text" placeholder="Car Number">
        <button onclick="deleteCar()">Delete Car</button>
        <div id="message"></div> <!-- Контейнер для повідомлень -->
    `;
}

async function deleteCar() {
    const carNumber = document.getElementById('deleteCarNumber').value;
    const response = await fetch(`/api/cars/${carNumber}`, {
        method: 'DELETE',
    });

    const message = document.getElementById('message');
    
    if (response.ok) {
        message.textContent = 'Car deleted successfully!';
        message.style.color = 'green';
    } else {
        message.textContent = 'Error deleting car.';
        message.style.color = 'red';
    }
}
