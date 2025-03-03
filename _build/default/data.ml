open Lwt.Infix
open Cohttp_lwt_unix

let id = "10000002"

(* Output the data to a file page_x.json *)
let fetch (page_number: int): unit =
  let url = "https://esi.evetech.net/dev/markets/" ^ id ^ "/orders/?datasource=tranquility&order_type=all&page=" ^ (page_number |> string_of_int) in
  let uri = Uri.of_string url in

  (* wow this ocaml language kinda sucks really bad *)
  Lwt_main.run (
    Client.get uri >>= fun (_res, body) ->
    Cohttp_lwt.Body.to_string body >>= fun str ->
      Lwt_io.with_file ~mode:Lwt_io.Output ("page_" ^ id ^ "_" ^ (page_number |> string_of_int) ^ ".json") (fun oc ->
        Lwt_io.write oc str
      )
  )
