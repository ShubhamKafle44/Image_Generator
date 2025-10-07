import "./App.css"
import React, { useState } from "react";
import Navbar from "./components/Navbar";
import ImageGenerator from "./components/ImageGenerator";
import ResultView from "./components/ResultView";

export default function App() {
  const [activePage, setActivePage] = useState("home");
  const pages = ["home", "results"]; // can add more dynamically

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900">
      <Navbar pages={pages} activePage={activePage} setActivePage={setActivePage} />
      <div className="pt-16 px-4 sm:px-6"> {/* padding for fixed navbar */}
        {activePage === "home" && <ImageGenerator />}
        {activePage === "results" && <ResultView />}
      </div>
    </div>
  );
}


