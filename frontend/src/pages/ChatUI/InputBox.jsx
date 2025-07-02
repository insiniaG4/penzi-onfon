import React, { useRef } from 'react';

const InputBox = ({ input, setInput, handleSend, step }) => {
  const inputRef = useRef(null);

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  const getPlaceholder = () => {
    switch (step) {
      case 'welcome':
        return 'Say hello to get started...';
      case 'basic':
        return 'Type: start#name#age#gender#county#town';
      case 'choose_edu':
        return 'Choose education level (1-5)...';
      case 'choose_prof':
        return 'Enter your profession...';
      case 'description':
        return 'Start with: MYSELF I am...';
      case 'match':
        return 'Type: match#ageRange#town';
      default:
        return 'Type your message...';
    }
  };

  return (
    <div className="border-t border-gray-200 px-4 py-4 bg-gray-50 rounded-b-2xl">
      <div className="flex gap-3 items-end">
        <div className="flex-1 relative">
          <input
            ref={inputRef}
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={handleKeyPress}

            placeholder={getPlaceholder()}
            className="w-full border border-gray-300 rounded-full px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-pink-500 focus:border-transparent transition-all duration-200 bg-white shadow-sm"
          />
          {step === 'match' && (
            <div className="absolute right-3 top-1/2 transform -translate-y-1/2 text-pink-400 text-sm">
              
            </div>
          )}
        </div>

        <button
          onClick={handleSend}
          disabled={!input.trim()}
          className="bg-gradient-to-r from-pink-500 to-red-500 text-white p-3 rounded-full text-sm font-medium shadow-lg hover:shadow-xl transform hover:scale-105 transition-all duration-200 disabled:opacity-50 disabled:transform-none disabled:hover:shadow-lg"
        >
          📩
        </button>
      </div>

      {step === 'basic' && (
        <div className="mt-2 text-xs text-gray-500 flex items-center gap-1">
          <span>💬</span>
          <span>Example: start#John#25#male#Nairobi#Westlands</span>
        </div>
      )}
    </div>
  );
};

export default InputBox;
