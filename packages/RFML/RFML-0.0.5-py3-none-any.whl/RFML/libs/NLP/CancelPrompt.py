import re


# rf.nlp.prompt.is_cancel_text(_input)

class CancelPrompt:
    def is_cancel_text(text, patterns):
        """
        Check if the input text matches any 'cancel request' variations.

        Args:
            text (str): The input string to check.
            patterns (list): A list of regex patterns to match against the text.

        Returns:
            bool: True if a match is found, False otherwise.
            str: The first matching pattern (for debugging/analysis purposes).
        """
        for pattern in patterns:
            if re.search(pattern, text):
                return True, pattern
        return False, None

    # List of regex patterns for "cancel request" variations
    cancel_request_patterns = [
        r"(?i)\bplease\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bi would like to\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bkindly\b.*\bcancel(ing)?\b.*\brequest\b",
        r"(?i)\bcould you\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bcancel\b.*\brequest\b.*\bsubmitted\b.*\bearlier\b",
        r"(?i)\bcan you\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bdrop\b.*\bmy request\b",
        r"(?i)\bjust\b.*\bcancel\b.*\bit\b",
        r"(?i)\bforget\b.*\babout\b.*\bmy request\b",
        r"(?i)\bcancel\b.*\brequest\b",
        r"(?i)\bstop\b.*\brequest\b",
        r"(?i)\babort\b",
        r"(?i)\bdrop\b.*\bit\b",
        r"(?i)\bi apologize\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bnot too late\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bmay i ask\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bappreciate\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bsorry\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bi don(?:'|’)?t need\b.*\brequest\b.*\bcancel\b",
        r"(?i)\b(?:isn'?t|is not)\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bchanged my mind\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bunhappy\b.*\bcancel\b.*\brequest\b",
        r"(?i)\bno longer need\b.*\bcancel\b.*\bit\b",
        r"(?i)\bcancel\b.*\bbooking\b.*\brequest\b",
        r"(?i)\bcancel\b.*\bservice\b.*\brequest\b",
        r"(?i)\bcancel\b.*\border\b.*\bplaced earlier\b",
        r"(?i)\bcancel\b.*\bticket\b.*\brequest\b",
        r"(?i)\bstop processing\b.*\brefund\b.*\brequest\b"
    ]

    # Example usage
    test_text = "Could you please cancel my booking request?"

    is_match, matched_pattern = is_cancel_text(test_text, cancel_request_patterns)

    if is_match:
        print(f"Match found! Pattern: {matched_pattern}")
    else:
        print("No match found.")
