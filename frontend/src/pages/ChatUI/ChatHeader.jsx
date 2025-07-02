import React, { useState, useEffect } from 'react';

const ChatHeader = () => {
  const [user, setUser] = useState(null);

  useEffect(() => {
    // Replace with actual auth logic later
    const mockUser = { phone: '+254712345678' };
    setUser(mockUser);
  }, []);

  return (
    <div className="bg-gradient-to-r from-pink-500 via-red-500 to-rose-600 text-white relative overflow-hidden rounded-t-2xl">
      <div className="absolute inset-0 bg-black/10"></div>

      <div className="relative z-10 text-center py-4 px-4">
        <div className="flex items-center justify-center gap-2 mb-1">
          <span className="text-xl animate-pulse"></span>
          <h2 className="text-lg font-bold">PENZI Dating Assistant</h2>
          <span className="text-lg"></span>
        </div>

        <p className="text-sm text-pink-100 opacity-90">Find your perfect match • 22141</p>

        {user?.phone && (
          <div className="flex items-center justify-center gap-1 mt-2 text-xs bg-white/20 rounded-full px-3 py-1 backdrop-blur-sm">
            
            <span>{user.phone}</span>
          </div>
        )}
      </div>

      {/* Decorative circles */}
      <div className="absolute top-0 right-0 w-32 h-32 bg-white/5 rounded-full -translate-y-16 translate-x-16"></div>
      <div className="absolute bottom-0 left-0 w-24 h-24 bg-white/5 rounded-full translate-y-12 -translate-x-12"></div>
    </div>
  );
};

export default ChatHeader;
