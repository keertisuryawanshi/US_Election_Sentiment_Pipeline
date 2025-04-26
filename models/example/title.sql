{{ config(
    materialized='table'     
) }}

WITH transformed_data AS (
    SELECT 
        a.article_title_id,
        ad.article_title,
        ad.article_title_pos_counts,
        a.article_publishedAt,
        CAST(JSON_EXTRACT_SCALAR(ad.article_title_pos_counts, '$.NOUN') AS INT64) AS noun_count,
        CAST(JSON_EXTRACT_SCALAR(ad.article_title_pos_counts, '$.ADJ') AS INT64) AS adj_count,
        CAST(JSON_EXTRACT_SCALAR(ad.article_title_pos_counts, '$.VERB') AS INT64) AS verb_count,
        CAST(JSON_EXTRACT_SCALAR(ad.article_title_pos_counts, '$.PROPN') AS INT64) AS propn_count
    FROM {{ source('newsanalytics', 'DimArticleTitle') }} AS ad
    LEFT OUTER JOIN {{ source('newsanalytics', 'DimArticle') }} AS a
        ON ad.article_title_id = a.article_title_id
    WHERE EXTRACT(MONTH FROM CAST(a.article_publishedAt AS TIMESTAMP)) = 10
      AND EXTRACT(YEAR FROM CAST(a.article_publishedAt AS TIMESTAMP)) = EXTRACT(YEAR FROM CURRENT_DATE())
      AND CAST(a.article_publishedAt AS TIMESTAMP) <= CURRENT_TIMESTAMP()
)

SELECT 
    article_title_id,
    article_publishedAt,
    article_title,
    noun_count,
    adj_count,
    verb_count,
    propn_count
FROM transformed_data
ORDER BY article_publishedAt DESC