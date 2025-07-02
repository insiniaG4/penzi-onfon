import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass


@dataclass
class SMSCommand:
    """Represents a parsed SMS command"""
    command: str
    action: Optional[str] = None
    parameters: Dict[str, str] = None
    raw_message: str = ""
    sender_phone: str = ""
    
    def __post_init__(self):
        if self.parameters is None:
            self.parameters = {}


class SMSParser:
    """Parses incoming SMS messages into structured commands"""
    
    # Command patterns - case insensitive
    COMMAND_PATTERNS = {
        # Registration commands
        'REGISTER': r'^(REG|REGISTER)\s+(.+)$',
        'UPDATE': r'^(UPDATE|EDIT)\s+(.+)$',
        
        # Profile commands
        'PROFILE': r'^(PROFILE|PROF)\s*(\d+)?$',
        'SEARCH': r'^(SEARCH|FIND)\s+(.+)$',
        
        # Matching commands
        'MATCH': r'^(MATCH|M)\s*(\d+)?$',
        'ACCEPT': r'^(ACCEPT|YES|Y)\s+(\d+)$',
        'REJECT': r'^(REJECT|NO|N)\s+(\d+)$',
        
        # Messaging commands
        'MESSAGE': r'^(MSG|MESSAGE)\s+(\d+)\s+(.+)$',
        'REPLY': r'^(REPLY|R)\s+(\d+)\s+(.+)$',
        
        # General commands
        'HELP': r'^(HELP|H|\?)$',
        'STOP': r'^(STOP|QUIT|EXIT)$',
        'STATUS': r'^(STATUS|STAT)$',
        
        # Menu navigation
        'MENU': r'^(MENU|MAIN)$',
        'BACK': r'^(BACK|B)$',
    }
    
    # Registration field patterns
    REGISTRATION_PATTERNS = {
        'name': r'NAME[:\s]+([^,\n]+)',
        'age': r'AGE[:\s]+(\d+)',
        'gender': r'GENDER[:\s]+(M|F|MALE|FEMALE)',
        'county': r'COUNTY[:\s]+([^,\n]+)',
        'town': r'TOWN[:\s]+([^,\n]+)',
        'education': r'EDUCATION[:\s]+([^,\n]+)',
        'profession': r'PROFESSION[:\s]+([^,\n]+)',
        'religion': r'RELIGION[:\s]+([^,\n]+)',
        'marital': r'MARITAL[:\s]+([^,\n]+)',
    }
    
    # Search criteria patterns
    SEARCH_PATTERNS = {
        'age_range': r'AGE[:\s]+(\d+)-(\d+)',
        'gender': r'GENDER[:\s]+(M|F|MALE|FEMALE)',
        'county': r'COUNTY[:\s]+([^,\n]+)',
        'town': r'TOWN[:\s]+([^,\n]+)',
        'education': r'EDUCATION[:\s]+([^,\n]+)',
        'profession': r'PROFESSION[:\s]+([^,\n]+)',
        'religion': r'RELIGION[:\s]+([^,\n]+)',
    }
    
    @classmethod
    def parse_sms(cls, message: str, sender_phone: str = "") -> SMSCommand:
        """
        Parse an incoming SMS message into a structured command
        
        Args:
            message: The SMS message content
            sender_phone: Phone number of the sender
            
        Returns:
            SMSCommand object with parsed information
        """
        message = message.strip().upper()
        
        # Try to match against known command patterns
        for command_name, pattern in cls.COMMAND_PATTERNS.items():
            match = re.match(pattern, message, re.IGNORECASE | re.MULTILINE)
            if match:
                return cls._parse_command(command_name, match, message, sender_phone)
        
        # If no pattern matches, treat as unknown command
        return SMSCommand(
            command="UNKNOWN",
            raw_message=message,
            sender_phone=sender_phone,
            parameters={"error": "Unknown command format"}
        )
    
    @classmethod
    def _parse_command(cls, command: str, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse specific command based on matched pattern"""
        
        if command == "REGISTER":
            return cls._parse_registration(match, raw_message, sender_phone)
        elif command == "UPDATE":
            return cls._parse_update(match, raw_message, sender_phone)
        elif command == "SEARCH":
            return cls._parse_search(match, raw_message, sender_phone)
        elif command == "MESSAGE":
            return cls._parse_message(match, raw_message, sender_phone)
        elif command == "REPLY":
            return cls._parse_reply(match, raw_message, sender_phone)
        elif command in ["ACCEPT", "REJECT"]:
            return cls._parse_match_response(command, match, raw_message, sender_phone)
        elif command == "PROFILE":
            return cls._parse_profile(match, raw_message, sender_phone)
        elif command == "MATCH":
            return cls._parse_match_request(match, raw_message, sender_phone)
        else:
            # Simple commands without parameters
            return SMSCommand(
                command=command,
                raw_message=raw_message,
                sender_phone=sender_phone
            )
    
    @classmethod
    def _parse_registration(cls, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse registration command"""
        registration_data = match.group(2)
        parameters = {}
        
        # Extract registration fields
        for field, pattern in cls.REGISTRATION_PATTERNS.items():
            field_match = re.search(pattern, registration_data, re.IGNORECASE)
            if field_match:
                value = field_match.group(1).strip()
                if field == 'gender':
                    value = 'M' if value.upper() in ['M', 'MALE'] else 'F'
                elif field == 'age':
                    value = int(value)
                parameters[field] = value
        
        return SMSCommand(
            command="REGISTER",
            parameters=parameters,
            raw_message=raw_message,
            sender_phone=sender_phone
        )
    
    @classmethod
    def _parse_update(cls, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse update command - similar to registration but for updates"""
        update_data = match.group(2)
        parameters = {}
        
        # Extract update fields (same as registration)
        for field, pattern in cls.REGISTRATION_PATTERNS.items():
            field_match = re.search(pattern, update_data, re.IGNORECASE)
            if field_match:
                value = field_match.group(1).strip()
                if field == 'gender':
                    value = 'M' if value.upper() in ['M', 'MALE'] else 'F'
                elif field == 'age':
                    value = int(value)
                parameters[field] = value
        
        return SMSCommand(
            command="UPDATE",
            parameters=parameters,
            raw_message=raw_message,
            sender_phone=sender_phone
        )
    
    @classmethod
    def _parse_search(cls, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse search command"""
        search_criteria = match.group(2)
        parameters = {}
        
        # Extract search criteria
        for field, pattern in cls.SEARCH_PATTERNS.items():
            field_match = re.search(pattern, search_criteria, re.IGNORECASE)
            if field_match:
                if field == 'age_range':
                    parameters['min_age'] = int(field_match.group(1))
                    parameters['max_age'] = int(field_match.group(2))
                else:
                    value = field_match.group(1).strip()
                    if field == 'gender':
                        value = 'M' if value.upper() in ['M', 'MALE'] else 'F'
                    parameters[field] = value
        
        return SMSCommand(
            command="SEARCH",
            parameters=parameters,
            raw_message=raw_message,
            sender_phone=sender_phone
        )
    
    @classmethod
    def _parse_message(cls, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse message command"""
        recipient_id = match.group(2)
        message_text = match.group(3)
        
        return SMSCommand(
            command="MESSAGE",
            parameters={
                "recipient_id": int(recipient_id),
                "message_text": message_text
            },
            raw_message=raw_message,
            sender_phone=sender_phone
        )
    
    @classmethod
    def _parse_reply(cls, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse reply command"""
        message_id = match.group(2)
        reply_text = match.group(3)
        
        return SMSCommand(
            command="REPLY",
            parameters={
                "message_id": int(message_id),
                "reply_text": reply_text
            },
            raw_message=raw_message,
            sender_phone=sender_phone
        )
    
    @classmethod
    def _parse_match_response(cls, command: str, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse accept/reject match commands"""
        match_id = match.group(2)
        
        return SMSCommand(
            command=command,
            parameters={"match_id": int(match_id)},
            raw_message=raw_message,
            sender_phone=sender_phone
        )
    
    @classmethod
    def _parse_profile(cls, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse profile command"""
        user_id = match.group(2) if match.group(2) else None
        parameters = {}
        
        if user_id:
            parameters["user_id"] = int(user_id)
        
        return SMSCommand(
            command="PROFILE",
            parameters=parameters,
            raw_message=raw_message,
            sender_phone=sender_phone
        )
    
    @classmethod
    def _parse_match_request(cls, match: re.Match, raw_message: str, sender_phone: str) -> SMSCommand:
        """Parse match request command"""
        user_id = match.group(2) if match.group(2) else None
        parameters = {}
        
        if user_id:
            parameters["target_user_id"] = int(user_id)
        
        return SMSCommand(
            command="MATCH",
            parameters=parameters,
            raw_message=raw_message,
            sender_phone=sender_phone
        )
    
    @classmethod
    def get_help_text(cls) -> str:
        """Return help text for SMS commands"""
        return """
PENZI SMS COMMANDS:

REGISTRATION:
REG NAME:John AGE:25 GENDER:M COUNTY:Nairobi TOWN:Westlands

PROFILE:
PROFILE - View your profile
PROFILE 123 - View user 123's profile

SEARCH:
SEARCH AGE:20-30 GENDER:F COUNTY:Nairobi

MATCHING:
MATCH - Get new matches
MATCH 123 - Request match with user 123
ACCEPT 456 - Accept match 456
REJECT 456 - Reject match 456

MESSAGING:
MSG 123 Hello there!
REPLY 789 Thanks for the message

GENERAL:
HELP - Show this help
STATUS - Check your status
STOP - Unsubscribe
        """.strip()