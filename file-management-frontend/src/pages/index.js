// pages/index.js
import FileList from "../components/FileList";
import UploadForm from "../components/UploadForm";

export default function Home({ files, fetchFiles }) {
  return (
    <div>
      <UploadForm fetchFiles={fetchFiles} />
      <FileList files={files} fetchFiles={fetchFiles} />
    </div>
  );
}
