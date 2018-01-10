DROP MATERIALIZED VIEW IF EXISTS view_cve_referring_tweets_extracted_cves;
DROP MATERIALIZED VIEW IF EXISTS view_cve_referring_tweets_extracted_domains;

CREATE MATERIALIZED VIEW view_cve_referring_tweets_extracted_cves AS
SELECT
  id AS tweet_id,
  (regexp_matches(text, 'CVE-[0-9]{3,4}-[0-9]{3,7}', 'g'))[1] as cve
FROM cve_referring_tweets
WITH DATA;

CREATE MATERIALIZED VIEW view_cve_referring_tweets_extracted_domains AS
SELECT
  id AS tweet_id,
  (regexp_matches(text, 'http[s]{0,1}:\/\/?\ ?([-a-zA-Z0-9:%._\+~#=]{2,255}\.[a-z]{2,6})', 'g'))[1] AS domain
FROM cve_referring_tweets
WITH DATA;
