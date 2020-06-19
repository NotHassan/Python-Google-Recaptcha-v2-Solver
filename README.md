# Python-Google-Recaptcha-v2-Solver

This is a working ReCaptcha v2 solver created with Python.

Create a Google Cloud Speech-to-Text API service account and API key file
The API key file must be in the same directory as gcaptcha_solver.py and must be named s2t-api.json

Install all requirements before using the solver:
```
pip install -r requirements.txt
```

Below is an example output of the solve_recaptcha_demo.py file.

```
Started solve_recaptcha_demo.py
Google Recaptcha response: 03AHaCkAYGDNPMwtLeCrbL_yTKe13ZIW6g1RtTO4gIIgiwmVuHz5PKHZwfekJKPUOtOJIPM6Y4LIORJ6w1MLXBjiG3PgM8Pp-acrTMD0h1U1sSEGMTeHEd87lXIq5fNDQ9JkJAC2wBXs84PVREojERmbTHhC_b-0JvL-yAVuwwr4n2BLMk0ahpaYC5UfGySX1ymETCLhJ7bSGF85PiwUZWstvhu47e8lWQPfH7D9_ltfWbkONVQ6Ttm7aj6cGckMdsovZMNL8TT6gMVm1ZbdQtCfkJHAodfgzzB6-y6i6irwnxJ57ELDoEZ-eQD4H1sMo6r-KG0oFUYVU9mSPA3j5QtCGSNIQSaOwTfZPXgZdYZW0MiUtvoYMw5PufNnpZP_dyalq3AUNyc6qGS9-wkoSIyBgfuUuBR01Q_w
--- 33.39432144165039 seconds ---
Transcription Attempts: 2
Transcription Successes: 1
Transcription Fails: 1
Recaptcha Solutions: 1
```
