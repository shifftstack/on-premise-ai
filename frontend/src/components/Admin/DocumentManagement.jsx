import React, { useState, useEffect } from 'react';
import { uploadDocument, listDocuments } from '../../utils/api';
import { getToken } from '../../utils/auth';

function DocumentManagement() {
  const [file, setFile] = useState(null);
  const [docs, setDocs] = useState([]);
  const [error, setError] = useState('');
  const [success, setSuccess] = useState('');
  const [loading, setLoading] = useState(false);
  const [loadingDocs, setLoadingDocs] = useState(false);

  const fetchDocs = async () => {
    setLoadingDocs(true);
    try {
      const docs = await listDocuments(getToken());
      setDocs(docs);
    } catch (err) {
      setError('Could not fetch documents: ' + (err.message || 'Unknown error'));
    }
    setLoadingDocs(false);
  };

  useEffect(() => {
    fetchDocs();
    // eslint-disable-next-line
  }, []);

  const handleUpload = async (e) => {
    e.preventDefault();
    setError('');
    setSuccess('');
    setLoading(true);
    if (!file) return;
    try {
      await uploadDocument(file, getToken());
      setSuccess('Upload successful');
      setFile(null);
      fetchDocs();
    } catch (err) {
      setError('Upload failed: ' + (err.message || 'Unknown error'));
    }
    setLoading(false);
  };

  return (
    <div>
      <h2>Document Management</h2>
      <form onSubmit={handleUpload}>
        <input type="file" onChange={e => setFile(e.target.files[0])} disabled={loading} />
        <button type="submit" disabled={!file || loading}>{loading ? 'Uploading...' : 'Upload'}</button>
      </form>
      {error && <div style={{ color: 'red' }}>{error}</div>}
      {success && <div style={{ color: 'green' }}>{success}</div>}
      <h3>Uploaded Documents</h3>
      {loadingDocs ? <div>Loading...</div> : (
        <ul>
          {docs.map((doc, i) => (
            <li key={i}>{doc.filename} (by {doc.uploader} at {doc.upload_time})</li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default DocumentManagement; 