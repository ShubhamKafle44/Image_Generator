import React from "react";

export default function ResultView({ generatedImage, onDownload, onGenerateAgain, numInferenceSteps, guidanceScale, prompt }) {
    return (
        <div className="w-full max-w-6xl bg-white/10 backdrop-blur-xl rounded-3xl p-6 sm:p-8 shadow-2xl border border-white/20 flex flex-col gap-6 sm:gap-8">
            <div className="text-center">
                <h2 className="text-4xl sm:text-5xl font-bold text-white mb-2">🎨 Your Masterpiece</h2>
                <p className="text-purple-200 text-base sm:text-lg">Generated with AI Magic</p>
            </div>

            <div className="bg-gradient-to-br from-slate-800 to-slate-900 rounded-2xl p-4 sm:p-6 border border-white/10">
                <img src={generatedImage} alt="Generated" className="w-full h-auto rounded-xl shadow-2xl" />
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <button
                    onClick={onDownload}
                    className="px-6 py-4 bg-gradient-to-r from-green-600 to-emerald-600 hover:from-green-700 hover:to-emerald-700 text-white font-bold text-lg rounded-2xl shadow-xl hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2"
                >
                    Download Image
                </button>
                <button
                    onClick={onGenerateAgain}
                    className="px-6 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold text-lg rounded-2xl shadow-xl hover:scale-105 active:scale-95 transition-all duration-200 flex items-center justify-center gap-2"
                >
                    Generate Again
                </button>
            </div>

            <div className="p-4 sm:p-6 bg-white/5 rounded-2xl border border-white/10">
                <h3 className="text-white font-bold text-lg mb-4">Generation Details</h3>
                <div className="grid grid-cols-2 gap-4 sm:gap-6 text-sm sm:text-base">
                    <div>
                        <p className="text-purple-300 font-semibold">Inference Steps</p>
                        <p className="text-white font-bold text-xl">{numInferenceSteps}</p>
                    </div>
                    <div>
                        <p className="text-purple-300 font-semibold">Guidance Scale</p>
                        <p className="text-white font-bold text-xl">{guidanceScale}</p>
                    </div>
                </div>
                {prompt && (
                    <div className="mt-4 pt-4 border-t border-white/10">
                        <p className="text-purple-300 font-semibold mb-2 text-sm">Prompt Used</p>
                        <p className="text-white italic text-sm sm:text-base">"{prompt}"</p>
                    </div>
                )}
            </div>
        </div>
    );
}
