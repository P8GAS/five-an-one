import { useEffect, useState } from "react"
import { get_team_card_info, get_team_logo } from "../api/teams"
import styles from "./TeamCard.module.css"

export default function TeamCard({ team }) {
  const [card_info, set_card_info] = useState(null)
  const [loading, set_loading] = useState(true)

  useEffect(() => {
    get_team_card_info(team.id)
      .then(res => set_card_info(res.data))
      .finally(() => set_loading(false))
  }, [team.id])

  return (
        <div className={styles.card}>
      <div className={styles.top}>
        <img
          src={get_team_logo(team.id)}
          alt={team.full_name}
          className={styles.logo}
        />
        <div className={styles.identity}>
          <span className={styles.city}>{team.city}</span>
          <h2 className={styles.name}>{team.nickname}</h2>
          <span className={styles.abbr}>{team.abbreviation}</span>
        </div>
      </div>
 
      <div className={styles.divider} />
 
      {loading && <p className={styles.loading}>Chargement…</p>}
 
      {card_info && (
        <div className={styles.info}>
          <div className={styles.infoRow}>
            <span className={styles.label}>Coach</span>
            <span className={styles.value}>{card_info.info.HEADCOACH || "N/A"}</span>
          </div>
          <div className={styles.infoRow}>
            <span className={styles.label}>Titulaires</span>
            <div className={styles.starters}>
              {card_info.starters.map(id => (
                <span key={id} className={styles.starter}>#{id}</span>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>

  )
}