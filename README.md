# Simple Game - Snake

Snake game made on python with pygame. It has 4 main classes including Game class.

1. Snake class creates main snake objects. It moves each frame by default to the right, can change direction based on user's input and grows after eating Food object. Snake class consists of:

  - control() method which controls direction of a snake
  - check_borders() method which checks borders to move position of a snake accordingly
  - check_self_eating() method which checks if snake eats itself
  - check_food() method which checks if snakes position is equal to foods position
  - move() method which moves snake each frame
  - draw() method which draws each segment of a snake depending on snake's length

2. Food class creates food object. Changes position after getting eaten by a Snake objects consists of:

  - draw() method which draws food on a random position

3. Game class consists of:

  -  run() method which runs classic while loop with: input handler, update and draw methods
  -  new_game() method which restarts game with all other objects

4. Menu class creates menu screen. It is just a simple game over screen with 2 strings on it and score number. Menu class consists of:
  
  - draw_score() method draws last result score after game over
  - draw() method which draws menu

This is my first experience in creating game with OOP structure so please don't judge to much)
Enjoy!
