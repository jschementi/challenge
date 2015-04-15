# Coding Challenge - Child Rummy

Child Rummy is a simple variation of [Rummy](http://en.wikipedia.org/wiki/Rummy):

- Each player is dealt 7 cards from a 52 card deck (no jokers)
- A player wins by being the first to have both a 
  3-of-a-kind (same card value, different suits) and a 4-card-run (same suit,
  incrementing card value) in their hand, where the cards used for each goal are
  mutually exclusive.
- After dealing, the remaining cards are stacked face-down (called
  the stack), and the top card on the stack is turned face-up next to the stack,
  (beginning the discard pile).
- Play is round robin, with each player's turn consists of picking a card from
  either the top of the stack or the top of the discard pile, adding the card
  to their hand, and then discarding to the top of the discard pile.
- A player can only declare they win during their turn, and must still discard
  at the end of their turn and still have a winning hand.
- If the stack is empty immediately after a player picks a card, before the 
  player can discard the discard pile is shuffled and becomes the stack.

Pick **at least two** of the challenges below (you can do more!). You can
decide to keep each individual challenge's implementation separate or
integrated. Be creative!

We only expect you to spend a maximum of 4 hours, both to respect your time
and to limit the scope of this assignment.

To submit, simply push your changes to this GitHub repository (please take care
to not push or share it publicly). Also, for each challenge you decide to do,
add any comments you'd like to make to `README.md`. It can include design
decisions, challenges you had, usage instructions, how to run tests, etc.

If you have any problems, please contact us.


## 1. Game Mechanics

Implement Child Rummy with a very-simple (text-based or something else comparable)
user-interface in whatever programming language you'd like, though we suggest
either JavaScript, Python, Objective-C, or Swift. At least one player
should be a human player, and the rest can be very simple bots (take a random
card, discard a random card).

## 2. Goal Detection

Given a player's hand, implement an algorithm to detect if a hand is a winning
hand or not.

For example, the following is a winning hand because there exists a 3-of-kind
and a 4-card-run:

```
A♥ A♠ A♣ 2♦ 3♦ 4♦ 5♦
```

While the following are interesting examples of non-winning hands:

- 4-card-run and 3-of-a-kind exists independently, but not when considered
  together (cards cannot be shared):

  ```
  A♥ A♦ A♣ 2♣ 3♣ 4♣ 8♣
  ```

- Not a 4-card-run, as all cards must be the same suit:

  ```
  A♥ A♣ A♦ 3♣ 4♦ 5♣ 6♥
  ```

## 3. User Interface

Implement a user-interface for Child Rummy, including the actions which
manipulate the user-interface, like dealing, picking a card, discarding,
and winning. It can be in whatever technology you'd like, though we suggest either
HTML/CSS/JavaScript or iOS.

## 4. Smart Bots

Implement the logic for a bot which attempts to win the game. 

