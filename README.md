# Python-Google-Recaptcha-v2-Solver

This is a working ReCaptcha v2 solver created with Python. Below is an example execution of the solve_recaptcha_demo.py file.
You will need to download chromedriver from Google for the program to work. You'll also need Google Speech to Text API access.


```
Started solve_recaptcha.py
Google Recaptcha response: 03AHaCkAYGDNPMwtLeCrbL_yTKe13ZIW6g1RtTO4gIIgiwmVuHz5PKHZwfekJKPUOtOJIPM6Y4LIORJ6w1MLXBjiG3PgM8Pp-acrTMD0h1U1sSEGMTeHEd87lXIq5fNDQ9JkJAC2wBXs84PVREojERmbTHhC_b-0JvL-yAVuwwr4n2BLMk0ahpaYC5UfGySX1ymETCLhJ7bSGF85PiwUZWstvhu47e8lWQPfH7D9_ltfWbkONVQ6Ttm7aj6cGckMdsovZMNL8TT6gMVm1ZbdQtCfkJHAodfgzzB6-y6i6irwnxJ57ELDoEZ-eQD4H1sMo6r-KG0oFUYVU9mSPA3j5QtCGSNIQSaOwTfZPXgZdYZW0MiUtvoYMw5PufNnpZP_dyalq3AUNyc6qGS9-wkoSIyBgfuUuBR01Q_w
--- 33.39432144165039 seconds ---
Transcription Attempts: 2
Transcription Successes: 1
Transcription Fails: 1
Recaptcha Solutions: 1
```

Note that there are some additional modifications not included in this version that bypasses Google's webdriver check. If you intend to use this, expect ReCaptcha to ask to solve multiple captchas and possibly timeout.
