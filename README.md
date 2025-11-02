# Anonym
CLI tool to anonymize and de-anonymize EDF and RESU files (patient-related data) with logging and lookup tables.

## Features
- Anonymization
    Overwrite sensitive fields in .EDF and .resu at fixed offsets: AnonymiseEDF, AnonymiseResu
    Rename files to RawAnonyme<ID>.EDF and resuAnonyme<ID>.resu: ChangeNameToAnonyme
    Save metadata to TSV tables: saveDataEDF, saveDataresu
- De-anonymization
    Restore original file names and contents from tables: UN, UnAnonymiseEDF, UnAnonymiseResu, ChangeAnonymeToName
- Incremental ID management: WriteFirstLine, CheckID
- Logging via utils.printLogs / utils.initLogs

## Requirements
- Python 3.8+
- NumPy

### Options

- `-d, --dir` : folder containing `.EDF` and `.resu` files
- `-a, --anonym` : anonymize
- `-u, --unanonym` : de-anonymize
- `-e, --EDFDB` : EDF TSV path (default: `EDFDatadefault.txt`)
- `-r, --resuDB` : RESU TSV path (default: `resuDataDefault.txt`)

### How It Works

**Anonymization:**
- For each `.resu`, extract fields and append to `resuDataDefault.txt` (`saveDataresu`)
- Overwrite sensitive fields and rename (`AnonymiseResu`, `ChangeNameToAnonyme`)
- Find the matching `.EDF` from `RawFileName`, save EDF metadata (`saveDataEDF`)
- Overwrite EDF fields and rename (`AnonymiseEDF`)

**De-anonymization:**
- For each `resuAnonyme<ID>.resu`, find the row by ID (`CheckInDataFile`)
- Restore original names (`ChangeAnonymeToName`)
- Restore contents at fixed offsets (`UnAnonymiseResu`, `UnAnonymiseEDF`)

### TSV Table Formats

**EDFDatadefault.txt**
- Header: `EDF/EDFHeader/identification fields/Date/ID`
- Columns: `[EDFName, Header[0:80], Header[80:160], Header[160:168], ID]`

**resuDataDefault.txt**
- Header: `resuName/Date/Room/EDFName/FileNumber/Name/FirstName/BirthDate/Sex/ID`
- Columns: `[resuName, ExamDate, Room, RawFileName, FileNumber, Name, FirstName, BirthDate, Sex, ID]`
- Tab-separated; values are read and written using fixed byte offsets from the source files.
