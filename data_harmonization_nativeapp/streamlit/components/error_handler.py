import streamlit as st
import traceback
import random
from services.i18n import Translator

def errorHandling (func):
    def internalErrorHandler(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as error:
            showErrorMessage(error, traceback.format_exc(), func.__name__)
            return None
    return internalErrorHandler

def showErrorMessage (error, stackTrace, processName = None):
    t = Translator().translate
    processName = f"\n{t('Process')}: {processName}." if processName is not None else ""
    showStackTrace = f"\n\nStackTrace: {stackTrace}" if stackTrace is not None else ""
    st.error(f"{t('GeneralError')}\n{processName}\n\nIssue: {error}.\n\n{showStackTrace}")