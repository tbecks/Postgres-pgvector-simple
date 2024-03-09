-- Enable Extensions
CREATE EXTENSION vector;

CREATE SCHEMA vector;

-- DROP TABLE vector.vectoritems;
CREATE TABLE vector.vectoritems(
    text varchar(200) PRIMARY KEY,
    embedding vector(1536)
    );

-- Sample scripts to test
SELECT * FROM vector.vectoritems;


SELECT text from vector.vectoritems ORDER BY embedding <-> 
    (SELECT embedding FROM vector.vectoritems WHERE text = 'Becker')
 LIMIT 5;