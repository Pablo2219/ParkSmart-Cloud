#!/bin/sh
set -eu

API_URL="${API_BASE_URL:-http://localhost:8000}"
API_URL="${API_URL%/}"

cat > /usr/share/nginx/html/config.js <<CONFIG
window.PARKSMART_CONFIG = {apiBaseUrl: "${API_URL}"};
CONFIG
