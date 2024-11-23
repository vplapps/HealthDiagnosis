const diagnoseForm = document.getElementById('diagnose-form');
const resultDiv = document.getElementById('result');
const historyButton = document.getElementById('get-history');

// Визначаємо tbody таблиці для історії
const historyTableBody = document.querySelector('#history-table tbody');

diagnoseForm.addEventListener('submit', async (e) => {
    e.preventDefault();

    // Зчитування даних із форми
    const name = document.getElementById('name').value;
    const age = parseInt(document.getElementById('age').value, 10);
    const temperature = parseFloat(document.getElementById('temperature').value);
    const pressure = parseInt(document.getElementById('pressure').value, 10);
    const pulse = parseInt(document.getElementById('pulse').value, 10);
    const spo2 = parseInt(document.getElementById('spo2').value, 10);

    // Відправка POST-запиту до сервера
    try {
        const response = await fetch('/diagnose', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, age, temperature, pressure, pulse, spo2 }),
        });

        if (response.ok) {
            const data = await response.json();
            resultDiv.innerHTML = `
                <h3>Diagnosis Result:</h3>
                <p>Name: ${data.name}</p>
                <p>Age: ${data.age}</p>
                <p>Temperature: ${data.temperature}</p>
                <p>Pressure: ${data.pressure}</p>
                <p>Pulse: ${data.pulse}</p>
                <p>SpO2: ${data.spo2}</p>
                <p>Risk Level: ${data.risk_level}</p>
            `;
        } else {
            resultDiv.innerHTML = `<p>Error: Unable to get diagnosis</p>`;
        }
    } catch (error) {
        console.error('Error:', error);
        resultDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});

historyButton.addEventListener('click', async () => {
    try {
        // Надсилаємо GET-запит до маршруту /history
        const response = await fetch('/history');

        if (response.ok) {
            const data = await response.json();
            historyTableBody.innerHTML = ''; // Очищаємо таблицю перед додаванням нових записів

            data.forEach(record => {
                const row = document.createElement('tr');
                row.innerHTML = `
                    <td>${record.name}</td>
                    <td>${record.age}</td>
                    <td>${record.temperature}</td>
                    <td>${record.pressure}</td>
                    <td>${record.pulse}</td>
                    <td>${record.spo2}</td>
                    <td>${record.risk_level}</td>
                    <td>${record.created_at}</td>
                     <td><button class="delete-button" data-id="${record.id}">Delete</button></td>
                `;
                historyTableBody.appendChild(row);
            });
            // Додаємо обробник подій для кнопок "Delete"
            document.querySelectorAll('.delete-button').forEach(button => {
                button.addEventListener('click', async (e) => {
                    const recordId = e.target.getAttribute('data-id');
                    await deleteRecord(recordId);
                });
            });
        } else {
            alert('Error: Unable to fetch history');
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    }
});
// Функція для видалення запису
async function deleteRecord(recordId) {
    try {
        const response = await fetch(`/history/${recordId}`, { method: 'DELETE' });
        if (response.ok) {
            alert('Record deleted successfully');
            historyButton.click(); // Оновлюємо таблицю
        } else {
            alert('Error: Unable to delete record');
        }
    } catch (error) {
        console.error('Error:', error);
        alert(`Error: ${error.message}`);
    }
}