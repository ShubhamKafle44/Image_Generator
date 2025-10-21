import LoadingSpinner from "./LoadingSpinner";

export default function PromptControls({
    prompt,
    setPrompt,
    numInferenceSteps,
    setNumInferenceSteps,
    guidanceScale,
    setGuidanceScale,
    handleGenerate,
    loading,
    error
}) {
    return (
        <div className="flex flex-col gap-4 sm:gap-6">
            <textarea
                value={prompt}
                onChange={(e) => setPrompt(e.target.value)}
                placeholder="Describe your vision..."
                rows="6"
                className="w-full px-4 py-3 bg-white/5 border-2 border-white/20 rounded-2xl text-white placeholder-purple-300 focus:outline-none focus:ring-2 focus:ring-purple-500 resize-none text-sm sm:text-base"
            />

            <div>
                <label className="flex justify-between text-purple-200 font-semibold text-sm sm:text-base mb-2">
                    <span>Quality (Inference Steps)</span>
                    <span className="bg-purple-600 px-3 py-1 rounded-full text-xs">{numInferenceSteps}</span>
                </label>
                <input
                    type="range"
                    min="10"
                    max="500"
                    value={numInferenceSteps}
                    onChange={(e) => setNumInferenceSteps(Number(e.target.value))}
                    className="w-full h-2 bg-white/20 rounded-lg accent-purple-500 cursor-pointer"
                />
                <div className="flex justify-between text-xs text-purple-300 mt-1">
                    <span>Fast</span>
                    <span>High Quality</span>
                </div>
            </div>

            <div>
                <label className="flex justify-between text-purple-200 font-semibold text-sm sm:text-base mb-2">
                    <span>Creativity (Guidance Scale)</span>
                    <span className="bg-purple-600 px-3 py-1 rounded-full text-xs">{guidanceScale}</span>
                </label>
                <input
                    type="range"
                    min="5"
                    max="15"
                    step="0.5"
                    value={guidanceScale}
                    onChange={(e) => setGuidanceScale(Number(e.target.value))}
                    className="w-full h-2 bg-white/20 rounded-lg accent-purple-500 cursor-pointer"
                />
                <div className="flex justify-between text-xs text-purple-300 mt-1">
                    <span>Creative</span>
                    <span>Precise</span>
                </div>
            </div>

            {error && (
                <p className="text-red-400 font-semibold text-sm bg-red-500/20 p-3 rounded-xl border border-red-500/50">
                    {error}
                </p>
            )}

            <button
                onClick={handleGenerate}
                disabled={loading}
                className="mt-auto px-6 py-4 bg-gradient-to-r from-purple-600 to-pink-600 hover:from-purple-700 hover:to-pink-700 text-white font-bold text-lg sm:text-xl rounded-2xl shadow-xl hover:scale-105 active:scale-95 transition-all duration-200 disabled:opacity-50 disabled:cursor-not-allowed"
            >
                {loading ? (
                    <span className="flex items-center justify-center gap-3">
                        <LoadingSpinner />
                        Generating Magic...
                    </span>
                ) : (
                    "Generate Image ✨"
                )}
            </button>
        </div>
    );
}
