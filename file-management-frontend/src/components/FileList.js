import { useState } from "react";
import styles from "../styles/FileList.module.css";

export default function FileList({ files, fetchFiles }) {
  const [showFileNames, setShowFileNames] = useState(false);
  const apiHost = process.env.NEXT_PUBLIC_API_HOST;

  const downloadFile = (fileId) => {
    window.location.href = `http://${apiHost}:5000/api/download?id=${fileId}`;
  };

  const deleteFile = async (fileId) => {
    await fetch(`http://${apiHost}:5000/api/delete?id=${fileId}`, {
      method: "DELETE",
    });
    fetchFiles();
  };

  const toggleFileNames = () => {
    setShowFileNames(!showFileNames);
  };

  return (
    <div className={styles.fileListContainer}>
      <button className={styles.toggleBtn} onClick={toggleFileNames}>
        {showFileNames ? "Hide File Names" : "Show File Names"}
      </button>
      <table className={styles.table}>
        <thead>
          <tr>
            <th className={styles.columnName}>Name</th>
            <th className={styles.columnExtension}>Extension</th>
            <th className={styles.columnSize}>Size</th>
            <th className={styles.columnDownload}>Download</th>
            <th className={styles.columnDelete}>Delete</th>
          </tr>
        </thead>
        <tbody>
          {files.map((file) => (
            <tr key={file.id}>
              <td className={showFileNames ? styles.fileName : styles.hidden}>
                {showFileNames ? file.name : "<file name hidden>"}
              </td>
              <td>{file.file_type}</td>
              <td>{formatBytes(file.total_size)}</td>
              <td>
                <button
                  className={`${styles.button} ${styles.downloadBtn}`}
                  onClick={() => downloadFile(file.id)}
                >
                  Download
                </button>
              </td>
              <td>
                <button
                  className={`${styles.button} ${styles.deleteBtn}`}
                  onClick={() => deleteFile(file.id)}
                >
                  Delete
                </button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}

function formatBytes(bytes, decimals = 2) {
  if (!+bytes) return "0 Bytes";

  const k = 1024;
  const dm = decimals < 0 ? 0 : decimals;
  const sizes = ["B", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"];

  const i = Math.floor(Math.log(bytes) / Math.log(k));

  return `${parseFloat((bytes / Math.pow(k, i)).toFixed(dm))} ${sizes[i]}`;
}
