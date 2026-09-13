#!/bin/bash
# Deploy an advertorial to Vercel and connect a subdomain on guthealthblog.org
#
# Usage: ./deploy.sh <project-folder> <subdomain>
# Example: ./deploy.sh glp1-v4 start5
#
# This script will:
# 1. Deploy the project to Vercel production
# 2. Fetch existing DNS records from Namecheap
# 3. Add a CNAME record for <subdomain>.guthealthblog.org -> cname.vercel-dns.com
# 4. Add the custom domain to the Vercel project

set -e

# --- Config ---
NC_API_USER="btorradre"
NC_API_KEY="[REDACTED_SECRET]"
NC_USERNAME="btorradre"
NC_CLIENT_IP="50.207.41.152"
DOMAIN_SLD="guthealthblog"
DOMAIN_TLD="org"
BASE_DIR="$(cd "$(dirname "$0")" && pwd)"

# --- Args ---
PROJECT_DIR="$1"
SUBDOMAIN="$2"

if [ -z "$PROJECT_DIR" ] || [ -z "$SUBDOMAIN" ]; then
    echo "Usage: ./deploy.sh <project-folder> <subdomain>"
    echo "Example: ./deploy.sh glp1-v4 start5"
    exit 1
fi

FULL_DOMAIN="${SUBDOMAIN}.${DOMAIN_SLD}.${DOMAIN_TLD}"

echo "========================================="
echo "Deploying: $PROJECT_DIR"
echo "Domain:    $FULL_DOMAIN"
echo "========================================="

# --- Step 1: Deploy to Vercel ---
echo ""
echo "[1/4] Deploying to Vercel..."
cd "$BASE_DIR/$PROJECT_DIR"
npx vercel --yes --prod

# --- Step 2: Fetch existing DNS records ---
echo ""
echo "[2/4] Fetching existing DNS records..."
RESPONSE=$(curl -s "https://api.namecheap.com/xml.response?ApiUser=${NC_API_USER}&ApiKey=${NC_API_KEY}&UserName=${NC_USERNAME}&Command=namecheap.domains.dns.getHosts&ClientIp=${NC_CLIENT_IP}&SLD=${DOMAIN_SLD}&TLD=${DOMAIN_TLD}")

# Check for errors
if echo "$RESPONSE" | grep -q 'Status="ERROR"'; then
    echo "ERROR: Failed to fetch DNS records from Namecheap"
    echo "$RESPONSE"
    exit 1
fi

# --- Step 3: Parse existing records and build setHosts URL ---
echo ""
echo "[3/4] Adding CNAME record for $FULL_DOMAIN..."

# Parse existing hosts into arrays
HOSTS=()
INDEX=0
while IFS= read -r line; do
    if echo "$line" | grep -q '<host '; then
        INDEX=$((INDEX + 1))
        NAME=$(echo "$line" | sed -n 's/.*Name="\([^"]*\)".*/\1/p')
        TYPE=$(echo "$line" | sed -n 's/.*Type="\([^"]*\)".*/\1/p')
        ADDRESS=$(echo "$line" | sed -n 's/.*Address="\([^"]*\)".*/\1/p')
        TTL=$(echo "$line" | sed -n 's/.*TTL="\([^"]*\)".*/\1/p')
        MXPREF=$(echo "$line" | sed -n 's/.*MXPref="\([^"]*\)".*/\1/p')

        # Skip if this subdomain already exists (we'll re-add it)
        if [ "$NAME" = "$SUBDOMAIN" ]; then
            echo "  Found existing record for $SUBDOMAIN, will overwrite."
            INDEX=$((INDEX - 1))
            continue
        fi

        HOSTS+=("HostName${INDEX}=${NAME}&RecordType${INDEX}=${TYPE}&Address${INDEX}=${ADDRESS}&TTL${INDEX}=${TTL}&MXPref${INDEX}=${MXPREF}")
        echo "  Preserving: $NAME ($TYPE) -> $ADDRESS"
    fi
done <<< "$RESPONSE"

# Add the new CNAME record
INDEX=$((INDEX + 1))
HOSTS+=("HostName${INDEX}=${SUBDOMAIN}&RecordType${INDEX}=CNAME&Address${INDEX}=cname.vercel-dns.com.&TTL${INDEX}=1799")
echo "  Adding:     $SUBDOMAIN (CNAME) -> cname.vercel-dns.com."

# Build the setHosts query string
HOST_PARAMS=$(IFS='&'; echo "${HOSTS[*]}")
SET_URL="https://api.namecheap.com/xml.response?ApiUser=${NC_API_USER}&ApiKey=${NC_API_KEY}&UserName=${NC_USERNAME}&Command=namecheap.domains.dns.setHosts&ClientIp=${NC_CLIENT_IP}&SLD=${DOMAIN_SLD}&TLD=${DOMAIN_TLD}&${HOST_PARAMS}"

# Execute setHosts
SET_RESPONSE=$(curl -s "$SET_URL")

if echo "$SET_RESPONSE" | grep -q 'IsSuccess="true"'; then
    echo "  DNS record added successfully!"
else
    echo "ERROR: Failed to set DNS records"
    echo "$SET_RESPONSE"
    exit 1
fi

# --- Step 4: Add domain to Vercel project ---
echo ""
echo "[4/4] Adding $FULL_DOMAIN to Vercel project..."
cd "$BASE_DIR/$PROJECT_DIR"
npx vercel domains add "$FULL_DOMAIN"

echo ""
echo "========================================="
echo "DONE!"
echo "Vercel:  https://${PROJECT_DIR}.vercel.app"
echo "Domain:  https://${FULL_DOMAIN}"
echo "========================================="
echo ""
echo "Note: SSL certificate may take a few minutes to provision."
