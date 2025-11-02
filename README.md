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






# Micro-arousal Prediction

This complements and describes the pipeline that produces micro-arousal predictions (.vec) from EDF/RESU files using a UNet model.

## Overview
Pipeline :
- Data IO and selection: PythAA.py (ArousalAnalysis)
- Padding/uniformization: Testuniform.py (uniformEDF)
- Prediction model: Testpredict.py (predictEDF with Deepsleep.unet0.get_unet)
- Paths/config: utils (u.DEEPSLEEP_PATH, u.TRAINING_PATH, u.FEATURE_PATH, u.NONAA_PATH, u.AA_PATH)

Key steps:
1) Load EDF/RESU.
2) Select 13 channels in this order:
   - ['EEG F4','EEG C4','EEG O2','EOG Droit','EMG menton','Amp Abd','Amp Thx','Flux Nas','Sao2','ECG','Frq.car.','EMG jamb.1','EMG jamb.2'].
3) Anchor signals to a reference (ref555.npy) and pad to 2^23 samples (≈ 8,388,608).
4) Select 5 input channels for the model by index: [8, 1, 7, 9, 0] = [Sao2, EEG C4, Flux Nas, ECG, EEG F4].
5) Run UNet and write predictions to <TRAINING_PATH>\<EDFName>.vec (one float per line).

## Requirements
- Python 3.9+ 
- TensorFlow 2.x + Keras
- NumPy, h5py
- scikit-learn, matplotlib (evaluation/plots)
- mne (EDF handling), plus your local edf/resu helpers

## Model Assets and Paths

Before running any code, make sure the following paths and files exist:

- **`u.DEEPSLEEP_PATH`**: Folder containing:
    - `ref555.npy`
    - `weights_01.h5`
- **`u.TRAINING_PATH`**: Where `.vec` prediction files are written.
- **`u.FEATURE_PATH`**: Where feature arrays (padded) may be saved.
- **`u.NONAA_PATH`**, **`u.AA_PATH`**: Used for evaluation/comparison.

Typical constant declarations in `utils.py` (change to match your own structure):

utils.py
DEEPSLEEP_PATH = r"C:\path\to\deepsleep"
TRAINING_PATH = r"C:\path\to\outputs"
FEATURE_PATH = r"C:\path\to\features"
NONAA_PATH = r"C:\path\to\nonAA"
AA_PATH = r"C:\path\to\AA"

---

## End-to-End Prediction

### Option A — Through AA Pipeline (Arousal mode)

The AA flow loads EDF and RESU files, selects relevant channels, and calls `predictEDF`:
*Note*: If calls to `uniformEDF` or `predictEDF` are commented out in `ArousalAnalysis`, un-comment them or use Option B.

---

### Option B — Direct Script Usage

Example script to run prediction manually:
run_predict.py
import os
import utils as u
from edf import readEDFHeader, readEDF
from Testpredict import predictEDF
from Testuniform import uniformEDF

edf_path = r"C:\data\BR515010.EDF"
header = readEDFHeader(edf_path)
raw = readEDF(edf_path)

Select channels in the exact order required by the pipeline BEFORE get_data()
raw.pick_channels([
'EEG F4', 'EEG C4', 'EEG O2', 'EOG Droit', 'EMG menton',
'Amp Abd', 'Amp Thx', 'Flux Nas', 'Sao2', 'ECG',
'Frq.car.', 'EMG jamb.1', 'EMG jamb.2'
])
new_raw = raw.get_data()
image = uniformEDF(new_raw) # Pads if needed

predictEDF(raw, os.path.basename(edf_path), image) # Writes <TRAINING_PATH><EDFName>.vec

Run with:
python run_predict.py

---

## Output

- **Prediction vector**: `<TRAINING_PATH>\<EDFName>.vec`
- Plain text file: One float per line (3 decimals).
- Length: EDF signal length (before padding) after inverse shift.

---

## Evaluation

Calculate AUC against ground-truth labels:
import numpy as np, os
from sklearn import metrics
import utils as u

y_true = np.loadtxt(r"C:\path\to\labels\BR515010.resu.vec", dtype=int)
y_pred = np.loadtxt(os.path.join(u.TRAINING_PATH, "BR515010.EDF.vec"), dtype=float)
print("AUC:", metrics.roc_auc_score(y_true, y_pred))
fpr, tpr, _ = metrics.roc_curve(y_true, y_pred)
