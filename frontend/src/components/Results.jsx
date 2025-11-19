import React, { useEffect, useState } from "react";
import { useUser } from "@clerk/clerk-react";

export default function Results({ setActivePage }) {
    const [results, setResults] = useState([]);
    const [loading, setLoading] = useState(true);
    const { user } = useUser();

    useEffect(() => {
        if (!user) return;

        const fetchResults = async () => {
            try {
                const response = await fetch(`/api/user/results?user_id=${encodeURIComponent(user.id)}`);
                if (!response.ok) throw new Error("Failed to fetch results");

                const data = await response.json();
                setResults(Array.isArray(data) ? data : []);
            } catch (error) {
                console.error("Failed to fetch user results:", error);
                setResults([]);
            } finally {
                setLoading(false);
            }
        };

        fetchResults();
    }, [user]);

    const handleClear = async () => {
        if (!window.confirm("Are you sure you want to clear all past results?")) return;

        try {
            const response = await fetch(`/api/user/results?user_id=${user.id}`, {
                method: "DELETE",
            });
            await response.json();
            setResults([]);
        } catch (error) {
            console.error("Failed to clear results:", error);
            alert("Failed to clear results. Try again later.");
        }
    };

    if (loading) {
        return (
            <div className="w-full flex items-center justify-center min-h-screen text-white">
                <p>Loading past results...</p>
            </div>
        );
    }

    if (results.length === 0) {
        return (
            <div className="w-full flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white px-4">
                <div className="bg-slate-800 p-8 rounded-xl shadow-lg text-center max-w-md w-full">
                    <p className="text-xl sm:text-2xl font-medium mb-4">No past results found.</p>
                    <button
                        onClick={() => setActivePage("generate")}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg transition"
                    >
                        Go Back
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-4 sm:p-8 text-white">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center mb-6 gap-4 sm:gap-0">
                <h1 className="text-3xl font-bold">Past Results</h1>
                <div className="flex gap-4 flex-wrap">
                    <button
                        onClick={() => setActivePage("generate")}
                        className="bg-purple-600 hover:bg-purple-700 px-4 py-2 rounded-lg transition"
                    >
                        Generate New
                    </button>
                    <button
                        onClick={handleClear}
                        className="bg-red-600 hover:bg-red-700 px-4 py-2 rounded-lg transition"
                    >
                        Clear All
                    </button>
                </div>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                {results.map((res) => (
                    <div
                        key={res.id}
                        className="bg-slate-800 rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow flex flex-col"
                    >
                        {/* Original + Generated images side by side */}
                        <div className="grid grid-cols-2 gap-2 p-2 bg-slate-900">
                            <div>
                                <p className="text-xs text-gray-400 mb-1 text-center">Original</p>
                                <img
                                    src={res.original_image_url}
                                    alt="Original"
                                    className="w-full h-40 object-cover rounded-lg"
                                />
                            </div>

                            <div>
                                <p className="text-xs text-gray-400 mb-1 text-center">Generated</p>
                                <img
                                    src={res.generated_image_url}
                                    alt="Generated"
                                    className="w-full h-40 object-cover rounded-lg"
                                />
                            </div>
                        </div>

                        <div className="p-4 flex flex-col flex-1 justify-between">
                            <div>
                                <p className="text-sm text-gray-300 mb-2 line-clamp-2">
                                    <strong>Prompt:</strong> {res.prompt}
                                </p>

                                <p className="text-xs text-gray-400">
                                    Steps: {res.num_inference_steps} | Guidance: {res.guidance_scale}
                                </p>

                                <p className="text-xs text-gray-500 mt-2">
                                    {new Date(res.timestamp).toLocaleString()}
                                </p>
                            </div>

                            <div className="flex gap-2 mt-3">
                                <button
                                    onClick={() => {
                                        const link = document.createElement("a");
                                        link.href = res.original_image_url;
                                        link.download = `original-${res.id}.png`;
                                        document.body.appendChild(link);
                                        link.click();
                                        document.body.removeChild(link);
                                    }}
                                    className="flex-1 bg-gray-600 hover:bg-gray-700 px-3 py-2 rounded-lg text-sm transition"
                                >
                                    Download Original
                                </button>

                                <button
                                    onClick={() => {
                                        const link = document.createElement("a");
                                        link.href = res.generated_image_url;
                                        link.download = `generated-${res.id}.png`;
                                        document.body.appendChild(link);
                                        link.click();
                                        document.body.removeChild(link);
                                    }}
                                    className="flex-1 bg-purple-600 hover:bg-purple-700 px-3 py-2 rounded-lg text-sm transition"
                                >
                                    Download Generated
                                </button>
                            </div>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
