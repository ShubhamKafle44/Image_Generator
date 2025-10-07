import React, { useState, useRef, useEffect } from "react";
import ImageUpload from "./ImageUpload";
import PromptControls from "./PromptControls";
import ResultView from "./ResultView";

export default function ImageGenerator() {
    const [uploadedImage, setUploadedImage] = useState(null);
    const [uploadedImagePreview, setUploadedImagePreview] = useState(null);
    const [prompt, setPrompt] = useState("");
    const [numInferenceSteps, setNumInferenceSteps] = useState(30);
    const [guidanceScale, setGuidanceScale] = useState(10);
    const [generatedImage, setGeneratedImage] = useState(null);
    const [loading, setLoading] = useState(false);
    const [showResult, setShowResult] = useState(false);
    const [error, setError] = useState(null);

    const formRef = useRef(null);
    const resultRef = useRef(null);

    const fileInputRef = useRef(null);
    const overlayRef = useRef(null);

    // Animate overlay in
    useEffect(() => {
        if (showResult && overlayRef.current) {
            overlayRef.current.style.animation = "overlayFadeIn 0.5s ease-out forwards";
        }
    }, [showResult]);

    const handleImageUpload = (e) => {
        const file = e.target.files[0];
        if (file) {
            if (!["image/jpeg", "image/png"].includes(file.type)) {
                setError("Please upload a valid JPG or PNG image");
                return;
            }
            setUploadedImage(file);
            setUploadedImagePreview(URL.createObjectURL(file));
            setError(null);
        }
    };

    const handleGenerate = async () => {
        if (!uploadedImage) {
            setError("Please upload an image first");
            return;
        }
        if (!prompt.trim()) {
            setError("Please enter a prompt");
            return;
        }
        console.log("Okay")

        setLoading(true);
        setError(null);

        const formData = new FormData();
        formData.append("image_file", uploadedImage);
        formData.append("prompt", prompt);
        formData.append("num_inference_steps", numInferenceSteps);
        formData.append("guidance_scale", guidanceScale);

        try {
            const response = await fetch("/api/generate", {
                method: "POST",
                body: formData
            });

            if (!response.ok) {
                const errorData = await response.json().catch(() => ({}));
                throw new Error(errorData.message || "Failed to generate image");
            }

            const blob = await response.blob();
            setGeneratedImage(URL.createObjectURL(blob));
            setLoading(false);

            // Show overlay with result
            setTimeout(() => {
                setShowResult(true);
            }, 100);
        } catch (err) {
            setError(err.message || "Failed to generate image. Please try again.");
            setLoading(false);
        }
    };

    const handleGenerateAgain = () => {
        if (overlayRef.current) {
            overlayRef.current.style.animation = "overlayFadeOut 0.5s ease-in forwards";
            setTimeout(() => {
                setShowResult(false);
                setGeneratedImage(null);
                setLoading(false);
            }, 500);
        }
    };

    const handleDownload = () => {
        if (!generatedImage) return;
        const link = document.createElement("a");
        link.href = generatedImage;
        link.download = `generated-image-${Date.now()}.png`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div className="h-screen w-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 overflow-auto flex items-center justify-center px-4 sm:px-6 py-6">
            {!showResult && (
                <div
                    ref={formRef}
                    className="w-full max-w-5xl flex flex-col gap-6 sm:gap-8"
                >
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-6 sm:gap-8">
                        <ImageUpload
                            uploadedImagePreview={uploadedImagePreview}
                            fileInputRef={fileInputRef}
                            setUploadedImage={setUploadedImage}
                            setUploadedImagePreview={setUploadedImagePreview}
                            setError={setError}
                        />
                        <PromptControls
                            prompt={prompt}
                            setPrompt={setPrompt}
                            numInferenceSteps={numInferenceSteps}
                            setNumInferenceSteps={setNumInferenceSteps}
                            guidanceScale={guidanceScale}
                            setGuidanceScale={setGuidanceScale}
                            error={error}
                            loading={loading}
                            handleGenerate={handleGenerate}
                        />
                    </div>
                </div>
            )}

            {showResult && generatedImage && (
                <ResultView
                    generatedImage={generatedImage}
                    numInferenceSteps={numInferenceSteps}
                    guidanceScale={guidanceScale}
                    prompt={prompt}
                    handleDownload={() => {
                        const link = document.createElement("a");
                        link.href = generatedImage;
                        link.download = `generated-image-${Date.now()}.png`;
                        document.body.appendChild(link);
                        link.click();
                        document.body.removeChild(link);
                    }}
                    handleGenerateAgain={handleGenerateAgain}
                    ref={resultRef}
                />
            )}
        </div>


    );
}
