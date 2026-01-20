-- Phase 2: Create clean, queryable jobs table


create table if not exists clean_jobs (
    job_id text primary key ,
    company_name text,
    title text,
    location text,
    remote boolean,
    url text ,
    created_at timestamp
);


insert into clean_jobs
 (
    job_id,
    company_name,
    title,
    location,
    remote,url,
    created_at
    )
SELECT DISTINCT ON (job->>'slug')
    job->>'slug'                    AS job_id,
    trim(job->>'company_name')      AS company_name,
    job->>'title'                   AS title,
    job->>'location'                AS location,
    (job->>'remote')::BOOLEAN       AS remote,
    job->>'url'                     AS url,
    TO_TIMESTAMP((job->>'created_at')::BIGINT)
FROM raw_jobs,
     LATERAL jsonb_array_elements(raw_payload->'data') AS job;

