# mkdocs-sql

A MkDocs plugin for executing and displaying SQL queries directly in your documentation. Create beautiful, interactive documentation with live SQL queries and formatted results.

## Features

- **Live SQL Query Execution**
  - Execute SQL queries directly in your markdown files
  - Support for SQLite and DuckDB databases
  - Automatic error handling and display

- **Beautiful Table Formatting**
  - Smart column type detection
  - Proper alignment (right for numbers, left for text)
  - Formatted numbers with commas (1,234,567)
  - Clean, modern table styling
  - Alternating row colors and hover effects

- **Interactive Controls**
  - Toggle between formatted and raw markdown tables
  - Show/hide SQL queries
  - State persistence for query visibility
  - Material Design icons

- **Flexible Configuration**
  - Global database settings in mkdocs.yml
  - Per-page database override in frontmatter
  - Support for relative and absolute paths
  - Home directory expansion (~)

## Installation

```bash
pip install mkdocs-sql
```

## Quick Start

1. Add to your mkdocs.yml:
```yaml
plugins:
  - sql:
      database:
        type: sqlite  # or duckdb
        path: ./path/to/database.file
```

2. Add Material Icons to mkdocs.yml:
```yaml
extra_css:
  - https://fonts.googleapis.com/icon?family=Material+Icons
```

3. In your markdown files:
```markdown
```sql
SELECT name, population, gdp_usd
FROM countries
ORDER BY population DESC
LIMIT 5;
```
```

## Configuration

### Global Configuration (mkdocs.yml)

```yaml
plugins:
  - sql:
      database:
        type: sqlite  # or duckdb
        path: ./path/to/database.file
      show_query: true  # default: false
```

### Per-page Configuration (Markdown Frontmatter)

```yaml
---
database: ./different/database.sqlite
show_query: true
---
```

### Configuration Options

| Option | Description | Default |
|--------|-------------|---------|
| database.type | Database type (sqlite/duckdb) | sqlite |
| database.path | Path to database file | None |
| show_query | Show SQL queries by default | false |

## Examples

Check out our [example documentation](https://github.com/ivishalgandhi/mkdocs-sql/tree/main/docs/examples) for:
- Population data analysis
- Database schema documentation
- Complex query examples
- Table formatting examples

## Features in Detail

### Smart Column Formatting
- Population numbers: Formatted with commas (1,234,567)
- Percentages: 2 decimal places
- Currency: Proper decimal alignment
- Automatic detection of numeric columns

### Interactive Controls
- **Table Toggle**: Switch between formatted and raw markdown
- **Query Toggle**: Show/hide SQL queries
- Persistent query visibility state
- Clean, minimal interface

### Table Styling
- Proper column alignment
- Alternating row colors
- Hover effects
- Responsive design
- Clean borders and spacing

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

MIT License - see LICENSE file for details.

## Support

If you encounter any issues or have questions, please [open an issue](https://github.com/ivishalgandhi/mkdocs-sql/issues).
