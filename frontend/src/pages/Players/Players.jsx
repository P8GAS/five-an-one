import { useEffect, useState } from "react"
import { get_leaders } from "../../api/players"
import PlayerCard from "../../components/Players/PlayerCard"
import styles from "./Players.module.css"

export default function Players() {
  const [players, setPlayers] = useState([])
  const [search, setSearch] = useState("")
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    get_leaders()
      .then(res => setPlayers(res.data))
      .finally(() => setLoading(false))
  }, [])

  const filtered = players.filter(p =>
    p.PLAYER_NAME.toLowerCase().includes(search.toLowerCase())
  )

  return (
    <div className={styles.page}>
      <header className={styles.header}>
        <h1 className={styles.title}>Players</h1>
        <input
          className={styles.search}
          placeholder="Rechercher un joueur…"
          value={search}
          onChange={e => setSearch(e.target.value)}
        />
      </header>
      {loading ? (
        <div className={styles.loader}>Chargement…</div>
      ) : (
        <div className={styles.grid}>
          {filtered.map(player => (
            <PlayerCard key={player.PLAYER_ID} player={player} />
          ))}
        </div>
      )}
    </div>
  )
}