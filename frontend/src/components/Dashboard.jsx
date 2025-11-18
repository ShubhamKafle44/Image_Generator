import { useState } from "react";
import Navbar from "./Navbar";
import ImageGenerator from "./ImageGenerator";
import Results from "./Results";

export default function Dashboard() {
    const pages = ["generate", "results"];
    const [activePage, setActivePage] = useState("generate");

    return (
        <div className="min-h-screen text-white">
            {/* Navbar */}
            <Navbar pages={pages} activePage={activePage} setActivePage={setActivePage} />

            <main>
                {/* Image Generator Section */}
                {activePage === "generate" && (
                    <ImageGenerator />
                )}

                {/* Results Section */}
                {activePage === "results" && (
                    <Results setActivePage={setActivePage} />
                )}
            </main>
        </div>
    );
}