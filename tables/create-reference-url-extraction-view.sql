CREATE MATERIALIZED VIEW view_cvereference_extracted_domains AS
SELECT
  cveid, 
  regexp_matches(reference, 'http[s]:\/\/?\ ?([-a-zA-Z0-9:%._\+~#=]{2,255}\.[a-z]{2,6})', 'g') AS domain
FROM cvereference
WITH DATA;
