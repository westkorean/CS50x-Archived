-- Keep a log of any SQL queries you execute as you solve the mystery.
SELECT * FROM crime_scene_reports
WHERE date = '2024-07-28' AND street = 'Humphrey Street';

SELECT * FROM interviews WHERE name IN ('Witness1', 'Witness2', ...);

SELECT * FROM flights WHERE origin_airport_id = (SELECT id FROM airports WHERE city = 'Fiftyville')
AND day = '2024-07-28';
