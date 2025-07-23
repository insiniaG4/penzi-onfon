import React, { useState, useEffect } from "react";
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import Login from "./pages/authentication/Login";
import Signup from "./pages/authentication/Signup";
import ChatBox from "./pages/ChatUI/ChatBox";
import LoadingPage from "./components/LoadingPage";

function App() {
  const [isLoading, setIsLoading] = useState(true);

  const handleLoadingComplete = () => {
    setIsLoading(false);
  };

  if (isLoading) {
    return <LoadingPage onLoadingComplete={handleLoadingComplete} />;
  }

  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/" element={<ChatBox />} />
      </Routes>
    </Router>
  );
}

export default App;
