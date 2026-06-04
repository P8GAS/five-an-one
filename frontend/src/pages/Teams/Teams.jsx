import { useEffect, useState } from "react"
import { get_teams } from "../../api/teams"
import TeamCard from "../../components/Teams/TeamCard"
import styles from "./Teams.module.css"

export default function Teams() {
  const [teams, set_teams] = useState([])
  const [loading, set_loading] = useState(true)

  useEffect(() => {
    get_teams()
      .then(res => set_teams(res.data))
      .finally(() => set_loading(false))
  }, [])

  if (loading) return <p>Chargement...</p>

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <span className={styles.badge}>2025 – 26</span>
        <h1 className={styles.title}>NBA Dashboard</h1>
        <p className={styles.subtitle}>30 franchises · Saison en cours</p>
      </header>
 
      {loading ? (
        <div className={styles.loader}>Chargement des franchises…</div>
      ) : (
        <div className={styles.grid}>
          {teams.map(team => (
            <TeamCard key={team.id} team={team} />
          ))}
        </div>
      )}
    </div>

  )
}