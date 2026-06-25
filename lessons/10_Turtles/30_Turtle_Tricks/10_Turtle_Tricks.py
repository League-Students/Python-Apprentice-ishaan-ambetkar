import tkinter as tk
import random

class CakeStacker:
    def __init__(self, root):
        self.root = root
        self.root.title("Cake Stacker!")
        
        # Game Dimensions
        self.canvas_width = 400
        self.canvas_height = 600
        
        # Setup Canvas
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height, bg="#FFF0F5")
        self.canvas.pack()
        
        # Game Variables
        self.layer_height = 30
        self.score = 0
        self.game_over = False
        
        # Cake Colors (cycles through these frosting flavors)
        self.colors = ["#FF69B4", "#FFB6C1", "#BA55D3", "#87CEFA", "#48D1CC", "#FFD700", "#FFA07A"]
        
        # Bind Controls
        self.root.bind("<space>", self.drop_layer)
        
        self.reset_game()
        self.game_loop()

    def reset_game(self):
        self.canvas.delete("all")
        self.score = 0
        self.game_over = False
        
        # Draw a beautiful serving plate at the bottom
        self.plate_y = self.canvas_height - 40
        self.canvas.create_rectangle(50, self.plate_y, 350, self.plate_y + 15, fill="#E6E6FA", outline="#D8BFD8", width=3, tags="plate")
        
        # Track stack information: (left_x, right_x, target_y)
        # The base target is the plate area (from x=50 to x=350)
        self.stack = [(50, 350, self.plate_y)]
        
        # Spawn the very first moving cake tier
        self.spawn_new_layer()
        
        # Draw score display
        self.score_text = self.canvas.create_text(200, 30, text=f"Layers: {self.score}", font=("Arial", 20, "bold"), fill="#C71585")

    def spawn_new_layer(self):
        # Calculate height for the new layer based on how many layers are already stacked
        current_tier_index = len(self.stack) - 1
        self.current_y = self.plate_y - (current_tier_index * self.layer_height) - self.layer_height
        
        # If the cake reaches near the top, shift everything down to keep it on screen
        if self.current_y < 150:
            self.shift_stack_down()
            self.current_y = self.plate_y - (current_tier_index * self.layer_height) - self.layer_height

        # Determine the maximum allowed width from the previous layer's size
        prev_left, prev_right, _ = self.stack[-1]
        self.layer_width = prev_right - prev_left
        
        # Movement configurations
        self.layer_speed = random.choice([4, 5, 6]) + min(self.score // 3, 5) # Speeds up as score increases
        self.direction = 1 # 1 = right, -1 = left
        
        # Spawn coordinates
        self.current_x = 0
        color = self.colors[self.score % len(self.colors)]
        
        # Render the moving layer
        self.active_layer = self.canvas.create_rectangle(
            self.current_x, self.current_y, 
            self.current_x + self.layer_width, self.current_y + self.layer_height, 
            fill=color, outline="#FFFFFF", width=2
        )

    def game_loop(self):
        if not self.game_over:
            # Move the active layer back and forth
            self.current_x += self.layer_speed * self.direction
            
            # Bounce off the walls
            if self.current_x + self.layer_width >= self.canvas_width:
                self.direction = -1
            elif self.current_x <= 0:
                self.direction = 1
                
            # Update canvas coordinates
            self.canvas.coords(
                self.active_layer, 
                self.current_x, self.current_y, 
                self.current_x + self.layer_width, self.current_y + self.layer_height
            )
            
            # Call loop again after 16 milliseconds (~60 FPS)
            self.root.after(16, self.game_loop)

    def drop_layer(self, event):
        if self.game_over:
            self.reset_game()
            self.game_loop()
            return

        # Get coordinates of the underlying layer to check alignment
        prev_left, prev_right, _ = self.stack[-1]
        curr_left = self.current_x
        curr_right = self.current_x + self.layer_width
        
        # Calculate overlapping boundaries
        new_left = max(prev_left, curr_left)
        new_right = min(prev_right, curr_right)
        
        if new_left < new_right:
            # Succesfully stacked! Update the layer visual to match trimmed size perfectly
            self.canvas.coords(self.active_layer, new_left, self.current_y, new_right, self.current_y + self.layer_height)
            
            # Save to stack data and update stats
            self.stack.append((new_left, new_right, self.current_y))
            self.score += 1
            self.canvas.itemconfig(self.score_text, text=f"Layers: {self.score}")
            
            # Move to next tier
            self.spawn_new_layer()
        else:
            # Missed the underlying layer completely
            self.trigger_game_over()

    def shift_stack_down(self):
        # Shift every graphical asset on screen down by 3 positions
        shift_amount = self.layer_height * 3
        self.canvas.move("all", 0, shift_amount)
        
        # Keep score text statically locked at the top
        self.canvas.move(self.score_text, 0, -shift_amount)
        
        # Re-calculate absolute logical coordinates for our background stack data
        for i in range(len(self.stack)):
            l, r, y = self.stack[i]
            self.stack[i] = (l, r, y + shift_amount)
            
    def trigger_game_over(self):
        self.game_over = True
        self.canvas.create_text(200, 250, text="GAME OVER", font=("Arial", 30, "bold"), fill="#FF0000")
        self.canvas.create_text(200, 300, text="Press Spacebar to Bake Again", font=("Arial", 14), fill="#555555")

# Run Game Window
if __name__ == "__main__":
    window = tk.Tk()
    game = CakeStacker(window)
    window.mainloop()