-- Save to: ipython_notebooks_python_and_R_scripts_imports_full
SELECT file_id, repo_name, path, line,
  IF(
    ENDS_WITH(path, '.py'),
    'Python',
    IF(
      (
        ENDS_WITH(path, '.r') OR
        ENDS_WITH(path, '.R') OR
        ENDS_WITH(path, '.Rmd') OR
        ENDS_WITH(path, '.rmd')
      ),
      'R',
      IF(
        ENDS_WITH(path, '.ipynb'),
        'IPython',
        'Others'
      )
    )
  ) AS script_type,
  IF(
    ENDS_WITH(path, '.py'),
    IF(
      REGEXP_CONTAINS(line, r'^\s*import\s+'),
      REGEXP_EXTRACT_ALL(line, r'(?:^\s*import\s|,)\s*([a-zA-Z0-9\_\.]+)'),
      REGEXP_EXTRACT_ALL(line, r'^\s*from\s+([a-zA-Z0-9\_\.]+)')
    ),
    IF(
      (
        ENDS_WITH(path, '.r') OR
        ENDS_WITH(path, '.R') OR
        ENDS_WITH(path, '.Rmd') OR
        ENDS_WITH(path, '.rmd')
      ),
      REGEXP_EXTRACT_ALL(line, r'library\s*\((?:package=|)[\"\']*([a-zA-Z0-9\_\.]+)[\"\']*.*?\)'), -- we're still ignoring commented out imports
      IF(
        ENDS_WITH(path, '.ipynb'),
        IF(
          REGEXP_CONTAINS(line, r'"\s*import\s+'),
          REGEXP_EXTRACT_ALL(line, r'(?:"\s*import\s|,)\s*([a-zA-Z0-9\_\.]+)'),
          REGEXP_EXTRACT_ALL(line, r'"\s*from\s+([a-zA-Z0-9\_\.]+)')
        ),
        ['']
      )
    )
  ) AS modules
FROM (
  SELECT
        ct.id AS file_id, repo_name, path,
        # Add a space after each line.
        # It is required to ensure correct line numbering.
        SPLIT(REPLACE(content, "\n", " \n"), "\n") AS lines
  FROM `bigquery-public-data.github_repos.files` AS fl
  JOIN `bigquery-public-data.github_repos.contents` AS ct ON fl.id=ct.id
  WHERE
    ENDS_WITH(path, '.py') OR
    (
      ENDS_WITH(path, '.r') OR
      ENDS_WITH(path, '.R') OR
      ENDS_WITH(path, '.Rmd') OR
      ENDS_WITH(path, '.rmd')
    ) OR
    ENDS_WITH(path, '.ipynb')  -- may include julia e.g., EthanAnderes/STA250CMB.jl/lectures/julia_lecture2_types/julia_type_design.ipynb
), UNNEST(lines) as line
WHERE
  (ENDS_WITH(path, '.py') AND (REGEXP_CONTAINS(line, r'^\s*import\s+') OR REGEXP_CONTAINS(line, r'^\s*from .* import '))) OR
  (
    (
      ENDS_WITH(path, '.r') OR
      ENDS_WITH(path, '.R') OR
      ENDS_WITH(path, '.Rmd') OR
      ENDS_WITH(path, '.rmd')
    ) AND REGEXP_CONTAINS(line, r'library\s*\(')) OR
  (
    ENDS_WITH(path, '.ipynb') AND
    (
      REGEXP_CONTAINS(line, r'"\s*import\s+') OR
      REGEXP_CONTAINS(line, r'"\s*from .* import ')
    )
  )