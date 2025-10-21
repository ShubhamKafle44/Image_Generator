import "./App.css";
import React, { useState } from "react";
import Navbar from "./components/Navbar";
import ImageGenerator from "./components/ImageGenerator";
import Results from "./components/Results";

export default function App() {
  const [activePage, setActivePage] = useState("home");
  const pages = ["home", "results"]; // can add more pages later

  return (
    <div className="min-h-screen min-w-screen flex flex-col bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 text-white">
      {/* Fixed Navbar */}
      <Navbar pages={pages} activePage={activePage} setActivePage={setActivePage} />

      {/* Page Content */}
      <main className="flex-1 pt-20 px-4 sm:px-6 pb-10">
        {activePage === "home" && <ImageGenerator />}
        {activePage === "results" && <Results setActivePage={setActivePage} />}
      </main>
    </div>
  );
}
