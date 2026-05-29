import axios from "axios"

const API = "http://localhost:8000"

export const get_teams = () => axios.get(`${API}/teams`)
export const get_team_card_info = (team_id) => axios.get(`${API}/teams/${team_id}/card_info`)
export const get_team_logo = (team_id) => `https://cdn.nba.com/logos/nba/${team_id}/primary/L/logo.svg`