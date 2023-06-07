const express = require('express');
const neo4j = require('neo4j-driver');

const app = express();
const port = 3000;

const driver = neo4j.driver(
  'bolt://neo4j:7687',
  neo4j.auth.basic('neo4j', 'password')
);

app.use(express.static('public'));

app.get('/attractions', async (req, res) => {
  try {
    const session = driver.session();
    const result = await session.run('MATCH (a:Attraction) RETURN a.name AS name, a.latitude AS latitude, a.longitude AS longitude, a.description AS description');
    const attractions = result.records.map((record) => record.toObject());
    res.send(attractions);
  } catch (error) {
    console.error('Error retrieving attractions from the database:', error);
    res.status(500).send('An error occurred while retrieving attractions');
  }
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
