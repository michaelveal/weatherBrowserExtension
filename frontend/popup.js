// Add an event listener to the "Get Current Weather" button
document.getElementById('currentWeatherBtn').addEventListener('click', function() {
    // Get the location entered by the user
    const location = document.getElementById('location').value;
    
    // Fetch the current weather data from the backend server
    fetch(`http://localhost:5000/current_weather?location=${location}`)
        .then(response => response.json())  // Parse the response as JSON
        .then(data => {
            // Check if there was an error in the response
            if (data.error) {
                // Display the error message
                document.getElementById('result').innerText = data.error;
            } else {
                // Display the current weather data
                document.getElementById('result').innerText = `
                    Temperature: ${data.main.temp}°C\n
                    Feels like: ${data.main.feels_like}°C\n
                    Weather: ${data.weather[0].description}\n
                    Humidity: ${data.main.humidity}%\n
                    Wind Speed: ${data.wind.speed} m/s\n
                    Pressure: ${data.main.pressure} hPa
                `;
            }
        });
});

// Add an event listener to the "Get 5-Day Forecast" button
document.getElementById('forecastBtn').addEventListener('click', function() {
    // Get the location entered by the user
    const location = document.getElementById('location').value;
    
    // Fetch the 5-day forecast data from the backend server
    fetch(`http://localhost:5000/forecast?location=${location}`)
        .then(response => response.json())  // Parse the response as JSON
        .then(data => {
            // Check if there was an error in the response
            if (data.error) {
                // Display the error message
                document.getElementById('result').innerText = data.error;
            } else {
                // Initialize a string to hold the forecast HTML
                let forecastHtml = '5-Day Forecast (3-hour intervals):\n';
                
                // Loop through the forecast data and append to the forecast HTML
                data.list.forEach(item => {
                    // Convert the timestamp to a readable date and time format
                    const date_time = new Date(item.dt * 1000).toLocaleString();
                    // Append the date, time, temperature, and weather description to the forecast HTML
                    forecastHtml += `${date_time}: ${item.main.temp}°C, ${item.weather[0].description}\n`;
                });
                
                // Display the forecast data
                document.getElementById('result').innerText = forecastHtml;
            }
        });
});
