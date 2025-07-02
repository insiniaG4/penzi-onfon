import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';

const Signup = () => {
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleSignup = (e) => {
    e.preventDefault();

    if (phone.length < 10 || password.length < 4) {
      alert('Enter valid phone number and password');
      return;
    }

    localStorage.setItem('penziUser', JSON.stringify({ phone, password }));
    navigate('/chat');
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <form
        onSubmit={handleSignup}
        className="bg-white p-6 rounded-lg shadow-md max-w-sm w-full"
      >
        <h2 className="text-xl font-bold text-center mb-4">Sign Up</h2>

        <input
          type="text"
          value={phone}
          onChange={(e) => setPhone(e.target.value.replace(/[^0-9]/g, ''))}
          placeholder="Phone Number"
          className="border p-2 w-full mb-3 rounded"
          maxLength={10}
        />

        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          className="border p-2 w-full mb-4 rounded"
        />

        <button
          type="submit"
          className="w-full bg-red-500 text-white py-2 rounded hover:bg-pink-600"
        >
          Sign Up
        </button>

        <p className="text-center text-sm mt-4">
          Already have an account?{' '}
          <Link to="/login" className="text-red-500 underline">
            Log in
          </Link>
        </p>
      </form>
    </div>
  );
};

export default Signup;
