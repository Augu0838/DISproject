SELECT
  u.username,
  s.stationname,
  temp.temperature

  
  
FROM
  users u
  LEFT JOIN stations s ON s.stationID = u.favoritestation
  JOIN (
    SELECT m.temperature, m.stationID, m.measurementdate
    FROM measurements m
	--WHERE date_part('year', m.measurementdate) = date_trunc('year', CURRENT_DATE) - interval '1 year'
    WHERE (EXTRACT(month FROM m.measurementdate), EXTRACT(day FROM m.measurementdate)) = (EXTRACT(month FROM CURRENT_DATE), EXTRACT(day FROM CURRENT_DATE))

  ) AS temp ON u.favoritestation = temp.stationID 
