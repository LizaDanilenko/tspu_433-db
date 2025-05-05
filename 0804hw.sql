SELECT albums.id AS album_id, albums.title AS album_title, authors.name AS author_name,
COUNT(songs.id) AS track_count,
printf('%02d:%02d', SUM(songs.duration) / 60, SUM(songs.duration) % 60) AS total_duration
FROM albums
LEFT JOIN songs ON albums.id = songs.album_id
LEFT JOIN song_authors ON songs.id = song_authors.song_id
LEFT JOIN authors ON song_authors.author_id = authors.id
GROUP BY albums.id, authors.id
ORDER BY albums.id;
