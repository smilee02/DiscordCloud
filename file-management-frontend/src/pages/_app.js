// pages/_app.js
import { useState, useEffect } from "react";
import "../styles/globals.css";

function MyApp({ Component, pageProps }) {
  const [files, setFiles] = useState([]);
  const apiHost = process.env.NEXT_PUBLIC_API_HOST;

  const fetchFiles = async () => {
    const res = await fetch(`http://${apiHost}:5000/api/files`);
    const data = await res.json();
    setFiles(data);
  };

  useEffect(() => {
    fetchFiles();
  }, []);

  return <Component {...pageProps} files={files} fetchFiles={fetchFiles} />;
}

export default MyApp;
