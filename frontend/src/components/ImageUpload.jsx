import React from "react";

export default function ImageUpload({
    uploadedImagePreview,
    fileInputRef,
    setUploadedImage,
    setUploadedImagePreview,
    setError,
}) {
    const handleFileChange = (e) => {
        const file = e.target.files[0];
        if (!file) return;

        if (!file.type.startsWith("image/")) {
            setError("Please upload a valid image file");
            return;
        }

        setUploadedImage(file);
        setUploadedImagePreview(URL.createObjectURL(file));
        setError(null);
    };

    const handleButtonClick = () => {
        if (fileInputRef.current) {
            fileInputRef.current.click(); // triggers hidden file input
        }
    };

    return (
        <div className="flex flex-col items-center justify-center border-2 border-dashed border-gray-400 p-6 rounded-lg">
            {uploadedImagePreview ? (
                <img
                    src={uploadedImagePreview}
                    alt="Preview"
                    className="w-full h-64 object-contain mb-4"
                />
            ) : (
                <div className="text-gray-300 mb-4">No image uploaded</div>
            )}

            <button
                type="button"
                onClick={handleButtonClick}
                className="px-4 py-2 bg-purple-700 text-white rounded hover:bg-purple-800"
            >
                Upload Image
            </button>

            <input
                type="file"
                ref={fileInputRef}
                onChange={handleFileChange}
                className="hidden"
                accept="image/*"
            />
        </div>
    );
}
