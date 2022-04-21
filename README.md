Small experiment using Pygame.

A reverse game of Snake, where you play as the food and try to escape the Snake.

Required: pygame, python3

To start: `python3 snake.py`

Controls: WASD

Score is awarded based on: `TICKS SURVIVED * (LENGTH OF SNAKE EACH TICK - 3)`. If you survive 30 ticks
with a snake of length 3, you get 30 score. 20 ticks with length 3 and 10 with length 4 is 40 score.

Being near the snake's head also doesn't award any score (shown with red outline in window)