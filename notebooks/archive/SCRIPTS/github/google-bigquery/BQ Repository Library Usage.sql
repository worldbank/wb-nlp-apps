-- Save to: module_usage_per_repository
SELECT
  IF(script_type='R' OR (script_type <> 'R' AND NOT REGEXP_CONTAINS(module, r'\.')), module, SUBSTR(module, 1, STRPOS(module, '.') - 1)) AS module,
  repo_name, script_type,
  COUNT(*) AS occurence
FROM `wb-analytics-259603.github_analytics_repositories.ipython_notebooks_python_and_R_scripts_imports_full`, UNNEST(modules) AS module
GROUP BY
  module, repo_name, script_type
ORDER BY
  repo_name