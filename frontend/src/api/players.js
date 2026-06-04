import axios from "axios"

const API = "http://localhost:8000"

export const get_infos = (player_id) => axios.get(`${API}/players/${player_id}/card_info`)
export const get_headshots = (player_id) => `https://cdn.nba.com/headshots/nba/latest/1040x760/${player_id}.png`
export const get_leaders = () => axios.get(`${API}/players/leaders`)