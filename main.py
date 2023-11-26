from mrt_paths import *
from autocomplete import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    if request.method == "POST":
        start = request.form["start"].lower()
        end = request.form["end"].lower()
        # every mrt stop has title format except for one-north
        if start.lower() != 'one-north':
            start = start.title()   
        if end.lower() != 'one-north':
            end = end.title()
        shortest_path = mrt_graph.find_shortest_path(start, end) 
        mrt_lines = mrt_graph.path_to_mrt_lines(shortest_path[1]) # from path generate list of the corresponding station codes
        rgb_codes = mrt_graph.mrt_lines_to_colour_code(mrt_lines)
        return render_template('index.html', shortest_path=shortest_path, start=start, end=end, mrt_lines=mrt_lines, rgb_codes=rgb_codes)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)