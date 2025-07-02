import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';

const Login = () => {
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();

    const storedUser = JSON.parse(localStorage.getItem('penziUser'));

    if (!storedUser) {
      alert('No account found. Please sign up first.');
      return;
    }

    if (storedUser.phone === phone && storedUser.password === password) {
      navigate('/chat');
    } else {
      alert('Incorrect phone number or password');
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleLogin}
        className="bg-white p-6 rounded-lg shadow-md max-w-sm w-full"
      >
        <h2 className="text-xl font-bold text-center mb-4">Login</h2>

        {/* Phone input with digit restriction */}
        <input
          type="text"
          value={phone}
          onChange={(e) => setPhone(e.target.value.replace(/[^0-9]/g, ''))}
          placeholder="Phone Number"
          className="border p-2 w-full mb-3 rounded"
          maxLength={10}
        />

        {/* Password input */}
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="border p-2 w-full mb-4 rounded"
        />

        {/* Submit button */}
        <button
          type="submit"
          className="w-full bg-red-500 text-white py-2 rounded hover:bg-pink-600"
        >
          Login
        </button>

        
        <p className="text-center text-sm mt-4">
          Don't have an account?{' '}
          <a href="/signup" className="text-red-500 underline">
            Sign Up
          </a>
        </p>
      </form>
    </div>
  );
};

export default Login;
