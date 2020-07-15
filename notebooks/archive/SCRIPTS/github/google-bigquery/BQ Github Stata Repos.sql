-- Save to: stata_files_github
SELECT
  *
FROM
  `bigquery-public-data.github_repos.files` AS fl
WHERE
    ENDS_WITH(path, '.ado') OR ENDS_WITH(path, '.do')
