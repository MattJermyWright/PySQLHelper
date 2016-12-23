-- create temporary table - illustrate markup
DROP TABLE IF EXISTS test.mjw_pageTable_q1_s1;
CREATE TABLE test.mjw_pageTable_q1_s1 AS
  SELECT
    visit_day,
    count(DISTINCT visitor_id)
  FROM test.page_hit
  WHERE :variableDATE_RANGE -- User parameters with a 'variable' or 'parameter' to allow substitution of variables
  GROUP BY 1;

-- select statement - results returned after executing this query
SELECT *
FROM test.mjw_pageTable_q1_s1
WHERE visit_day = (SELECT max(visit_day)
                   FROM test.mjw_pageTable_q1_s1)