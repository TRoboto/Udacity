## Part 2: Clinical Application Overview

Now that you have built your pulse rate algorithm and tested your algorithm to know it works, we can use it to compute more clinically meaningful features and discover healthcare trends.

Specifically, you will use 24 hours of heart rate data from 1500 samples to try to validate the well known trend that average resting heart rate increases up until middle age and then decreases into old age. We'll also see if resting heart rates are higher for women than men. See the trend illustrated in this image:

![heart-rate-age-ref-chart](heart-rate-age-reference-chart.jpg)

Follow the steps in the `clinical_app_starter.ipynb` to reproduce this result!

### Dataset (CAST)

The data from this project comes from the [Cardiac Arrythmia Suppression Trial (CAST)](https://physionet.org/content/crisdb/1.0.0/), which was sponsored by the National Heart, Lung, and Blood Institute (NHLBI). CAST collected 24 hours of heart rate data from ECGs from people who have had a myocardial infarction (MI) within the past two years.<sup>1</sup> This data has been smoothed and resampled to more closely resemble PPG-derived pulse rate data from a wrist wearable.<sup>2</sup>

1. **CAST RR Interval Sub-Study Database Citation** - Stein PK, Domitrovich PP, Kleiger RE, Schechtman KB, Rottman JN. Clinical and demographic determinants of heart rate variability in patients post myocardial infarction: insights from the Cardiac Arrhythmia Suppression Trial (CAST). Clin Cardiol 23(3):187-94; 2000 (Mar)
2. **Physionet Citation** - Goldberger AL, Amaral LAN, Glass L, Hausdorff JM, Ivanov PCh, Mark RG, Mietus JE, Moody GB, Peng C-K, Stanley HE. PhysioBank, PhysioToolkit, and PhysioNet: Components of a New Research Resource for Complex Physiologic Signals (2003). Circulation. 101(23):e215-e220.

### Folder Contents

#### Starter
These are the files that are given:
- `README.md`
- `datasets`
- `clinical_app_starter.ipynb`
- `heart-rate-age-reference-chart.jpg`

#### Completed
Once you have completed this portion these should be the files in this repo.
- `README.md`
- `datasets` - this folder should be removed when submitting for reviewers.
- `clinical_app.ipynb`<sup>*</sup> - completed code portions and clinical conclusion.
- `heart-rate-age-reference-chart.jpg`

<sup>*</sup> This file can be named slightly different but must fufill the description given and be clear to the reviewer what that file includes.
