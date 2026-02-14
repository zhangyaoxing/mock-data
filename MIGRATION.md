# Migration Guide: v0.1.x to v0.2.0

This guide helps you migrate from the old project structure to the new v0.2.0 structure.

## What Changed?

### Directory Structure

**Old Structure:**
```
mock-data/
├── mock.py              # Main script
├── libs/
│   ├── mock_data.py
│   ├── utils.py
│   └── providers/
├── schemas/
├── output/              # Output directory
└── config.json          # Root config
```

**New Structure:**
```
mock-data/
├── src/
│   └── mockdata/        # Main package
│       ├── core/
│       ├── providers/
│       └── utils/
├── schemas/
├── data/                # Output directory (renamed)
├── config/
│   └── config.json      # Moved to config/
└── pyproject.toml       # Modern Python packaging
```

## Migration Steps

### 1. Backup Your Data

```bash
# Backup your schemas and output
cp -r schemas schemas_backup
cp -r output output_backup
cp config.json config_backup.json
```

### 2. Update Configuration

**Old location:** `config.json` (project root)  
**New location:** `config/config.json` or `config.json` (both supported)

Update output folder path in config:
```json
{
  "output": {
    "ejson": {
      "folder": "data"  // Changed from "output/"
    }
  }
}
```

### 3. Update Import Statements (If You Imported the Library)

**Old imports:**
```python
from libs.mock_data import MockData
from libs.providers.ejson_provider import EJsonProvider
from libs.utils import load_config
```

**New imports:**
```python
from mockdata import MockData
from mockdata.providers import EJsonProvider
from mockdata.utils import load_config
```

### 4. Update Run Commands

**Old command:**
```bash
./run
# or
python mock.py
```

**New command:**
```bash
mockdata
# or
python -m mockdata
# or (still works)
./run
```

### 5. Move Your Data

```bash
# Move output files to new location
mkdir -p data
mv output/*.ejson data/ 2>/dev/null || true

# Move config if needed
mkdir -p config
cp config.json config/config.json
```

## Compatibility Notes

### Backward Compatibility

- The `./run` script now works with both old and new structures
- Schema files remain unchanged
- Config format is the same, only location changed
- Output format (EJSON) is identical

### Breaking Changes

None! The tool is designed to be backward compatible. Your existing schemas and configurations will work without modification.

## New Features in v0.2.0

### 1. Package Installation

You can now install mockdata as a proper Python package:

```bash
pip install -e .
```

This adds the `mockdata` command to your PATH.

### 2. Better CLI

```bash
# More informative output
mockdata

# Environment variables
LOG_LEVEL=DEBUG mockdata
```

### 3. Testing Support

Run the test suite:
```bash
pytest
pytest --cov=mockdata
```

### 4. Development Tools

```bash
# Code formatting
black src tests

# Linting
flake8 src tests

# Type checking
mypy src
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'mockdata'"

**Solution:** Install the package:
```bash
pip install -e .
```

### "Config file not found"

**Solution:** Ensure config exists in one of these locations:
- `config/config.json` (recommended)
- `config.json` (legacy, still supported)

### "Output directory not found"

**Solution:** Create the data directory:
```bash
mkdir -p data
```

Or update your config to use a different folder.

### Old imports not working

**Solution:** Either:
1. Update imports to use new package structure, or
2. Keep using the old `mock.py` script directly

## Gradual Migration

You can migrate gradually:

1. **Phase 1:** Keep using old structure with `python mock.py`
2. **Phase 2:** Install new package but keep old files
3. **Phase 3:** Switch to `mockdata` command
4. **Phase 4:** Remove old `libs/` directory after testing

The `./run` script will automatically detect and use the appropriate structure.

## Need Help?

- Check the [README.md](README.md) for detailed documentation
- Review [examples](schemas/) for schema definitions
- Open an issue on GitHub

## Rollback

If you need to rollback to v0.1.x:

```bash
# Restore backups
cp config_backup.json config.json
cp -r output_backup/* output/

# Use git to revert
git checkout v0.1.x  # or your previous version tag
```
