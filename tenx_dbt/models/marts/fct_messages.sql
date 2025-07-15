{{ config(materialized='table', schema='marts') }}

SELECT
    f.id,
    f.channel_name,
    f.message_id,
    f.message_text,
    f.has_image,
    i.object_detected,
    i.confidence
FROM {{ ref('fct_messages') }} f
LEFT JOIN public.image_objects i ON f.message_id = i.message_id AND f.channel_name = i.channel_name