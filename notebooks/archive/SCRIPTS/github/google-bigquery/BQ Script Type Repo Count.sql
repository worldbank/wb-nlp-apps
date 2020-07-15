SELECT
  script_type, COUNT(repo_name) AS repo_count
FROM(
  SELECT DISTINCT repo_name, script_type
  FROM `wb-analytics-259603.github_analytics_repositories.module_usage_per_repository`
)
GROUP BY
  script_type
ORDER BY
  COUNT(repo_name) DESC