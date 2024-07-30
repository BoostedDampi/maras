
from maraslib.engine import AnimationEngine

print("Code Animation")


engine = AnimationEngine("RobotoMono.ttf", 20)

slide0 = engine.new_slide("""
void Graph::DFS(int v)
{
Some code
}
""")

slide1 = engine.new_slide("""
void Graph::DFS(int v)
{
    // Mark the current node as visited and
    // print it
    visited[v] = true;
    cout << v << " ";

    // Recur for all the vertices adjacent
    // to this vertex
    list<int>::iterator i;
    for (i = adj[v].begin(); i != adj[v].end(); ++i){what is this? other code}
}
""")


slide2 = engine.new_slide("""
void Graph::DFS(int v)
{
    // Mark the current node as visited and
    // print it
    visited[v] = true;
    cout << v << " ";

    // Recur for all the vertices adjacent
    // to this vertex
    list<int>::iterator i;
    for (i = adj[v].begin(); i != adj[v].end(); ++i){
        if (!visited[*i]){
            DFS(*i);
        }
    }
}
""")


slide0.add_animation(engine.animator.show_before, 1)
slide0.add_animation(engine.animator.fade_out, 1)
slide0.add_animation(engine.animator.dynamic_move, 1)
slide0.add_animation(engine.animator.fade_in, 1)

slide1.add_animation(engine.animator.show_before, 1)
slide1.add_animation(engine.animator.fade_out, 1)
slide1.add_animation(engine.animator.dynamic_move, 1)
slide1.add_animation(engine.animator.fade_in, 1)

slide1.add_animation(engine.animator.show_before, 1)

engine.render()

