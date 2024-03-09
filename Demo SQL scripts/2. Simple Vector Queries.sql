-- Simple Vector Queries

-- Lets look at all the vectors:
SELECT * FROM vector.vectoritems LIMIT 20;

-- Get a vector to use in a proximity match:
SELECT embedding from vector.vectoritems where text = 'Tyler';

-- Vector Query using Euclidean Distance
SELECT text FROM vector.vectoritems ORDER BY embedding <-> (SELECT embedding from vector.vectoritems where text = 'Tyler') LIMIT 5;

-- Vector Query using Cosine Distance
SELECT text FROM vector.vectoritems ORDER BY embedding <=> (SELECT embedding from vector.vectoritems where text = 'Tyler') LIMIT 5;

-- Vector Query using Negative Inner Product
SELECT text FROM vector.vectoritems ORDER BY embedding <#> (SELECT embedding from vector.vectoritems where text = 'Tyler') LIMIT 5;