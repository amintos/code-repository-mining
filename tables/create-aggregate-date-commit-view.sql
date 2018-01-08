-- create a function that can help eliminating bad timestamps first
CREATE FUNCTION is_timestamp_valid(text) returns boolean language plpgsql immutable AS
$$
BEGIN
RETURN CASE WHEN to_timestamp($1::text, 'YYYY-MM-DD HH24:MI:SS') IS NOT NULL THEN true ELSE false END; EXCEPTION WHEN others THEN RETURN false;
END;
$$;
