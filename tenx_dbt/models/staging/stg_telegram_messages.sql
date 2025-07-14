{{ config(materialized='view') }}

SELECT
    channel_name,
    message_id,
    message_date,
    message_text,
    has_image
FROM public.raw_messages
WHERE message_text IS NOT NULL