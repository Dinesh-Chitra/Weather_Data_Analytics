CREATE TABLE weather_data (
    id SERIAL PRIMARY KEY,
    city VARCHAR(255),
    temperature FLOAT,
    description VARCHAR(255),
    humidity INT,
    wind_speed FLOAT,
    clouds INT,
    visibility INT,
    precipitation FLOAT,
    pressure INT
);

select * from weather_data

TRUNCATE TABLE weather_data RESTART IDENTITY;

select case when humidity > 40 then 'highly humid'
when humidity between 20 and 40  then 'Little humid'
when humidity <20 then'not so humid'
end as Humidity_level, count(*) as Total_count
from weather_data
group by Humidity_level





