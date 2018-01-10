DROP MATERIALIZED VIEW IF EXISTS view_cvereference_extracted_domains;
CREATE MATERIALIZED VIEW view_cvereference_extracted_domains AS
SELECT
  cveid, 
  (regexp_matches(reference, 'http[s]{0,1}:\/\/?\ ?([-a-zA-Z0-9:%._\+~#=]{2,255}\.[a-z]{2,6})', 'g'))[1] AS domain
FROM cvereference
WITH DATA;
