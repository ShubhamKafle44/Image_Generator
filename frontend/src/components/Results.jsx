import React, { useEffect, useState } from "react";

export default function Results({ setActivePage }) {
    const [results, setResults] = useState([]);

    useEffect(() => {
        const storedResults = JSON.parse(localStorage.getItem("results")) || [];
        setResults(storedResults);
    }, []);

    const handleClear = () => {
        if (window.confirm("Are you sure you want to clear all past results?")) {
            localStorage.removeItem("results");
            setResults([]);
        }
    };

    if (results.length === 0) {
        return (
            <div className="w-full flex flex-col items-center justify-center min-h-[calc(100vh-4rem)] bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white px-4">
                <div className="bg-slate-800 p-8 rounded-xl shadow-lg text-center max-w-md w-full">
                    <p className="text-xl sm:text-2xl font-medium mb-4">No past results found.</p>
                    <button
                        onClick={() => setActivePage("home")}
                        className="bg-purple-600 hover:bg-purple-700 text-white px-6 py-2 rounded-lg transition"
                    >
                        Go Back
                    </button>
                </div>
            </div>
        );
    }



    return (
        <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 p-8 text-white">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Past Results</h1>
                <div className="flex gap-4">
                    <button
                        onClick={() => setActivePage("home")}
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
                        className="bg-slate-800 rounded-2xl overflow-hidden shadow-lg hover:shadow-xl transition-shadow"
                    >
                        <img
                            src={res.imageUrl}
                            alt={res.prompt}
                            className="w-full h-64 object-cover"
                        />
                        <div className="p-4">
                            <p className="text-sm text-gray-300 mb-2 line-clamp-2">
                                <strong>Prompt:</strong> {res.prompt}
                            </p>
                            <p className="text-xs text-gray-400">
                                Steps: {res.numInferenceSteps} | Guidance: {res.guidanceScale}
                            </p>
                            <p className="text-xs text-gray-500 mt-2">
                                {new Date(res.timestamp).toLocaleString()}
                            </p>

                            <button
                                onClick={() => {
                                    const link = document.createElement("a");
                                    link.href = res.imageUrl;
                                    link.download = `result-${res.id}.png`;
                                    document.body.appendChild(link);
                                    link.click();
                                    document.body.removeChild(link);
                                }}
                                className="mt-3 w-full bg-purple-600 hover:bg-purple-700 px-3 py-2 rounded-lg text-sm transition"
                            >
                                Download
                            </button>
                        </div>
                    </div>
                ))}
            </div>
        </div>
    );
}
