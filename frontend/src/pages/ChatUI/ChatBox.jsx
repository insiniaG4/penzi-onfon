import React, { useState, useRef, useEffect } from 'react';
import ChatHeader from './ChatHeader';
import MessageBubble from './MessageBubble';
import InputBox from './InputBox';
import { registerUser } from '../../utils/api';

const ChatBox = () => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [hasWelcomed, setHasWelcomed] = useState(false);
  const [step, setStep] = useState('welcome');
  const [isTyping, setIsTyping] = useState(false);
  const [userData, setUserData] = useState({});
  const [matches, setMatches] = useState([]);
  const [matchIndex, setMatchIndex] = useState(0);
  const messagesEndRef = useRef(null);

  const educationLevels = ['Primary', 'Secondary', 'Diploma', 'Graduate', 'Masters'];
  const maritalStatuses = ['Single', 'Married', 'Divorced', 'Widowed'];
  const religions = ['Christian', 'Muslim', 'Hindu', 'Other'];
  const ethnicities = ['Luo', 'Kikuyu', 'Kalenjin', 'Kamba', 'Somali', 'Mijikenda', 'Other'];
  const validGenders = ['male', 'female'];

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isTyping]);

  const handleSend = (e) => {
    e?.preventDefault();
    if (!input.trim()) return;

    const cleanInput = input.trim().toLowerCase();
    const userMessage = { type: 'user', text: input };
    setMessages((prev) => [...prev, userMessage]);
    setInput('');
    setIsTyping(true);

    setTimeout(async () => {
      try {
        let reply = '';

        if (!hasWelcomed) {
          reply = 'Welcome to PENZI - Kenya\'s #1 Dating Platform with 6000 potential dating partners!\n\nType: start#name#age#gender#county#town#phone\nExample: start#Mary#24#female#Nairobi#CBD#0712345678';
          setHasWelcomed(true);
          setStep('basic');
        } else if (cleanInput === 'help') {
          reply = 'PENZI HELP MENU:\nstart#name#age#gender#county#town#phone\ndetails#levelOfEducation#profession#maritalStatus#religion#ethnicity\nMYSELF I am...\nmatch#ageRange#town\nDESCRIBE phone_number\nNEXT\nYES';
        } else if (cleanInput.startsWith('start#') && step === 'basic') {
          const parts = input.split('#');
          console.log('Input parts:', parts);
          if (parts.length === 7) {
            const [_, username, ageStr, gender, county, town, phone_number] = parts;
            const age = parseInt(ageStr);
            console.log('Parsed age, gender:', age, gender);
            if (isNaN(age) || age < 18 || age > 80) {
              reply = 'Age must be between 18 and 80.';
            } else if (!validGenders.includes(gender.toLowerCase())) {
              reply = 'Gender must be "male" or "female".';
            } else if (!/^\d{10}$/.test(phone_number)) {
              reply = 'Phone number must be exactly 10 digits.';
            } else {
              const newUserData = { username, age, gender, county, town, phone_number, registration_status: 'Pending' };
              setUserData(newUserData);
              console.log('Sending to DB (POST /users/):', JSON.stringify(newUserData));
              const userRes = await fetch('http://127.0.0.1:5000/users/', {
                method: 'POST',
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json'
                },
                body: JSON.stringify(newUserData)
              });
              if (!userRes.ok) {
                throw new Error(`HTTP error! Status: ${userRes.status}`);
              }
              const userResData = await userRes.json();
              console.log('DB Response (POST /users/):', userResData);
              
              setUserData((prev) => ({ ...prev, user_id: userResData.data.user_id }));
              reply = `Hello ${username}! Your info is saved.\nNow type: details#levelOfEducation#profession#maritalStatus#religion#ethnicity\nExample: details#Graduate#Accountant#Divorced#Muslim#Somali`;
              setStep('details');
            }
          } else {
            reply = 'Format: start#name#age#gender#county#town#phone';
          }
        } else if (cleanInput.startsWith('details#') && step === 'details') {
          const parts = input.split('#');
          console.log('Details input parts:', parts);
          if (parts.length === 6) {
            const [_, education, profession, maritalStatus, religion, ethnicity] = parts;
            if (!educationLevels.includes(education)) {
              reply = `Education must be one of: ${educationLevels.join(', ')}`;
            } else if (!maritalStatuses.includes(maritalStatus)) {
              reply = `Marital status must be one of: ${maritalStatuses.join(', ')}`;
            } else if (!religions.includes(religion)) {
              reply = `Religion must be one of: ${religions.join(', ')}`;
            } else if (!ethnicities.includes(ethnicity)) {
              reply = `Ethnicity must be one of: ${ethnicities.join(', ')}`;
            } else {
              const updatedUserData = {
                ...userData,
                education_level: education, 
                profession,
                marital_status: maritalStatus,
                religion,
                ethnicity,
                registration_status: 'Pending'
              };
              setUserData(updatedUserData);
              console.log('Sending to DB (PUT /users/):', JSON.stringify(updatedUserData));
              const updateRes = await fetch(`http://127.0.0.1:5000/users/${userData.user_id}`, {
                method: 'PUT',
                headers: {
                  'Content-Type': 'application/json',
                  'Accept': 'application/json'
                },
                body: JSON.stringify(updatedUserData)
              });
              if (!updateRes.ok) {
                throw new Error(`HTTP error! Status: ${updateRes.status}`);
              }
              const updateResData = await updateRes.json();
              console.log('DB Response (PUT /users/):', updateResData);
              reply = `You were registered for dating with your initial details.\nThis is the last stage of registration.\nSMS a brief description of yourself starting with the word MYSELF.\nExample: MYSELF tall, dark and handsome`;
              setStep('description');
            }
          } else {
            reply = 'Format: details#levelOfEducation#profession#maritalStatus#religion#ethnicity';
          }
        } else if (cleanInput.startsWith('myself') && step === 'description') {
          const desc = input.slice(6).trim();
          if (desc) {
            const fullUserData = {
              ...userData,
              self_description: desc,
              registration_status: 'Complete'
            };
            setUserData(fullUserData);
            console.log('Sending to DB (PUT /users/):', JSON.stringify(fullUserData));
            const updateRes = await fetch(`http://127.0.0.1:5000/users/${userData.user_id}`, {
              method: 'PUT',
              headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/json'
              },
              body: JSON.stringify(fullUserData)
            });
            if (!updateRes.ok) {
              throw new Error(`HTTP error! Status: ${updateRes.status}`);
              }
              const updateResData = await updateRes.json();
              console.log('DB Response (PUT /users/):', updateResData);
              reply = `You are now registered for dating.\nTo search for a MPENZI, SMS match#ageRange#town to find matches.\nExample: match#23-25#Kisumu`;
              setStep('match');
            } else {
              reply = 'Please describe yourself using: MYSELF I am...';
            } }else if (cleanInput.startsWith('match#') && step === 'match') {
               const parts = input.split('#');
                  console.log('Match input parts:', parts);
                  if (parts.length === 3) {
               const [_, ageRange, town] = parts;
                    const [minAge, maxAge] = ageRange.split('-').map(Number);
                    if (isNaN(minAge) || isNaN(maxAge) || minAge >= maxAge || minAge < 18 || maxAge > 80) {
                      reply = 'Age range must be valid (e.g., 23-25) and between 18-80.';
              } else {
                     const matchCriteria = {
                  age_min: minAge,
                  age_max: maxAge,
                  town,
                  gender: userData.gender === 'male' ? 'female' : 'male'
             };
              console.log('Sending to DB (GET /matches):', JSON.stringify(matchCriteria));
              const matchRes = await fetch(
             `http://127.0.0.1:5000/matches/?age_min=${minAge}&age_max=${maxAge}&town=${town}&gender=${matchCriteria.gender}`,
             { headers: { 'Accept': 'application/json' } }
               );
              if (!matchRes.ok) throw new Error(`HTTP error! Status: ${matchRes.status}`);
         const matchesData = await matchRes.json();
            console.log('DB Response (GET /matches):', matchesData);
            setMatches(matchesData.data || matchesData);
              setMatchIndex(0);

              if ((matchesData.data?.length || matchesData.length) > 0) {
        const matchesArray = matchesData.data || matchesData;
        const batch = matchesArray.slice(0, 3);
        const matchDescriptions = batch.map(match =>
          `${match.username} aged ${match.age}, ${match.phone_number}.`
        ).join('\n');
        reply = `We have ${matchesArray.length} ${userData.gender === 'male' ? 'ladies' : 'gentlemen'} who match your choice! We will send you details of ${Math.min(3, matchesArray.length)} of them:\n${matchDescriptions}\n\nTo know more about any of them, type: DESCRIBE <phone_number>\nTo see more matches, type: NEXT`;
      } else {
        reply = 'No matches found. Try a different age range or town.';
      }
    }
  } else {
    reply = 'Format: match#ageRange#town';
  }

} else if (cleanInput === 'next' && step === 'match' && matches.length > matchIndex + 3) {
  const batch = matches.slice(matchIndex + 3, matchIndex + 6);
  setMatchIndex(prev => prev + 3);
  const matchDescriptions = batch.map(match =>
    `${match.username} aged ${match.age}, ${match.phone_number}.`
  ).join('\n');
  reply = `${matchDescriptions}\n\nTo see more matches, type: NEXT\nTo get details of any person, type: DESCRIBE <phone_number>`;

} else if (cleanInput.startsWith('describe ') && step === 'match') {
  const phone_number = input.split(' ')[1];
  console.log('Fetching details for phone:', phone_number);
  const matchRes = await fetch(`http://127.0.0.1:5000/users/phone/${phone_number}`, {
    headers: { 'Accept': 'application/json' }
  });
  if (!matchRes.ok) throw new Error(`HTTP error! Status: ${matchRes.status}`);
  const match = await matchRes.json();
  console.log('DB Response (GET /users/phone/):', match);

  if (!match || !match.data?.phone_number) {
    reply = 'Sorry, no match found with that phone number. Please check the number and try again.';
  } else {
    const matchData = match.data;
    const details = `${matchData.username} aged ${matchData.age}, ${matchData.county} County, ${matchData.town} town, ${matchData.education_level}, ${matchData.profession}, ${matchData.marital_status}, ${matchData.religion}, ${matchData.ethnicity}.`;
    reply = `${details}\n${matchData.self_description ? `${matchData.username} describes themselves as ${matchData.self_description}.` : 'No description available.'}`;

    // Notify logic
    const notifyData = {
      requester: userData,
      requested: matchData
    };
    console.log('Sending to DB (POST /notify):', JSON.stringify(notifyData));
    const notifyRes = await fetch('http://127.0.0.1:5000/users/notify', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify(notifyData)
    });
    if (!notifyRes.ok) throw new Error(`HTTP error! Status: ${notifyRes.status}`);
    const notifyResData = await notifyRes.json();
    console.log('DB Response (POST /notify):', notifyResData);

   const messageToUser2 = `Hi ${matchData.username}, a ${userData.gender} called ${userData.username} is interested in you and requested your details. They are aged ${userData.age} based in ${userData.town}. Do you want to know more about them? Type YES`;
    console.log(`message to user2: "${messageToUser2}"`);

  }

} else if (cleanInput === 'yes' && step === 'match') {
  console.log('Fetching requester for user:', userData.phone_number);
  const requesterRes = await fetch(`http://127.0.0.1:5000/requester/${userData.phone_number}`, {
    headers: { 'Accept': 'application/json' }
  });
  if (!requesterRes.ok) throw new Error(`HTTP error! Status: ${requesterRes.status}`);
  const requester = await requesterRes.json();
  console.log('DB Response (GET /requester/):', requester);

  if (requester && requester.data?.phone_number) {
    const r = requester.data;
    reply = `${r.username} aged ${r.age}, ${r.county} County, ${r.town} town, ${r.education_level}, ${r.profession}, ${r.marital_status}, ${r.religion}, ${r.ethnicity}.\n${r.self_description ? `${r.username} describes themselves as ${r.self_description}.` : 'No description available.'}\nSend DESCRIBE ${r.phone_number} to get more details about ${r.username}.`;
  } else {
    reply = 'No requester details available.';
  }
}




          
        setMessages((prev) => [...prev, { type: 'system', text: reply }]);
      } catch (err) {
        console.error('Error in handleSend:', err.message, err.stack);
        setMessages((prev) => [
          ...prev,
          { type: 'system', text: `Error: ${err.message}. Please try again or contact support.` }
        ]);
      } finally {
        setIsTyping(false);
      }
    }, 1000);
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100 px-4 py-6">
      <div className="max-w-md w-full bg-white rounded-2xl shadow-xl border overflow-hidden">
        <ChatHeader />
        <div className="h-96 p-4 overflow-y-auto">
          <div className="space-y-2">
            {messages.map((msg, idx) => (
              <MessageBubble key={idx} msg={msg} />
            ))}
            {isTyping && <MessageBubble isTyping={true} />}
            <div ref={messagesEndRef} />
          </div>
        </div>
        <InputBox input={input} setInput={setInput} handleSend={handleSend} step={step} />
      </div>
    </div>
  );
};

export default ChatBox;