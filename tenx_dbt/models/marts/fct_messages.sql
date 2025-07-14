{{ config(materialized='table', schema='marts') }}

SELECT
    id,
    channel_name,
    message_id,
    message_text,
    has_image
FROM {{ ref('stg_telegram_messages') }}