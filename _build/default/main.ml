open Data

let () =
  let i = ref 71 in
  while true do
    fetch !i;
    i := !i + 1;
  done;

