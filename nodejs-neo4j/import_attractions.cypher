LOAD CSV WITH HEADERS FROM 'file:///attractions.csv' AS row FIELDTERMINATOR ';'
CREATE (:Attraction {
  name: row.name,
  latitude: toFloat(row.latitude),
  longitude: toFloat(row.longitude),
  description: row.description
});