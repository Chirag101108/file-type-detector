# File Type Detector with Danger Level

This Python tool monitors directories or checks individual files to detect their file type and assess their security risk level. It uses file signatures to determine the file type and rates the potential danger of the file.

## Features

- Detect file type using magic numbers.
- Evaluate the security risk level on a scale from 1 (Low Risk) to 10 (Very High Risk).
- Verbal description of the file risk.
- Send desktop notifications with file risk information.

## How to Use

### 1. Monitor a Directory
Run the tool and choose to monitor a directory. It will notify you when a new file is added, showing its type and danger level.

```bash
python file_type_checker.py
