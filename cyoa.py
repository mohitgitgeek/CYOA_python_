from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
from sklearn.ensemble import RandomForestClassifier
import json
import os
import random

app = Flask(__name__)
CORS(app)

# Expanded story data structure
STORY_DATA = {
    "start": {
        "text": "You are in a dark forest. There are three paths in front of you.",
        "choices": {
            "1": {
                "text": "Take the misty left path",
                "next": "left_path"
            },
            "2": {
                "text": "Take the middle path with strange mushrooms",
                "next": "mushroom_path"
            },
            "3": {
                "text": "Take the right path with ancient ruins",
                "next": "right_path"
            }
        }
    },
    "left_path": {
        "text": "You encounter a friendly elf who offers you a choice of gifts.",
        "choices": {
            "1": {
                "text": "Accept the mysterious glowing sword",
                "next": "sword_choice"
            },
            "2": {
                "text": "Accept the ancient spellbook",
                "next": "spellbook_choice"
            },
            "3": {
                "text": "Politely decline",
                "next": "elf_gift_decline"
            }
        }
    },
    "sword_choice": {
        "text": "The elf hands you the sword. As you grasp it...",
        "choices": {
            "1": {
                "text": "Swing it to test its power",
                "next": "sword_test"
            },
            "2": {
                "text": "Thank the elf and continue your journey",
                "next": "sword_journey"
            }
        }
    },
    "sword_test": {
        "text": "The sword unleashes a powerful beam of light, revealing a hidden dragon's lair filled with treasure. You've discovered a legendary artifact! You win gloriously!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "sword_journey": {
        "text": "As you travel, you encounter a village under attack by bandits. Your magical sword helps you defend the villagers, who reward you handsomely. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "spellbook_choice": {
        "text": "The spellbook glows with ancient power. You...",
        "choices": {
            "1": {
                "text": "Try to cast a simple spell",
                "next": "spell_attempt"
            },
            "2": {
                "text": "Study it carefully first",
                "next": "spell_study"
            }
        }
    },
    "spell_attempt": {
        "text": "Your hasty spell backfires, turning you into a frog. The elf laughs and says the transformation will wear off... eventually. You lose!",
        "choices": {},
        "is_ending": True,
        "outcome": "lose"
    },
    "spell_study": {
        "text": "Your careful study reveals powerful protection spells. You become a renowned magic user in the realm. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "mushroom_path": {
        "text": "The glowing mushrooms seem to whisper ancient secrets. You notice...",
        "choices": {
            "1": {
                "text": "A fairy ring of mushrooms",
                "next": "fairy_ring"
            },
            "2": {
                "text": "A trail of mushrooms leading deeper into the forest",
                "next": "mushroom_trail"
            },
            "3": {
                "text": "Pick some mushrooms to eat",
                "next": "eat_mushrooms"
            }
        }
    },
    "fairy_ring": {
        "text": "The fairies invite you to dance. You...",
        "choices": {
            "1": {
                "text": "Join their dance",
                "next": "fairy_dance"
            },
            "2": {
                "text": "Politely watch from outside the ring",
                "next": "fairy_watch"
            }
        }
    },
    "fairy_dance": {
        "text": "You dance with the fairies and they grant you the ability to speak with animals. Your new power leads you to countless adventures! You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "fairy_watch": {
        "text": "The fairies appreciate your respectful distance and gift you with a magical compass that always points to adventure. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "mushroom_trail": {
        "text": "Following the trail, you discover...",
        "choices": {
            "1": {
                "text": "A wizard's hidden cottage",
                "next": "wizard_cottage"
            },
            "2": {
                "text": "An underground gnome city",
                "next": "gnome_city"
            }
        }
    },
    "wizard_cottage": {
        "text": "The wizard takes you as an apprentice, teaching you the mysteries of the forest. You become a powerful forest sage. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "gnome_city": {
        "text": "The gnomes share their ancient mining secrets with you. You discover a new type of crystal that revolutionizes magic in the realm. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "eat_mushrooms": {
        "text": "The mushrooms were not meant for human consumption. You have vivid hallucinations and wake up three days later. You lose!",
        "choices": {},
        "is_ending": True,
        "outcome": "lose"
    },
    "right_path": {
        "text": "Among the ancient ruins, you find a mysterious temple.",
        "choices": {
            "1": {
                "text": "Explore the temple's main chamber",
                "next": "temple_main"
            },
            "2": {
                "text": "Search for secret passages",
                "next": "temple_secret"
            },
            "3": {
                "text": "Examine the temple's inscriptions",
                "next": "temple_inscription"
            }
        }
    },
    "temple_main": {
        "text": "In the main chamber, you find an ancient artifact.",
        "choices": {
            "1": {
                "text": "Take the artifact",
                "next": "take_artifact"
            },
            "2": {
                "text": "Leave it on its pedestal",
                "next": "leave_artifact"
            }
        }
    },
    "take_artifact": {
        "text": "The temple begins to collapse! You barely escape with the artifact, but it grants you great power. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "leave_artifact": {
        "text": "Your respect for ancient treasures impresses the temple's guardian spirit. You become the temple's chosen protector. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "temple_secret": {
        "text": "You discover a hidden passage leading to...",
        "choices": {
            "1": {
                "text": "An ancient library",
                "next": "ancient_library"
            },
            "2": {
                "text": "A treasure vault",
                "next": "treasure_vault"
            }
        }
    },
    "ancient_library": {
        "text": "The library contains scrolls of forgotten knowledge. You become a renowned scholar and adventurer. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "treasure_vault": {
        "text": "The vault triggers a trap! You're teleported outside the temple with nothing to show for your efforts. You lose!",
        "choices": {},
        "is_ending": True,
        "outcome": "lose"
    },
    "temple_inscription": {
        "text": "The inscriptions tell of a hidden power within the temple.",
        "choices": {
            "1": {
                "text": "Perform the ritual described",
                "next": "perform_ritual"
            },
            "2": {
                "text": "Copy the inscriptions for later study",
                "next": "copy_inscriptions"
            }
        }
    },
    "perform_ritual": {
        "text": "The ritual summons an ancient spirit who grants you mystical powers. You win!",
        "choices": {},
        "is_ending": True,
        "outcome": "win"
    },
    "copy_inscriptions": {
        "text": "While copying the inscriptions, you accidentally trigger a curse. You lose!",
        "choices": {},
        "is_ending": True,
        "outcome": "lose"
    },
    "elf_gift_decline": {
        "text": "The elf is offended and casts a spell on you. You spend the next year speaking in rhymes. You lose!",
        "choices": {},
        "is_ending": True,
        "outcome": "lose"
    }
}

# Initialize ML model
class GameML:
    def __init__(self):
        self.model = RandomForestClassifier(n_estimators=100)
        self.choices_history = []
        self.outcomes_history = []
        self.is_trained = False

    def record_choice(self, state, choice, outcome=None):
        # Convert state and choice to numerical features
        features = [hash(state) % 100, int(choice)]
        self.choices_history.append(features)
        if outcome:
            self.outcomes_history.append(1 if outcome == "win" else 0)

    def train(self):
        if len(self.choices_history) > 5:  # Only train if we have enough data
            X = np.array(self.choices_history)
            y = np.array(self.outcomes_history)
            self.model.fit(X, y)
            self.is_trained = True

    def predict_best_choice(self, state):
        if not self.is_trained:
            return None
        
        # Evaluate all choices for the current state
        choices = STORY_DATA[state]['choices'].keys()
        scores = []
        for choice in choices:
            score = self.model.predict_proba([[hash(state) % 100, int(choice)]])[0][1]
            scores.append((choice, score))
        
        # Return the choice with highest score
        return max(scores, key=lambda x: x[1])[0] if scores else None

# Initialize game state
game_ml = GameML()

@app.route('/api/game/state', methods=['GET'])
def get_state():
    state = request.args.get('state', 'start')
    current_state_data = STORY_DATA[state]
    
    # Get ML recommendation if available
    recommendation = None
    if current_state_data['choices'] and game_ml.is_trained:
        recommendation = game_ml.predict_best_choice(state)
    
    return jsonify({
        'state': state,
        'stateData': current_state_data,
        'recommendation': recommendation
    })

@app.route('/api/game/choice', methods=['POST'])
def make_choice():
    data = request.json
    current_state = data['state']
    choice = data['choice']
    
    state_data = STORY_DATA[current_state]
    next_state = state_data['choices'][choice]['next']
    next_state_data = STORY_DATA[next_state]
    
    # Record choice for ML
    if 'is_ending' in next_state_data:
        game_ml.record_choice(current_state, choice, next_state_data['outcome'])
        game_ml.train()
    else:
        game_ml.record_choice(current_state, choice)
    
    return jsonify({
        'state': next_state,
        'stateData': next_state_data
    })

if __name__ == '__main__':
    app.run(debug=True)
