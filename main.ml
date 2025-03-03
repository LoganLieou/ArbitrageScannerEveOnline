open Data
open Yojson.Basic.Util
open Yojson

module StringSet = Set.Make(struct
  type t = string
  let compare = compare
end)

let vis = ref StringSet.empty

let handler (filename: string): unit =
  let json = Basic.from_file filename |> to_list in
  List.iter (fun order ->
    let type_id = order |> member "type_id" |> Basic.to_string in
    if not (StringSet.find_opt type_id !vis |> Option.is_none) then
      print_endline type_id;
    vis := StringSet.add type_id !vis
  ) json

let () =
  let i = ref 71 in
  while true do
    fetch !i;
    i := !i + 1;
  done;

