SELECT issue_key, status, MAX(datetime(started_at / 1000, 'unixepoch')) as started_at
FROM history
GROUP BY issue_key
HAVING started_at <= strftime('%s', 'now') * 1000 and status != 'Closed' and status != 'Resolved';