import { useRef } from "react"
import { get_headshots } from "../../api/players"
import { get_team_logo } from "../../api/teams"
import styles from "../Players/PlayerCard.module.css"

export default function PlayerCard({ player }) {
  const cardRef = useRef(null)

  const handleMouseMove = (e) => {
    const card = cardRef.current
    if (!card) return
    const rect = card.getBoundingClientRect()
    const x = (e.clientX - rect.left) / rect.width
    const y = (e.clientY - rect.top) / rect.height
    const tiltX = (y - 0.5) * -12
    const tiltY = (x - 0.5) * 12
    card.style.transform = `perspective(800px) rotateX(${tiltX}deg) rotateY(${tiltY}deg)`
  }

  const handleMouseLeave = () => {
    const card = cardRef.current
    if (!card) return
    card.style.transform = `perspective(800px) rotateX(0deg) rotateY(0deg)`
  }

  const stats = [
    { label: "PTS", value: player.PTS },
    { label: "REB", value: player.REB },
    { label: "AST", value: player.AST },
    { label: "STL", value: player.STL },
    { label: "BLK", value: player.BLK },
    { label: "+/-", value: player.PLUS_MINUS },
  ]

  return (
    <div
      className={styles.card}
      ref={cardRef}
      onMouseMove={handleMouseMove}
      onMouseLeave={handleMouseLeave}
    >
      <div className={styles.left}>
        <div className={styles.photoWrapper}>
          <img
            src={get_headshots(player.PLAYER_ID)}
            alt={player.PLAYER_NAME}
            className={styles.photo}
          />
        </div>
        <div className={styles.identity}>
          <span className={styles.name}>{player.PLAYER_NAME}</span>
          <div className={styles.team}>
            <img
              src={get_team_logo(player.TEAM_ID)}
              alt={player.TEAM_ABBREVIATION}
              className={styles.teamLogo}
            />
            <span className={styles.teamName}>{player.TEAM_ABBREVIATION}</span>
          </div>
        </div>
      </div>

      <div className={styles.divider} />

      <div className={styles.stats}>
        <span className={styles.statsTitle}>Stats</span>
        <div className={styles.statsList}>
          {stats.map(s => (
            <div key={s.label} className={styles.statRow}>
              <span className={styles.statLabel}>{s.label}</span>
              <span className={styles.statValue}>{s.value}</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}