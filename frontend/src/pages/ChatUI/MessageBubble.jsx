// MessageBubble.jsx
const MessageBubble = ({ msg, isTyping = false }) => {
  const bubbleStyle =
    msg?.type === 'user'
      ? 'bg-pink-100 text-gray-800 self-end ml-auto'
      : 'bg-gray-100 text-gray-800 self-start mr-auto';

  if (isTyping) {
    return (
      <div className="flex items-center space-x-2 self-start mr-auto px-3 py-2 rounded-xl bg-gray-100 max-w-[90%] animate-pulse text-sm text-gray-600">
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" />
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-150" />
        <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce delay-300" />
        <span>typing...</span>
      </div>
    );
  }

  return (
    <div className={`px-3 py-2 rounded-xl max-w-[90%] text-sm ${bubbleStyle}`}>
      {msg?.text}
    </div>
  );
};

export default MessageBubble;
