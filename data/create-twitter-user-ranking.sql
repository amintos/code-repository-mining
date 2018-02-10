-- create the view that is used for recommending a twitter/github user inside the application
-- the sole reason for its existence here is speed
DROP MATERIALIZED VIEW IF EXISTS view_twitter_user_ranking;
CREATE MATERIALIZED VIEW view_twitter_user_ranking AS
SELECT
    DISTINCT t.username,
    ccc.cweid,
    COUNT(t.id) OVER (PARTITION BY t.username, ccc.cweid) AS t_cwe_count,
    COUNT(t.id) OVER (PARTITION BY ccc.cweid) AS t_count
FROM cve_referring_tweets t
JOIN view_commit_data_search_for_cve vc ON vc.name = t.username
JOIN view_cve_referring_tweets_extracted_cves ec ON t.id = ec.tweet_id
JOIN cve_cwe_classification ccc ON ec.cve = ccc.cveid
WITH DATA;
