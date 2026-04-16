from flask import Flask, render_template, request
from collections import deque

app = Flask(__name__)

# Graf berbobot
graph = {
    "Batu 10": {"RSUP": 2, "Batu 8": 3},
    "RSUP": {"Batu 10": 2, "Kampung Bugis": 4},
    "Batu 8": {"Batu 10": 3, "Kota Piring": 2},
    "Kampung Bugis": {"RSUP": 4, "Senggarang": 3},
    "Kota Piring": {"Batu 8": 2, "Senggarang": 5},
    "Senggarang": {"Kampung Bugis": 3, "Kota Piring": 5}
}

# Koordinat titik di Tanjungpinang
coords = {
    "Batu 10": [0.9200411, 104.5120340],
    "RSUP": [0.9241577, 104.5000892],
    "Batu 8": [0.90031, 104.48648],
    "Kampung Bugis": [0.9551846, 104.4707004],
    "Kota Piring": [0.9173611, 104.4852806],
    "Senggarang": [0.9614345, 104.4310834],
}

map_center = [0.91683, 104.44329]


def path_cost(path):
    total = 0
    for a, b in zip(path, path[1:]):
        total += graph[a][b]
    return total


def bfs(start, goal):
    if start == goal:
        return [start], 0

    queue = deque([[start]])
    visited = {start}

    while queue:
        path = queue.popleft()
        node = path[-1]

        if node == goal:
            return path, path_cost(path)

        for neighbor in graph[node]:
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append(path + [neighbor])

    return None, None


def dfs(start, goal):
    if start == goal:
        return [start], 0

    stack = [[start]]
    visited = set()

    while stack:
        path = stack.pop()
        node = path[-1]

        if node == goal:
            return path, path_cost(path)

        if node in visited:
            continue
        visited.add(node)

        neighbors = list(graph[node].keys())[::-1]
        for neighbor in neighbors:
            if neighbor not in visited:
                stack.append(path + [neighbor])

    return None, None


def route_coords(path):
    if not path:
        return []
    return [coords[node] for node in path]


@app.route("/", methods=["GET", "POST"])
def index():
    nodes = list(graph.keys())

    start = ""
    goal = ""
    method = "compare"

    result_bfs = None
    result_dfs = None
    bfs_coords = []
    dfs_coords = []

    if request.method == "POST":
        start = request.form.get("start", "")
        goal = request.form.get("goal", "")
        method = request.form.get("method", "compare")

        if start in graph and goal in graph:
            if method in ["bfs", "compare"]:
                path, cost = bfs(start, goal)
                if path:
                    bfs_coords = route_coords(path)
                    result_bfs = {
                        "path": path,
                        "cost": cost
                    }

            if method in ["dfs", "compare"]:
                path, cost = dfs(start, goal)
                if path:
                    dfs_coords = route_coords(path)
                    result_dfs = {
                        "path": path,
                        "cost": cost
                    }

    return render_template(
        "index.html",
        nodes=nodes,
        start=start,
        goal=goal,
        result_bfs=result_bfs,
        result_dfs=result_dfs,
        coords=coords,
        map_center=map_center,
        bfs_coords=bfs_coords,
        dfs_coords=dfs_coords
    )


if __name__ == "__main__":
    app.run(debug=True)