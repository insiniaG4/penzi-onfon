import React, { useState, useEffect } from 'react';

const LoadingPage = ({ onLoadingComplete }) => {
  const [progress, setProgress] = useState(0);
  const [loadingText, setLoadingText] = useState('Initializing...');

  useEffect(() => {
    const loadingSteps = [
      { progress: 20, text: 'Loading components...' },
      { progress: 40, text: 'Connecting to server...' },
      { progress: 60, text: 'Setting up chat interface...' },
      { progress: 80, text: 'Finalizing setup...' },
      { progress: 100, text: 'Ready!' }
    ];

    let currentStep = 0;
    const interval = setInterval(() => {
      if (currentStep < loadingSteps.length) {
        setProgress(loadingSteps[currentStep].progress);
        setLoadingText(loadingSteps[currentStep].text);
        currentStep++;
      } else {
        clearInterval(interval);
        setTimeout(() => {
          onLoadingComplete();
        }, 500);
      }
    }, 800);

    return () => clearInterval(interval);
  }, [onLoadingComplete]);

  return (
    <div className="fixed inset-0 bg-gradient-to-r from-pink-500 via-red-500 to-rose-600 flex items-center justify-center">
      {/* Background animation */}
      <div className="absolute inset-0 overflow-hidden">
        <div className="absolute -top-40 -right-40 w-80 h-80 bg-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob"></div>
        <div className="absolute -bottom-40 -left-40 w-80 h-80 bg-red-500 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-2000"></div>
        <div className="absolute top-40 left-40 w-80 h-80 bg-rose-600 rounded-full mix-blend-multiply filter blur-xl opacity-70 animate-blob animation-delay-4000"></div>
      </div>

      {/* Main loading content */}
      <div className="relative z-10 text-center">
        {/* Logo/Brand */}
        <div className="mb-8">
          <h1 className="text-6xl font-bold text-white mb-4 tracking-wider">
            PENZI
          </h1>
          <p className="text-xl text-gray-300 font-light">
            Connect • Chat • Share
          </p>
        </div>

        {/* Loading spinner */}
        <div className="mb-8">
          <div className="relative w-24 h-24 mx-auto">
            <div className="absolute inset-0 border-4 border-gray-600 rounded-full"></div>
            <div className="absolute inset-0 border-4 border-transparent border-t-white rounded-full animate-spin"></div>
            <div className="absolute inset-2 border-4 border-transparent border-t-rose-400 rounded-full animate-spin animate-reverse"></div>
          </div>
        </div>

        {/* Progress bar */}
        <div className="w-80 mx-auto mb-6">
          <div className="bg-gray-700 rounded-full h-2 overflow-hidden">
            <div 
              className="bg-gradient-to-r from-pink-500 to-rose-600 h-full rounded-full transition-all duration-500 ease-out"
              style={{ width: `${progress}%` }}
            ></div>
          </div>
          <div className="text-center mt-2">
            <span className="text-white text-sm font-medium">{progress}%</span>
          </div>
        </div>

        {/* Loading text */}
        <div className="text-gray-300 text-lg font-medium min-h-[1.5rem]">
          {loadingText}
        </div>

        {/* Dots animation */}
        <div className="flex justify-center space-x-1 mt-4">
          <div className="w-2 h-2 bg-white rounded-full animate-bounce"></div>
          <div className="w-2 h-2 bg-white rounded-full animate-bounce animation-delay-200"></div>
          <div className="w-2 h-2 bg-white rounded-full animate-bounce animation-delay-400"></div>
        </div>
      </div>
    </div>
  );
};

export default LoadingPage;