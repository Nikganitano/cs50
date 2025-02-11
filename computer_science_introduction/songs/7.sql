-- The average energy of songs that are by Drake
SELECT AVG(songs.energy) FROM songs FULL JOIN artists ON songs.artist_id=artists.id WHERE artists.name = "Drake";
