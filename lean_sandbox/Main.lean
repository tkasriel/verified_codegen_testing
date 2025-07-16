/-- Returns a fresh copy of an Array of Arrays -/
def deepCopy (g : Array (Array Nat)) : Array (Array Nat) :=
  g.map (fun row => row.map id)

/-- bfs for Ford-Fulkerson. Returns (foundPath, parent) -/
def bfs
  (graph : Array (Array Nat))
  (source sink : Nat)
: (Bool × Array (Option Nat)) :=
  let n := graph.size
  -- visited and parent arrays
  let rec go (queue : List Nat) (visited : Array Bool) (parent : Array (Option Nat)) : (Bool × Array (Option Nat)) :=
    match queue with
    | []      => (visited[sink]!, parent)
    | u :: qs =>
      let (visited, parent, queue) :=
        ((List.range n).foldl
          (fun (acc : Array Bool × Array (Option Nat) × List Nat) ind =>
            let (vis, par, q) := acc
            if ¬vis[ind]! ∧ graph[u]![ind]! > 0 then
              (vis.set! ind true, par.set! ind (some u), q ++ [ind])
            else
              acc)
          (visited, parent, qs))
      go queue visited parent
  let visited0 := Array.replicate n false |>.set! source true
  let parent0  := Array.replicate n none
  go [source] visited0 parent0

/-- find nodes reachable from source in residual graph returns a visited array -/
def reachableFrom (graph : Array (Array Nat)) (source : Nat) : Array Bool :=
  let n := graph.size
  let rec go (queue : List Nat) (vis : Array Bool) : Array Bool :=
    match queue with
    | [] => vis
    | u :: qs =>
      let (vis, queue) :=
        ((List.range n).foldl
          (fun (acc : Array Bool × List Nat) ind =>
            let (v, q) := acc
            if graph[u]![ind]! > 0 ∧ ¬v[ind]! then
              (v.set! ind true, q ++ [ind])
            else
              acc)
          (vis, qs))
      go queue vis
  go [source] (Array.replicate n false |>.set! source true)

/-- mincut core algorithm, functional style --/
def mincut (graphIn : Array (Array Nat)) (source sink : Nat) : List (Nat × Nat) :=
  let n := graphIn.size
  let temp := deepCopy graphIn
  -- Simulate mutating graph via recursion
  -- loop: (residual graph, flow so far) → (final residual, parent, final flow)
  let rec flowLoop (graph : Array (Array Nat)) (accFlow : Nat) : (Array (Array Nat) × Array (Option Nat) × Nat) :=
    let (found, par) := bfs graph source sink
    if ¬found then
      (graph, par, accFlow)
    else
      -- Find minimum path flow
      let rec pathMin (s : Nat) (f : Nat) : Nat :=
        if s = source then f
        else
          match par[s]! with
          | none   => f         -- shouldn't happen if found = true, but safe
          | some u => pathMin u (Nat.min f graph[u]![s]!)
      let flowval := pathMin sink 1000000000
      -- Update graph (residual)
      let rec updateGraph (s : Nat) (g : Array (Array Nat)) : Array (Array Nat) :=
        if s = source then g
        else
          match par[s]! with
          | none   => g
          | some u =>
            let newG_U := g[u]!.set! s (g[u]![s]! - flowval)
            let newG_S := g[s]!.set! u (g[s]![u]! + flowval)
            let g := g.set! u newG_U
            let g := g.set! s newG_S
            updateGraph u g
      let graph' := updateGraph sink graph
      flowLoop graph' (accFlow + flowval)
  let (residual, parentFinal, maxFlow) := flowLoop (deepCopy graphIn) 0
  let visited := reachableFrom residual source
  -- find all edges from reachable (visited) to non-reachable in original graph
  let mut res : List (Nat × Nat) := []
  for i in List.range n do
    for j in List.range n do
      if visited[i]! ∧ ¬visited[j]! ∧ temp[i]![j]! > 0 then
        res := res ++ [(i, j)]
  res

/-- Example test graph --/
def testGraph : Array (Array Nat) :=
  #[ #[0, 16, 13, 0, 0, 0],
     #[0, 0, 10, 12, 0, 0],
     #[0, 4, 0, 0, 14, 0],
     #[0, 0, 9, 0, 0, 20],
     #[0, 0, 0, 7, 0, 4],
     #[0, 0, 0, 0, 0, 0] ]

#eval mincut testGraph 0 5 -- [(1, 3), (4, 3), (4, 5)]
