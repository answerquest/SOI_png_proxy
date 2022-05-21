#!/bin/bash

uvicorn soi_proxy_launch:app --port 5520 --host 0.0.0.0 --reload
