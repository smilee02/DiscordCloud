import { useState } from "react";
import { FaTrash } from "react-icons/fa"; // Import trash icon from react-icons/fa
import styles from "../styles/UploadForm.module.css"; // Import the CSS module

export default function UploadForm({ fetchFiles }) {
  const [uploadingFiles, setUploadingFiles] = useState([]);
  const [progress, setProgress] = useState({});
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [uploadClicked, setUploadClicked] = useState(false);
  const [elapsedTime, setElapsedTime] = useState({});
  const [uploadErrors, setUploadErrors] = useState({});
  const apiHost = process.env.NEXT_PUBLIC_API_HOST;

  const uploadFile = async (file) => {
    const formData = new FormData();
    formData.append("file", file);

    const startTime = Date.now();

    const xhr = new XMLHttpRequest();
    xhr.open("POST", `http://${apiHost}:5000/api/upload`, true);

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable) {
        const percentCompleted = parseInt((event.loaded / event.total) * 100);
        setProgress((prevProgress) => ({
          ...prevProgress,
          [file.name]: percentCompleted,
        }));
      }
    };

    xhr.onload = () => {
      if (xhr.status === 200) {
        fetchFiles();
        setProgress((prevProgress) => {
          const { [file.name]: _, ...rest } = prevProgress;
          return rest;
        });
        setSelectedFiles((prevSelectedFiles) =>
          prevSelectedFiles.filter((selectedFile) => selectedFile !== file)
        );
        setElapsedTime((prevElapsedTime) => {
          const newElapsedTime = { ...prevElapsedTime };
          delete newElapsedTime[file.name]; // Remove elapsed time for this file
          return newElapsedTime;
        });
        setUploadingFiles((prevUploadingFiles) =>
          prevUploadingFiles.filter((uploadingFile) => uploadingFile !== file)
        );
      } else if (xhr.status === 400) {
        const response = JSON.parse(xhr.responseText);
        setUploadErrors((prevErrors) => ({
          ...prevErrors,
          [file.name]: response.message,
        }));
      }
    };

    xhr.send(formData);

    // Start the timer for the current file
    setUploadingFiles((prevUploadingFiles) => [...prevUploadingFiles, file]);

    // Start the timer for the current file
    const interval = setInterval(() => {
      setElapsedTime((prevElapsedTime) => {
        const newElapsedTime = { ...prevElapsedTime };
        newElapsedTime[file.name] = Math.floor((Date.now() - startTime) / 1000);
        return newElapsedTime;
      });
    }, 1000);

    // Clean up the interval when the upload is complete
    xhr.onloadend = () => clearInterval(interval);
  };

  const handleFileChange = (e) => {
    const files = Array.from(e.target.files);
    setSelectedFiles(files);
    setUploadClicked(false);
  };

  const handleUploadButtonClick = () => {
    setUploadingFiles([...selectedFiles]);
    setProgress({});
    setUploadErrors({});
    setUploadClicked(true);

    selectedFiles.forEach((file) => {
      uploadFile(file);
    });
  };

  const handleRemoveFile = (file) => {
    setSelectedFiles((prevSelectedFiles) =>
      prevSelectedFiles.filter((selectedFile) => selectedFile !== file)
    );
    setUploadErrors((prevErrors) => {
      const { [file.name]: _, ...rest } = prevErrors;
      return rest;
    });
  };

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>File Manager</h1>
      <div className={styles["file-upload"]}>
        <input type="file" onChange={handleFileChange} multiple />
        <button
          className={styles["file-upload-btn"]}
          onClick={handleUploadButtonClick}
        >
          Upload Files
        </button>
      </div>
      {uploadClicked && (
        <div className={styles["file-list"]}>
          {selectedFiles.map((file) => (
            <div
              className={`${styles["file-item"]} ${
                uploadErrors[file.name] && styles.error
              }`}
              key={file.name}
            >
              <div className={styles["file-info"]}>
                <span className={styles["file-name"]}>{file.name}</span>
                {elapsedTime[file.name] !== undefined && ( // Check if elapsed time exists
                  <div className={styles["elapsed-time"]}>
                    Elapsed Time: {elapsedTime[file.name]} seconds
                  </div>
                )}
                {uploadErrors[file.name] && (
                  <div className={styles.errorContainer}>
                    <span className={styles.errorMessage}>
                      Error: {uploadErrors[file.name]}
                    </span>
                    <button
                      className={styles.removeButton}
                      onClick={() => handleRemoveFile(file)}
                    >
                      <FaTrash />
                    </button>
                  </div>
                )}
              </div>
              {uploadingFiles.includes(file) && (
                <progress
                  className={styles["progress-bar"]}
                  value={progress[file.name] || 0}
                  max="100"
                />
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
