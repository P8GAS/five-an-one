import { NavLink } from "react-router-dom"
import styles from "./Navbar.module.css"

export default function Navbar() {
  return (
    <nav className={styles.nav}>
      <span className={styles.logo}>🏀</span>
      <div className={styles.links}>
        <NavLink
          to="/teams"
          className={({ isActive }) => isActive ? `${styles.link} ${styles.active}` : styles.link}
        >
          Teams
        </NavLink>
        <NavLink
          to="/players"
          className={({ isActive }) => isActive ? `${styles.link} ${styles.active}` : styles.link}
        >
          Players
        </NavLink>
      </div>
    </nav>
  )
}