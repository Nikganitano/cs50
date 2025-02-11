-- The names of songs that are by Post Malone.
SELECT songs.name FROM songs FULL JOIN artists ON songs.artist_id=artists.id WHERE artists.name = "Post Malone";
