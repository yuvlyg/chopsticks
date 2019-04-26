
from flask import Flask, request, render_template
import hit
import random

hit_game = None

def init_game():
    global hit_game
    hit_game = hit.Game()
    hit_game.calculate_labels()
    
app = Flask(__name__)

@app.route('/', methods=['GET'])
def main():
    if u'v0' not in request.args:
        return render_template('h.html', v=[1] * 4, checked=["", "", "checked"])
    v = [int(request.args[u'v%d' % i]) for i in range(4)]
    level = int(request.args[u'level'])
    h1 = hit.rep_hand((v[0], v[1]))
    h2 = hit.rep_hand((v[2], v[3]))
    print(h1, h2, end='')
    if h1 == ():  # computer lost, don't move
        h1_new, h2_new = h1, h2
    else:
        if level == 0:
            dumb = True
        elif level == 1:
            print("randomizing dumbness")
            dumb = random.randint(0,10) < 8
        else:
            dumb = False
        h2_new, h1_new = hit_game.get_best_move((h1, h2), dumb)
    label = hit_game.get_label((h2_new, h1_new))
    if label == hit.WIN:
        message = "I think you can win..."
    elif label == hit.LOSE:
        message = "I think I will win..."
    else:
        message = ""
    h2_new = list(h2_new) + [0] * (2 - len(h2_new))
    h1_new = list(h1_new) + [0] * (2 - len(h1_new))

    # try to change the order, so it fits the status before move 
    if h2_new[0] == v[3] or h2_new[1] == v[2]:
        h2_new = h2_new[1], h2_new[0]
        print("it was", h2, "change to", h2_new)
    if h1_new[0] == v[1] or h1_new[1] == v[0]:
        h1_new = h1_new[1], h1_new[0]
    
    if h2_new == (0,0):
        big_message = "You Lost!"
        message = ""
    elif h1_new == (0,0):
        big_message = "You Won!"
        message = ""
    else:
        big_message = ""
    # avoid changing selected level
    checked = ["", "", ""]
    checked[level] = "checked"
    return render_template('h.html', v=[h1_new[0], h1_new[1], h2_new[0], h2_new[1]],
                                     small_message=message,
                                     big_message=big_message,
                                     checked=checked)
    

if __name__ == "__main__":
    init_game()
    app.run(debug=True)

