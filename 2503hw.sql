CREATE TABLE IF NOT EXISTS albums (
  id INTEGER primary key autoincrement,
  title VARCHAR(255),
  description TEXT,
  `year` YEAR
);

CREATE TABLE IF NOT EXISTS songs (
  id INTEGER primary key autoincrement,
  title VARCHAR(255),
  duration INT(3),
  album_id INTEGER,
  FOREIGN KEY (album_id) REFERENCES albums(id)
);

CREATE TABLE IF NOT EXISTS authors (
  id INTEGER primary key autoincrement,
  name VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS song_authors (
  song_id INTEGER,
  author_id INTEGER,
  PRIMARY KEY (song_id, author_id),
  FOREIGN KEY (song_id) REFERENCES songs(id),
  FOREIGN KEY (author_id) REFERENCES authors(id)
);

INSERT INTO authors (name) VALUES
('John Lennon'),
('Paul McCartney');

INSERT INTO albums (title, description, `year`) VALUES
('Imagine', 'John Lennon solo album', 1971),
('Band on the Run', 'Paul McCartney and Wings album', 1973);

INSERT INTO songs (title, duration, album_id)
VALUES
('Imagine', 181, (SELECT id FROM albums WHERE title = 'Imagine')),
('Jealous Guy', 254, (SELECT id FROM albums WHERE title = 'Imagine')),
('Gimme Some Truth', 196, (SELECT id FROM albums WHERE title = 'Imagine')),
('Band on the Run', 313, (SELECT id FROM albums WHERE title = 'Band on the Run')),
('Jet', 248, (SELECT id FROM albums WHERE title = 'Band on the Run')),
('Let Me Roll It', 298, (SELECT id FROM albums WHERE title = 'Band on the Run')),
('Mrs Vandebilt', 274, (SELECT id FROM albums WHERE title = 'Band on the Run')),
('Bluebird', 202, (SELECT id FROM albums WHERE title = 'Band on the Run')),
('Helen Wheels', 224, (SELECT id FROM albums WHERE title = 'Band on the Run')),
('Nineteen Hundred and Eighty Five', 335, (SELECT id FROM albums WHERE title = 'Band on the Run'));


INSERT INTO song_authors (song_id, author_id)
VALUES
((SELECT id FROM songs WHERE title = 'Imagine'), (SELECT id FROM authors WHERE name = 'John Lennon')),
((SELECT id FROM songs WHERE title = 'Jealous Guy'), (SELECT id FROM authors WHERE name = 'John Lennon')),
((SELECT id FROM songs WHERE title = 'Gimme Some Truth'), (SELECT id FROM authors WHERE name = 'John Lennon')),
((SELECT id FROM songs WHERE title = 'Band on the Run'), (SELECT id FROM authors WHERE name = 'Paul McCartney')),
((SELECT id FROM songs WHERE title = 'Jet'), (SELECT id FROM authors WHERE name = 'Paul McCartney')),
((SELECT id FROM songs WHERE title = 'Let Me Roll It'), (SELECT id FROM authors WHERE name = 'Paul McCartney')),
((SELECT id FROM songs WHERE title = 'Mrs Vandebilt'), (SELECT id FROM authors WHERE name = 'Paul McCartney')),
((SELECT id FROM songs WHERE title = 'Bluebird'), (SELECT id FROM authors WHERE name = 'Paul McCartney')),
((SELECT id FROM songs WHERE title = 'Helen Wheels'), (SELECT id FROM authors WHERE name = 'Paul McCartney')),
((SELECT id FROM songs WHERE title = 'Nineteen Hundred and Eighty Five'), (SELECT id FROM authors WHERE name = 'Paul McCartney'));
