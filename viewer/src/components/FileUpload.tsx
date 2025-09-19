import React from 'react';

interface FileUploadProps {
  onFileUpload: (event: React.ChangeEvent<HTMLInputElement>) => void;
}

export const FileUpload: React.FC<FileUploadProps> = ({ onFileUpload }) => {
  return (
    <div>
      <input
        type="file"
        accept=".json"
        onChange={onFileUpload}
        className="hidden"
        id="file-upload"
      />
      <label
        htmlFor="file-upload"
        className="w-full px-3 py-2 bg-gray-100 text-gray-700 rounded border border-gray-300 hover:bg-gray-200 cursor-pointer text-center block"
      >
        Upload JSON
      </label>
    </div>
  );
};
