#!/bin/bash
set -e
BACKUP_DIR=../backup_$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR
cp ../onpremiseai.db $BACKUP_DIR/
cp -r ../backend/app/uploaded_docs $BACKUP_DIR/
echo "Backup completed at $BACKUP_DIR" 