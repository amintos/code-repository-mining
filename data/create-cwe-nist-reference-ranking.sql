DROP MATERIALIZED VIEW IF EXISTS view_nist_reference_cwe_ranking;

CREATE MATERIALIZED VIEW view_nist_reference_cwe_ranking AS
SELECT *, nrefs/nrefstotal::float AS refshare
FROM (
    SELECT DISTINCT cr.domain,
	   cvecwe.cweid,
	   COUNT(cr.domain) OVER (PARTITION BY cvecwe.cweid) AS nrefstotal,
	   COUNT(cr.domain) OVER (PARTITION BY cr.domain, cvecwe.cweid) AS nrefs
    FROM view_cvereference_extracted_domains cr 
    JOIN cve_cwe_classification cvecwe ON cr.cveid = cvecwe.cveid 
) a
WHERE  nrefs/nrefstotal::float > 0.1
WITH DATA;
