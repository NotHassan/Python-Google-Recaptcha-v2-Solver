#!/usr/bin/env python3
from gcaptcha_solver import Gcaptcha
import time

print('Started solve_recaptcha.py')
start_time = time.time()
gcaptcha = Gcaptcha('https://www.google.com/recaptcha/api2/demo')
print('Google Recaptcha response: {}'.format(gcaptcha.response))

print("--- %s seconds ---" % (time.time() - start_time))
print('Transcription Attempts: {}'.format(gcaptcha.transcription.attempts))
print('Transcription Successes: {}'.format(gcaptcha.transcription.successful))
print('Transcription Fails: {}'.format(gcaptcha.transcription.failed))
print('Recaptcha Solutions: {}'.format(gcaptcha.recaptcha.solved))