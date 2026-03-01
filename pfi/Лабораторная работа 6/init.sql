CREATE DATABASE IF NOT EXISTS lab6_webapp
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE lab6_webapp;

CREATE TABLE IF NOT EXISTS sportsmen (
    id INT UNSIGNED AUTO_INCREMENT PRIMARY KEY,
    surname VARCHAR(100) NOT NULL,
    sport VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO sportsmen (surname, sport)
SELECT 'Иванов', 'Футбол'
WHERE NOT EXISTS (
    SELECT 1 FROM sportsmen WHERE surname = 'Иванов' AND sport = 'Футбол'
);

INSERT INTO sportsmen (surname, sport)
SELECT 'Петров', 'Баскетбол'
WHERE NOT EXISTS (
    SELECT 1 FROM sportsmen WHERE surname = 'Петров' AND sport = 'Баскетбол'
);

INSERT INTO sportsmen (surname, sport)
SELECT 'Сидоров', 'Теннис'
WHERE NOT EXISTS (
    SELECT 1 FROM sportsmen WHERE surname = 'Сидоров' AND sport = 'Теннис'
);

INSERT INTO sportsmen (surname, sport)
SELECT 'Кузнецов', 'Плавание'
WHERE NOT EXISTS (
    SELECT 1 FROM sportsmen WHERE surname = 'Кузнецов' AND sport = 'Плавание'
);
