$(document).ready(function () {
    // weather api

    const key = 'LotdkzXJjnLh5l3hbwUfEQittwSEmy0f';

    // get weather information
    const getWeather = async (id) => {

        const base = 'https://dataservice.accuweather.com/forecasts/v1/daily/5day/';
        const query = `${id}?apikey=${key}&details=true&metric=true`;

        const response = await fetch(base + query);
        const data = await response.json();

        return data;

    };

    // get location information
    const getLocation = async (lat, lon) => {

        const base = 'https://dataservice.accuweather.com/locations/v1/cities/geoposition/search';
        const query = `?apikey=${key}&q=${lat},${lon}`;

        const response = await fetch(base + query);
        const data = await response.json();

        return data;
    };

    const getWeatherData = async (lat, lon) => {
        const location = await getLocation(lat, lon);
        const weather = await getWeather(location.Key);

        return {
            location,
            weather
        };
    };

    const updateUI = (data) => {

        const weather = data.weather;

        days = [];

        const populateDays = (days) => {
            weather.DailyForecasts.forEach(day => {
                days.push(day);
            });
        };

        console.log(days);

        details = document.querySelectorAll('.details');

        populateDays(days);

        details.forEach(detail => {
            day = days[0];
            detail.innerHTML = `
            <div>
                <p>${new Date(day.Date).toLocaleDateString('en-us', { weekday:"long", month:"short", day:"numeric"})}</p>
            </div>
            <div>
                <p>${day.Day.ShortPhrase}</p>
            </div>
            <div>
                <p>max-temp ${day.Temperature.Maximum.Value}&deg;C<p>
            </div>
        `;
            days = days.slice(1);
        });

        icons = document.querySelectorAll('.icon img');

        populateDays(days);

        icons.forEach(icon => {
            day = days[0];
            icon.setAttribute('src', `../../../media/icons/${day.Day.Icon}.svg`);
            days = days.slice(1);
        });
    };

    getWeatherData(lat, lon)
        .then(data => updateUI(data))
        .catch(err => console.log(err));
});