{{ config(
    materialized='table'    
) }}

WITH transformed_data AS (
    SELECT 
        a.article_content_id,
        ad.article_content,
        ad.article_content_pos_counts,
        a.article_publishedAt,
        CAST(JSON_EXTRACT_SCALAR(ad.article_content_pos_counts, '$.NOUN') AS INT64) AS noun_count,
        CAST(JSON_EXTRACT_SCALAR(ad.article_content_pos_counts, '$.ADJ') AS INT64) AS adj_count,
        CAST(JSON_EXTRACT_SCALAR(ad.article_content_pos_counts, '$.VERB') AS INT64) AS verb_count,
        CAST(JSON_EXTRACT_SCALAR(ad.article_content_pos_counts, '$.PROPN') AS INT64) AS propn_count
    FROM {{ source('newsanalytics', 'DimArticleContent') }} AS ad
    LEFT OUTER JOIN {{ source('newsanalytics', 'DimArticle') }} AS a
        ON ad.article_content_id = a.article_content_id
    WHERE EXTRACT(MONTH FROM CAST(a.article_publishedAt AS TIMESTAMP)) = 10
      AND EXTRACT(YEAR FROM CAST(a.article_publishedAt AS TIMESTAMP)) = EXTRACT(YEAR FROM CURRENT_DATE())
      AND CAST(a.article_publishedAt AS TIMESTAMP) <= CURRENT_TIMESTAMP()
)

SELECT 
    article_content_id,
    article_publishedAt,
    article_content,
    noun_count,
    adj_count,
    verb_count,
    propn_count
FROM transformed_data
ORDER BY article_publishedAt DESC