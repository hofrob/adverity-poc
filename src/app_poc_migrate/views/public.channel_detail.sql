CREATE OR REPLACE VIEW public.channel_detail AS
WITH tvshows AS (
    SELECT channel.id AS channel_id, jsonb_agg(tvshow.name) AS tvshow_names
    FROM tvshow
    JOIN episode ON tvshow.id = episode.tvshow_id
    JOIN channel_episode ON episode.id = channel_episode.episode_id
    JOIN channel ON channel_episode.channel_id = channel.id
    GROUP BY channel.id
)

SELECT
    channel.id,
    channel.uuid,
    channel.created_at,
    channel.updated_at,
    channel.name,
    coalesce(tvshows.tvshow_names, '[]'::jsonb) AS tvshow_names
FROM channel
LEFT JOIN tvshows ON channel.id = tvshows.channel_id
