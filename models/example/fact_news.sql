{{ config(
    materialized='table'    
) }}

SELECT
    fn.article_id,
    fn.source_id,
    fn.source_name,
    fn.author_name
FROM {{ source('newsanalytics', 'FactNews') }} AS fn

-- Dummy join to establish dependency for lineage graph
LEFT JOIN (
    SELECT article_id FROM {{ source('newsanalytics', 'DimArticle') }} LIMIT 0
) AS da ON fn.article_id = da.article_id
