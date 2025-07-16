open List

def myfunc (xs ys : List Nat) : IO (List Nat) := do
  if he : xs.length = ys.length then
    let mut res := nil
    for hi : i in 0...xs.length do
      res := (xs[i]'?h1 + ys[i]'?h2) :: res
    return res
  else
    panic! "lengths not same"
where finally
  case h1 =>
    exact hi.2
  case h2 =>
    rw [← he]
    exact hi.2
