import random
from typing import List
# import email_manager

class Participent:
    """
    Participent class:
    Define a participent in the secret santa game.
    """
    def __init__(self, name, email, DontPick = []):
        self.name = name
        self.email = email
        self.DontPick = []

    def __eq__(self, other):
        return self.name == other.name and self.email == other.email
    
    def __repr__(self) -> str:
        return f"Participent({self.name}, {self.email}, {[part.name for part in self.DontPick]})"

class SecretSantaGame:
    """
    Game instance takes participents and picks pairs.
    """
    def __init__(self, participents: List[Participent]):
        self.participents = participents
        self.pairs = [] # Pairs are tuples of (giver, receiver)

    def play_game(self) -> None:
        """
        Take participents and pick pairs.
        """
        # Make a copy of the participents list to draw from
        participents = self.participents[:]
        for participent in self.participents:
            # Pick a random participent from the list
            receiver = random.choice(participents)
            # If the receiver is the same as the giver or the giver is in the receivers DontPick list, pick again
            while receiver == participent or receiver in participent.DontPick:
                # Redraw case
                receiver = random.choice(participents)
            # Add participents receiver to the DontPick list for subsequent games if applicable
            participent.DontPick.append(receiver)
            # Add participent to receivers DontPick list 
            receiver.DontPick.append(participent)
            # Add the pair to the list of pairs
            self.pairs.append((participent, receiver))
            # Remove the receiver from the list of participents
            participents.remove(receiver)

    def dry_run(self):
        """
        Run a dry run and print results to the console instead of sending emails.
        """
        self.play_game()
        for pair in self.pairs:
            print(f"{pair[0].name} is giving to {pair[1].name}")

    def run(self):
        pass


if __name__ == "__main__":
    # Example usage

    # Create participents and add to list
    josh = Participent("Josh", "josh.nj.lawrence@gmail.com", ["julee"])
    julee = Participent("julee", "josh.nj.lawrence@gmail.com", ["josh"])
    mike = Participent("mike", "josh.nj.lawrence@gmail.com", ["leslee"])
    leslee = Participent("leslee", "josh.nj.lawrence@gmail.com", ["mike"])
    kyle = Participent("kyle", "josh.nj.lawrence@gmail.com", ["rylan"])
    rylan = Participent("rylan", "josh.nj.lawrence@gmail.com", ["kyle"])
    mitchell = Participent("mitchell", "josh.nj.lawrence@gmail.com", ["lorin", "emilia"])
    lorin = Participent("lorin", "josh.nj.lawrence@gmail.com", ["mitchell", "emilia"])
    emilia = Participent("emilia", "josh.nj.lawrence@gmail.com", ["lorin", "mitchell"])
    participents = [josh, julee, mike, leslee, kyle, rylan, mitchell, lorin, emilia]

    # Create game instance
    game = SecretSantaGame(participents)
    # Play game
    game.dry_run()
    # Print participent list after
    print(participents)

