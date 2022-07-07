#!/bin/bash
# Folosirea script-ului pentru pornirea aplicatiei

uvicorn server:app --port 44777 --reload --log-level info
