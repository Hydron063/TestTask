SELECT SUBSTR(issue_key ,1,1), ROUND(AVG(minutes_in_status)/60, 2)
FROM history
WHERE status == 'Open'
GROUP BY SUBSTR(issue_key ,1,1);
