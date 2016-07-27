"""
Programming task
================

The following is an implementation of a simple Named Entity Recognition (NER).
NER is concerned with identifying place names, people names or other special
identifiers in text.

Here we make a very simple definition of a named entity: A sequence of
at least two consecutive capitalized words. E.g. "Los Angeles" is a named
entity, "our hotel" is not.

While the implementation passes the Unit test, it suffers from bad structure and
readability. It is your task to rework *both* the implementation and the Unit
test. You are expected to come up with a better interface than the one presented
here.

Your code will be evaluated on:
- Readability: Is naming intuitive? Are there comments where necessary?
- Structure: Is functionality grouped into functions or classes in a way that
enables reusability?
- Testability: Is it easy to test individual components of your algorithm? This
is a good indicator of good interface design.
- Bonus: Functional programming. Demonstrate how you have applied principles of
functional programming to improve this code.

If you want, explain reasons for changes you've made in comments.

Note that you don't have to improve the actual Named Entity Recognition
algorithm itself - the focus is on code quality.
"""

import re
import unittest

"""
NamedEntityRecognizer is responsible for recognizing all the entities in a text
"""


class NamedEntityRecognizer:
    # Regular expression for matching a token at the beginning of a sentence
    FIRST_SENT_TOKEN_RE = re.compile(r"([a-z]+)\s*(.*)$", re.I)

    # Regular expression to recognize an uppercase token
    CAPITALIZED_TOKEN_RE = re.compile(r"[A-Z][a-z]*$")

    def __init__(self, text):
        # Buffer to store current named entity
        self.named_entity_buffer = []
        # keeps track of the text to be processed
        self.remaining_text = text

    def update_buffer(self, entity_token):
        """
        Updates named entity buffer if its a capitalized word
        """
        if self.CAPITALIZED_TOKEN_RE.match(entity_token):
            self.named_entity_buffer.append(entity_token)
        else:
            self.named_entity_buffer = []

    def chop_token_to_buffer(self):
        """
        Take the first token off the beginning of text. If its first letter is
        capitalized, remember it in word buffer - we may have a named entity on our
        hands!!

        @return: token, token is None in case text is empty
        """

        entity_match = self.FIRST_SENT_TOKEN_RE.match(self.remaining_text)
        entity_token = None

        if entity_match:
            entity_token = entity_match.group(1)
            self.remaining_text = entity_match.group(2)
            self.update_buffer(entity_token)
        return True if entity_token else False


    def consume_namedentity_buffer(self):
        """
        Return a named entity, if we have assembled one in the current buffer.
        Returns None if we have to keep searching.

        @return named entity string if buffer has enough tokens otherwise None
        """
        if len(self.named_entity_buffer) >= 2:
            named_entity = " ".join(self.named_entity_buffer)
            # Clears buffer after finding named entity
            self.named_entity_buffer = []
            return named_entity
        else:
            return None

    def get_named_entities(self):
        """
        Returns set of  named entities in a text
        @return set
        """
        entities = set()

        while self.chop_token_to_buffer():
            entity = self.consume_namedentity_buffer()
            if entity:
                entities.add(entity)

        return entities


class NamedEntityTestCase(unittest.TestCase):
    def test_ner_extraction(self):
        # Remember to change this Unit test as well to follow the interface
        # changes you propose above

        text = "When we went to Los Angeles last year we visited the Hollywood Sign"

        ner = NamedEntityRecognizer(text)
        entities = ner.get_named_entities()

        self.assertEqual(set(["Los Angeles", "Hollywood Sign"]), entities)


if __name__ == "__main__":
    unittest.main()