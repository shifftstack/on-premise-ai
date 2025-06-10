#!/bin/bash
set -e
if [ -z "$1" ]; then
  echo "Usage: $0 <backup_dir>"
  exit 1
fi
BACKUP_DIR=$1
cp $BACKUP_DIR/onpremiseai.db ../onpremiseai.db
cp -r $BACKUP_DIR/uploaded_docs ../backend/app/
echo "Restore completed from $BACKUP_DIR" 