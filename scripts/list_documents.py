import sqlite3

DB_PATH = "../onpremiseai.db"

def main():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT id, filename, uploader, upload_time FROM documents")
    docs = c.fetchall()
    print("ID\tFilename\tUploader\tUpload Time")
    for doc in docs:
        print(f"{doc[0]}\t{doc[1]}\t{doc[2]}\t{doc[3]}")
    conn.close()

if __name__ == "__main__":
    main() 